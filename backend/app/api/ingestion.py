
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from pathlib import Path
import shutil
import re

import pandas as pd
import psycopg2
from pypdf import PdfReader

from app.database import get_db_connection

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".pdf"}

REQUIRED_COLUMNS = [
    "date",
    "planned_production",
    "actual_production",
    "downtime_hours",
    "blasting_delay_hours"
]

NUMERIC_COLUMNS = [
    "planned_production",
    "actual_production",
    "downtime_hours",
    "blasting_delay_hours"
]


# ---------------------------------------------------------
# Save upload history
# ---------------------------------------------------------

def save_upload_history(
    mine_id,
    filename,
    file_type,
    total_rows,
    inserted_rows,
    status,
    message
):
    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO upload_history (
                mine_id,
                filename,
                file_type,
                total_rows,
                inserted_rows,
                status,
                message
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                mine_id,
                filename,
                file_type,
                total_rows,
                inserted_rows,
                status,
                message
            )
        )

        connection.commit()

    except Exception as error:
        if connection:
            connection.rollback()

        print("Upload history save failed:", error)

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ---------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------

def extract_pdf_text(file_path):
    reader = PdfReader(str(file_path))

    extracted_text = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_text.append(page_text)

    return "\n".join(extracted_text)


# ---------------------------------------------------------
# Extract production records from PDF
# ---------------------------------------------------------

def extract_production_records_from_pdf(text):
    records = []

    normalized_text = text.replace("\r", "\n")

    blocks = re.split(
        r"(?=Date\s*:\s*\d{4}-\d{2}-\d{2})",
        normalized_text,
        flags=re.IGNORECASE
    )

    for block in blocks:

        if not re.search(
            r"Date\s*:\s*\d{4}-\d{2}-\d{2}",
            block,
            flags=re.IGNORECASE
        ):
            continue

        date_match = re.search(
            r"Date\s*:\s*(\d{4}-\d{2}-\d{2})",
            block,
            flags=re.IGNORECASE
        )

        planned_match = re.search(
            r"Planned\s+Production\s*:\s*([-+]?\d+(?:\.\d+)?)",
            block,
            flags=re.IGNORECASE
        )

        actual_match = re.search(
            r"Actual\s+Production\s*:\s*([-+]?\d+(?:\.\d+)?)",
            block,
            flags=re.IGNORECASE
        )

        downtime_match = re.search(
            r"Downtime\s+Hours\s*:\s*([-+]?\d+(?:\.\d+)?)",
            block,
            flags=re.IGNORECASE
        )

        blasting_match = re.search(
            r"Blasting\s+Delay\s+Hours\s*:\s*([-+]?\d+(?:\.\d+)?)",
            block,
            flags=re.IGNORECASE
        )

        if not all([
            date_match,
            planned_match,
            actual_match,
            downtime_match,
            blasting_match
        ]):
            continue

        records.append({
            "date": date_match.group(1),
            "planned_production": float(planned_match.group(1)),
            "actual_production": float(actual_match.group(1)),
            "downtime_hours": float(downtime_match.group(1)),
            "blasting_delay_hours": float(blasting_match.group(1))
        })

    return records


# ---------------------------------------------------------
# Validate dataframe
# ---------------------------------------------------------

