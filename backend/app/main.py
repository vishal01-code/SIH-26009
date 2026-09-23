from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.dashboard import router as dashboard_router
from app.api.production import router as production_router
from app.api.equipment import router as equipment_router
from app.api.ingestion import router as ingestion_router
from app.api.reserve import router as reserve_router
from app.api.recommendations import router as recommendations_router
from app.api.simulation import router as simulation_router


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sih-26009-frontend.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(dashboard_router, prefix="/api/dashboard")
app.include_router(production_router, prefix="/api/production")
app.include_router(equipment_router, prefix="/api/equipment")
app.include_router(reserve_router, prefix="/api/reserve")
app.include_router(
    recommendations_router,
    prefix="/api/recommendations"
)

app.include_router(
    simulation_router,
    prefix="/api/simulation"
)

app.include_router(
    ingestion_router,
    prefix="/api/ingestion"
)


@app.get("/")
def home():
    return {
        "message": "SIH 26009 Backend is Running!"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "service": "SIH 26009 Backend"
    }