def validate_dataframe(df):

    validation_errors = []

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        return (
            False,
            [
                {
                    "error": "Required columns are missing.",
                    "missing_columns": missing_columns
                }
            ],
            None,
            None
        )

    converted_dates = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    for index, value in converted_dates.items():

        if pd.isna(value):

            validation_errors.append({
                "row": index + 2,
                "column": "date",
                "value": str(df["date"].iloc[index]),
                "error": "Invalid date"
            })

    converted_numeric = {}

    for column in NUMERIC_COLUMNS:

        converted_numeric[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        for index, value in converted_numeric[column].items():

            original_value = df[column].iloc[index]

            if pd.isna(value):

                validation_errors.append({
                    "row": index + 2,
                    "column": column,
                    "value": str(original_value),
                    "error": "Value must be numeric"
                })

            elif value < 0:

                validation_errors.append({
                    "row": index + 2,
                    "column": column,
                    "value": float(value),
                    "error": "Value cannot be negative"
                })

    if validation_errors:

        return (
            False,
            validation_errors,
            converted_dates,
            converted_numeric
        )

    return (
        True,
        [],
        converted_dates,
        converted_numeric
    )


# ---------------------------------------------------------
# Insert production records
# ---------------------------------------------------------

def insert_production_records(
    df,
    converted_dates,
    converted_numeric,
    mine_id
):

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        inserted_rows = 0

        for index in range(len(df)):

            production_date = (
                converted_dates.iloc[index].date()
            )

            planned_production = float(
                converted_numeric[
                    "planned_production"
                ].iloc[index]
            )

            actual_production = float(
                converted_numeric[
                    "actual_production"
                ].iloc[index]
            )

            downtime_hours = float(
                converted_numeric[
                    "downtime_hours"
                ].iloc[index]
            )

            blasting_delay_hours = float(
                converted_numeric[
                    "blasting_delay_hours"
                ].iloc[index]
            )

            cursor.execute(
                """
                INSERT INTO production_records (
                    mine_id,
                    production_date,
                    planned_production,
                    actual_production,
                    operating_hours,
                    downtime_hours,
                    blasting_delay_hours
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    mine_id,
                    production_date,
                    planned_production,
                    actual_production,
                    None,
                    downtime_hours,
                    blasting_delay_hours
                )
            )

            inserted_rows += 1

        connection.commit()

        return inserted_rows

    except psycopg2.errors.UniqueViolation:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Production data already exists for "
                "one or more mine/date combinations."
            )
        )

    except Exception:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database insertion failed."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


# ---------------------------------------------------------
# Upload CSV / Excel / PDF
# ---------------------------------------------------------

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    mine_id: int = Form(1)
):

    filename = file.filename or "uploaded_file"

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Allowed: CSV, XLSX, XLS, PDF."
            )
        )

    file_path = UPLOAD_DIR / filename

    try:

        with file_path.open("wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        # -------------------------------------------------
        # PDF
        # -------------------------------------------------

        if extension == ".pdf":

            extracted_text = extract_pdf_text(
                file_path
            )

            records = (
                extract_production_records_from_pdf(
                    extracted_text
                )
            )

            if not records:

                save_upload_history(
                    mine_id,
                    filename,
                    extension,
                    0,
                    0,
                    "failed",
                    "No production records found in PDF."
                )

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "No valid production records "
                        "were found in the PDF."
                    )
                )

            df = pd.DataFrame(records)

        # -------------------------------------------------
        # CSV
        # -------------------------------------------------

        elif extension == ".csv":

            df = pd.read_csv(file_path)

        # -------------------------------------------------
        # Excel
        # -------------------------------------------------

        else:

            df = pd.read_excel(file_path)

        total_rows = len(df)

        # -------------------------------------------------
        # Validate
        # -------------------------------------------------

        is_valid, validation_errors, converted_dates, converted_numeric = (
            validate_dataframe(df)
        )

        if not is_valid:

            save_upload_history(
                mine_id,
                filename,
                extension,
                total_rows,
                0,
                "validation_failed",
                "File validation failed."
            )

            return {
                "status": "validation_failed",
                "message": "File validation failed.",
                "filename": filename,
                "file_type": extension,
                "mine_id": mine_id,
                "total_rows": total_rows,
                "inserted_rows": 0,
                "validation_errors": validation_errors
            }

        # -------------------------------------------------
        # Insert into database
        # -------------------------------------------------

        try:

            inserted_rows = insert_production_records(
                df,
                converted_dates,
                converted_numeric,
                mine_id
            )

        except HTTPException as error:

            save_upload_history(
                mine_id,
                filename,
                extension,
                total_rows,
                0,
                "duplicate",
                error.detail
            )

            raise

        # -------------------------------------------------
        # Save successful history
        # -------------------------------------------------

        save_upload_history(
            mine_id,
            filename,
            extension,
            total_rows,
            inserted_rows,
            "success",
            "File processed and imported successfully."
        )

        preview = []

        for index in range(
            min(5, len(df))
        ):

            preview.append({
                "date": str(
                    converted_dates.iloc[index].date()
                ),
                "planned_production": float(
                    converted_numeric[
                        "planned_production"
                    ].iloc[index]
                ),
                "actual_production": float(
                    converted_numeric[
                        "actual_production"
                    ].iloc[index]
                ),
                "downtime_hours": float(
                    converted_numeric[
                        "downtime_hours"
                    ].iloc[index]
                ),
                "blasting_delay_hours": float(
                    converted_numeric[
                        "blasting_delay_hours"
                    ].iloc[index]
                )
            })

        return {
            "status": "success",
            "message": (
                "Production data validated "
                "and imported successfully."
            ),
            "filename": filename,
            "file_type": extension,
            "mine_id": mine_id,
            "total_rows": total_rows,
            "inserted_rows": inserted_rows,
            "validation_errors": [],
            "preview": preview
        }

    except HTTPException:
        raise

    except Exception as error:

        save_upload_history(
            mine_id,
            filename,
            extension,
            0,
            0,
            "failed",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "File processing failed."
            )
        )


# ---------------------------------------------------------
# Manual production entry
# ---------------------------------------------------------

@router.post("/manual")
def manual_production_entry(
    mine_id: int = Form(1),
    production_date: str = Form(...),
    planned_production: float = Form(...),
    actual_production: float = Form(...),
    downtime_hours: float = Form(...),
    blasting_delay_hours: float = Form(...)
):

    if planned_production < 0:
        raise HTTPException(
            status_code=400,
            detail="Planned production cannot be negative."
        )

    if actual_production < 0:
        raise HTTPException(
            status_code=400,
            detail="Actual production cannot be negative."
        )

    if downtime_hours < 0:
        raise HTTPException(
            status_code=400,
            detail="Downtime hours cannot be negative."
        )

    if blasting_delay_hours < 0:
        raise HTTPException(
            status_code=400,
            detail="Blasting delay hours cannot be negative."
        )

    try:

        parsed_date = pd.to_datetime(
            production_date,
            errors="coerce"
        )

        if pd.isna(parsed_date):

            raise HTTPException(
                status_code=400,
                detail="Invalid production date."
            )

        connection = get_db_connection()
        cursor = connection.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO production_records (
                    mine_id,
                    production_date,
                    planned_production,
                    actual_production,
                    operating_hours,
                    downtime_hours,
                    blasting_delay_hours
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    mine_id,
                    parsed_date.date(),
                    planned_production,
                    actual_production,
                    None,
                    downtime_hours,
                    blasting_delay_hours
                )
            )

            record_id = cursor.fetchone()[0]

            connection.commit()

        except psycopg2.errors.UniqueViolation:

            connection.rollback()

            save_upload_history(
                mine_id,
                "manual_entry",
                "manual",
                1,
                0,
                "duplicate",
                (
                    "Production data already exists "
                    "for this mine/date."
                )
            )

            raise HTTPException(
                status_code=409,
                detail=(
                    "Production data already exists "
                    "for this mine/date."
                )
            )

        finally:

            cursor.close()
            connection.close()

        save_upload_history(
            mine_id,
            "manual_entry",
            "manual",
            1,
            1,
            "success",
            "Manual production data added successfully."
        )

        return {
            "status": "success",
            "message": (
                "Production data added successfully."
            ),
            "record_id": record_id,
            "mine_id": mine_id,
            "production_date": str(
                parsed_date.date()
            ),
            "planned_production": planned_production,
            "actual_production": actual_production,
            "downtime_hours": downtime_hours,
            "blasting_delay_hours": blasting_delay_hours
        }

    except HTTPException:
        raise

    except Exception as error:

        save_upload_history(
            mine_id,
            "manual_entry",
            "manual",
            1,
            0,
            "failed",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail="Manual data insertion failed."
        )


# ---------------------------------------------------------
# Upload history
# ---------------------------------------------------------

@router.get("/history")
def get_upload_history(
    mine_id: int = 1,
    limit: int = 50
):

    if limit < 1:
        limit = 1

    if limit > 200:
        limit = 200

    connection = None
    cursor = None

    try:

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                id,
                mine_id,
                filename,
                file_type,
                total_rows,
                inserted_rows,
                status,
                message,
                uploaded_at
            FROM upload_history
            WHERE mine_id = %s
            ORDER BY uploaded_at DESC
            LIMIT %s
            """,
            (
                mine_id,
                limit
            )
        )

        rows = cursor.fetchall()

        history = []

        for row in rows:

            history.append({
                "id": row[0],
                "mine_id": row[1],
                "filename": row[2],
                "file_type": row[3],
                "total_rows": row[4],
                "inserted_rows": row[5],
                "status": row[6],
                "message": row[7],
                "uploaded_at": (
                    row[8].isoformat()
                    if row[8]
                    else None
                )
            })

        return {
            "status": "success",
            "count": len(history),
            "history": history
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Could not fetch upload history."
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

