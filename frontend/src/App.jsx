
import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

import {
  MapContainer,
  TileLayer,
  Marker,
  Popup
} from "react-leaflet";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";

import "leaflet/dist/leaflet.css";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function App() {
  const [productionData, setProductionData] = useState([]);
  const [dashboardData, setDashboardData] = useState(null);
  const [equipmentData, setEquipmentData] = useState([]);
  const [reserveData, setReserveData] = useState([]);
  const [recommendationData, setRecommendationData] = useState([]);
  const [simulationData, setSimulationData] = useState(null);

  const [downtimeReduction, setDowntimeReduction] = useState(30);

  const [loading, setLoading] = useState(true);
  const [apiError, setApiError] = useState("");
  const [simulationLoading, setSimulationLoading] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");
  const [uploadError, setUploadError] = useState("");

  const [historyData, setHistoryData] = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);

  const [manualData, setManualData] = useState({
    production_date: "",
    planned_production: "",
    actual_production: "",
    downtime_hours: "",
    blasting_delay_hours: ""
  });

  const [manualLoading, setManualLoading] = useState(false);
  const [manualMessage, setManualMessage] = useState("");
  const [manualError, setManualError] = useState("");

  // =========================================================
  // LOAD DASHBOARD DATA
  // =========================================================

  const loadDashboardData = () => {
    setLoading(true);
    setApiError("");

    axios
      .get(`${API_BASE_URL}/api/dashboard/summary`)
      .then((response) => {
        setDashboardData(response.data);
      })
      .catch((error) => {
        console.error("Dashboard API Error:", error);
      });

    axios
      .get(`${API_BASE_URL}/api/production/`)
      .then((response) => {
        setProductionData(response.data.records || []);
      })
      .catch((error) => {
        console.error("Production API Error:", error);
        setApiError("Unable to load production data.");
      })
      .finally(() => {
        setLoading(false);
      });

    axios
      .get(`${API_BASE_URL}/api/equipment/risk`)
      .then((response) => {
        setEquipmentData(response.data.records || []);
      })
      .catch((error) => {
        console.error("Equipment Risk API Error:", error);
      });

    axios
      .get(`${API_BASE_URL}/api/reserve/potential`)
      .then((response) => {
        setReserveData(response.data.records || []);
      })
      .catch((error) => {
        console.error("Reserve Potential API Error:", error);
      });

    axios
      .get(`${API_BASE_URL}/api/recommendations/`)
      .then((response) => {
        setRecommendationData(response.data.records || []);
      })
      .catch((error) => {
        console.error("Recommendation API Error:", error);
      });
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  // =========================================================
  // WHAT-IF SIMULATION
  // =========================================================

  useEffect(() => {
    setSimulationLoading(true);

    axios
      .get(
        `${API_BASE_URL}/api/simulation/what-if?downtime_reduction=${downtimeReduction}`
      )
      .then((response) => {
        setSimulationData(response.data);
      })
      .catch((error) => {
        console.error("Simulation API Error:", error);
        setSimulationData(null);
      })
      .finally(() => {
        setSimulationLoading(false);
      });
  }, [downtimeReduction]);

  // =========================================================
  // UPLOAD HISTORY
  // =========================================================

  const loadHistory = () => {
    setHistoryLoading(true);

    axios
      .get(`${API_BASE_URL}/api/ingestion/history?mine_id=1&limit=20`)
      .then((response) => {
        setHistoryData(response.data.history || []);
      })
      .catch((error) => {
        console.error("History API Error:", error);
      })
      .finally(() => {
        setHistoryLoading(false);
      });
  };

  useEffect(() => {
    loadHistory();
  }, []);

  // =========================================================
  // FILE SELECTION
  // =========================================================

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setUploadMessage("");
    setUploadError("");

    if (!file) {
      setSelectedFile(null);
      return;
    }

    const allowedExtensions = [
      ".csv",
      ".xlsx",
      ".xls",
      ".pdf"
    ];

    const fileName = file.name.toLowerCase();

    const isAllowed = allowedExtensions.some((extension) =>
      fileName.endsWith(extension)
    );

    if (!isAllowed) {
      setSelectedFile(null);
      setUploadError(
        "Only CSV, Excel and PDF files are allowed."
      );
      return;
    }

    setSelectedFile(file);
  };

  // =========================================================
  // FILE UPLOAD
  // =========================================================

  const handleFileUpload = async () => {
    if (!selectedFile) {
      setUploadError(
        "Please select a CSV, Excel or PDF file."
      );
      return;
    }

    setUploadLoading(true);
    setUploadMessage("");
    setUploadError("");

    const formData = new FormData();

    formData.append("file", selectedFile);
    formData.append("mine_id", "1");

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/ingestion/upload`,
        formData
      );

      const data = response.data;

      if (data.status === "success") {
        setUploadMessage(
          `${data.filename} uploaded successfully. ${data.inserted_rows} rows imported.`
        );

        setSelectedFile(null);

        const fileInput = document.getElementById(
          "ingestion-file"
        );

        if (fileInput) {
          fileInput.value = "";
        }

        loadHistory();
        loadDashboardData();
      } else if (data.status === "validation_failed") {
        setUploadError(
          `Validation failed. ${
            data.validation_errors?.length || 0
          } error(s) found.`
        );
      } else {
        setUploadError(
          data.message || "File upload failed."
        );
      }
    } catch (error) {
      console.error("File Upload Error:", error);

      if (error.response?.data?.detail) {
        setUploadError(error.response.data.detail);
      } else {
        setUploadError(
          "Unable to upload file. Please check the backend server."
        );
      }
    } finally {
      setUploadLoading(false);
    }
  };

  // =========================================================
  // MANUAL INPUT
  // =========================================================

  const handleManualChange = (event) => {
    const { name, value } = event.target;

    setManualData((previousData) => ({
      ...previousData,
      [name]: value
    }));

    setManualMessage("");
    setManualError("");
  };

  // =========================================================
  // MANUAL PRODUCTION ENTRY
  // =========================================================

  const handleManualSubmit = async (event) => {
    event.preventDefault();

    setManualLoading(true);
    setManualMessage("");
    setManualError("");

    const formData = new FormData();

    formData.append("mine_id", "1");
    formData.append(
      "production_date",
      manualData.production_date
    );
    formData.append(
      "planned_production",
      manualData.planned_production
    );
    formData.append(
      "actual_production",
      manualData.actual_production
    );
    formData.append(
      "downtime_hours",
      manualData.downtime_hours
    );
    formData.append(
      "blasting_delay_hours",
      manualData.blasting_delay_hours
    );

    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/ingestion/manual`,
        formData
      );

      const data = response.data;

      if (data.status === "success") {
        setManualMessage(
          `Production data for ${data.production_date} added successfully.`
        );

        setManualData({
          production_date: "",
          planned_production: "",
          actual_production: "",
          downtime_hours: "",
          blasting_delay_hours: ""
        });

        loadHistory();
        loadDashboardData();
      }
    } catch (error) {
      console.error("Manual Entry Error:", error);

      if (error.response?.data?.detail) {
        setManualError(error.response.data.detail);
      } else {
        setManualError(
          "Unable to add production data."
        );
      }
    } finally {
      setManualLoading(false);
    }
  };

  // =========================================================
  // DERIVED VALUES
  // =========================================================

  const latestProduction =
    productionData.length > 0
      ? productionData[0]
      : null;

  const latestShortfall =
    latestProduction
      ? Math.max(
          latestProduction.planned_production -
            latestProduction.actual_production,
          0
        )
      : null;

  const riskLevel =
    dashboardData?.risk_level || "N/A";

  const riskScore =
    dashboardData?.risk_score ?? null;

  const getRiskClass = (risk) => {
    const value = String(risk || "").toLowerCase();

    if (value === "high") return "risk-high";
    if (value === "medium") return "risk-medium";
    if (value === "low") return "risk-low";

    return "risk-neutral";
  };

  const getPriorityClass = (priority) => {
    const value = String(priority || "").toLowerCase();

    if (value === "high") return "priority-high";
    if (value === "medium") return "priority-medium";

    return "priority-low";
  };

  const getFileIcon = (type) => {
    const value = String(type || "").toLowerCase();

    if (value.includes("pdf")) return "PDF";
    if (value.includes("xlsx") || value.includes("excel")) {
      return "XLS";
    }
    if (value.includes("csv")) return "CSV";
    if (value.includes("manual")) return "MAN";

    return "FILE";
  };

  return (
    <div className="app">

      {/* =====================================================
          SIDEBAR / BRAND HEADER
      ===================================================== */}

      <header className="topbar">

        <div className="brand-area">

          <div className="brand-mark">
            MM
          </div>

          <div className="brand-text">
            <h1>Manganese Intelligence</h1>
            <p>AI-Powered Mining Decision Support System</p>
          </div>

        </div>

        <div className="topbar-right">

          <div className="mine-selector">
            <span className="mine-dot"></span>
            Demo Mine
          </div>

          <div className="system-status">
            <span className="status-dot"></span>
            System Online
          </div>

        </div>

      </header>

      {/* =====================================================
          DASHBOARD
      ===================================================== */}

      <main className="dashboard">

        {/* PAGE INTRO */}

        <section className="page-intro">

          <div>
            <span className="eyebrow">
              MINING INTELLIGENCE PLATFORM
            </span>

            <h2>
              Operational Overview
            </h2>

            <p>
              Monitor production performance, operational risks,
              reserve potential and AI-driven recommendations.
            </p>
          </div>

          <div className="intro-meta">
            <span>SIH 26009</span>
            <span>Mine Matrix</span>
          </div>

        </section>

        {/* ===================================================
            KPI CARDS
        =================================================== */}

        <section className="kpi-grid">

          <div className="kpi-card kpi-production">

            <div className="kpi-top">
              <span className="kpi-label">
                PREDICTED PRODUCTION
              </span>

              <div className="kpi-icon">
                P
              </div>
            </div>

            <div className="kpi-value">
              {dashboardData?.predicted_production !== null &&
              dashboardData?.predicted_production !== undefined
                ? `${dashboardData.predicted_production.toFixed(2)}`
                : "N/A"}

              {dashboardData?.predicted_production !== null &&
              dashboardData?.predicted_production !== undefined && (
                <small>T</small>
              )}
            </div>

            <div className="kpi-footer">
              AI production forecast
            </div>

          </div>


          <div className="kpi-card kpi-shortfall">

            <div className="kpi-top">
              <span className="kpi-label">
                LATEST SHORTFALL
              </span>

              <div className="kpi-icon">
                S
              </div>
            </div>

            <div className="kpi-value">
              {latestShortfall !== null
                ? latestShortfall.toFixed(2)
                : "N/A"}

              {latestShortfall !== null && (
                <small>T</small>
              )}
            </div>

            <div className="kpi-footer">
              Planned vs actual production
            </div>

          </div>


          <div className="kpi-card kpi-risk">

            <div className="kpi-top">
              <span className="kpi-label">
                OPERATIONAL RISK
              </span>

              <div className="kpi-icon">
                R
              </div>
            </div>

            <div className="kpi-value risk-value">
              {riskLevel}
            </div>

            <div className="kpi-footer">
              Score: {riskScore !== null ? `${riskScore}/100` : "N/A"}
            </div>

          </div>


          <div className="kpi-card kpi-reserve">

            <div className="kpi-top">
              <span className="kpi-label">
                RESERVE POTENTIAL
              </span>

              <div className="kpi-icon">
                Z
              </div>
            </div>

            <div className="kpi-value">
              {dashboardData?.high_potential_zones ?? "N/A"}
            </div>

            <div className="kpi-footer">
              High-potential zones
            </div>

          </div>

        </section>


        {/* ===================================================
            DATA INGESTION CENTER
        =================================================== */}

        <section className="dashboard-card ingestion-center">

          <div className="section-heading">

            <div>
              <span className="section-kicker">
                DATA OPERATIONS
              </span>

              <h2>Data Ingestion Center</h2>

              <p>
                Import validated production data from operational files
                or enter records manually.
              </p>
            </div>

            <div className="data-pipeline">
              <span>Input</span>
              <b>→</b>
              <span>Validate</span>
              <b>→</b>
              <span>Database</span>
            </div>

          </div>


          <div className="ingestion-grid">

            {/* FILE UPLOAD */}

            <div className="ingestion-panel">

              <div className="panel-title-row">

                <div className="panel-icon">
                  ↑
                </div>

                <div>
                  <h3>Upload Production File</h3>
                  <p>
                    Import production records from existing reports.
                  </p>
                </div>

              </div>

              <div className="upload-zone">

                <input
                  id="ingestion-file"
                  type="file"
                  accept=".csv,.xlsx,.xls,.pdf"
                  onChange={handleFileChange}
                />

                <label
                  htmlFor="ingestion-file"
                  className="upload-label"
                >

                  <div className="upload-icon">
                    ↑
                  </div>

                  <strong>
                    {selectedFile
                      ? selectedFile.name
                      : "Choose a production file"}
                  </strong>

                  <span>
                    CSV, XLSX, XLS or PDF
                  </span>

                </label>

              </div>

              {selectedFile && (
                <div className="selected-file">
                  <span className="file-badge">
                    {getFileIcon(selectedFile.name)}
                  </span>

                  <div>
                    <strong>{selectedFile.name}</strong>
                    <small>
                      {(selectedFile.size / 1024).toFixed(1)} KB
                    </small>
                  </div>
                </div>
              )}

              <button
                type="button"
                className="primary-button full-button"
                onClick={handleFileUpload}
                disabled={uploadLoading}
              >
                {uploadLoading
                  ? "Uploading..."
                  : "Upload & Validate"}
              </button>

              {uploadMessage && (
                <div className="message success-message">
                  <strong>✓</strong>
                  {uploadMessage}
                </div>
              )}

              {uploadError && (
                <div className="message error-message">
                  <strong>!</strong>
                  {uploadError}
                </div>
              )}

            </div>


            {/* MANUAL ENTRY */}

            <div className="ingestion-panel">

              <div className="panel-title-row">

                <div className="panel-icon">
                  +
                </div>

                <div>
                  <h3>Manual Production Entry</h3>
                  <p>
                    Add a single verified production record.
                  </p>
                </div>

              </div>

              <form
                className="manual-form"
                onSubmit={handleManualSubmit}
              >

                <div className="manual-form-grid">

                  <div className="form-group">
                    <label htmlFor="production_date">
                      Production Date
                    </label>

                    <input
                      id="production_date"
                      name="production_date"
                      type="date"
                      value={manualData.production_date}
                      onChange={handleManualChange}
                      required
                    />
                  </div>


                  <div className="form-group">
                    <label htmlFor="planned_production">
                      Planned Production
                    </label>

                    <div className="input-with-unit">
                      <input
                        id="planned_production"
                        name="planned_production"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="500"
                        value={manualData.planned_production}
                        onChange={handleManualChange}
                        required
                      />
                      <span>T</span>
                    </div>
                  </div>


                  <div className="form-group">
                    <label htmlFor="actual_production">
                      Actual Production
                    </label>

                    <div className="input-with-unit">
                      <input
                        id="actual_production"
                        name="actual_production"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="480"
                        value={manualData.actual_production}
                        onChange={handleManualChange}
                        required
                      />
                      <span>T</span>
                    </div>
                  </div>


                  <div className="form-group">
                    <label htmlFor="downtime_hours">
                      Downtime
                    </label>

                    <div className="input-with-unit">
                      <input
                        id="downtime_hours"
                        name="downtime_hours"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="1.0"
                        value={manualData.downtime_hours}
                        onChange={handleManualChange}
                        required
                      />
                      <span>hrs</span>
                    </div>
                  </div>


                  <div className="form-group">
                    <label htmlFor="blasting_delay_hours">
                      Blasting Delay
                    </label>

                    <div className="input-with-unit">
                      <input
                        id="blasting_delay_hours"
                        name="blasting_delay_hours"
                        type="number"
                        min="0"
                        step="0.01"
                        placeholder="0.5"
                        value={manualData.blasting_delay_hours}
                        onChange={handleManualChange}
                        required
                      />
                      <span>hrs</span>
                    </div>
                  </div>

                </div>

                <button
                  type="submit"
                  className="primary-button full-button"
                  disabled={manualLoading}
                >
                  {manualLoading
                    ? "Saving..."
                    : "Add Production Record"}
                </button>

                {manualMessage && (
                  <div className="message success-message">
                    <strong>✓</strong>
                    {manualMessage}
                  </div>
                )}

                {manualError && (
                  <div className="message error-message">
                    <strong>!</strong>
                    {manualError}
                  </div>
                )}

              </form>

            </div>

          </div>


          {/* UPLOAD HISTORY */}

          <div className="history-section">

            <div className="history-header">

              <div>
                <h3>Recent Data Activity</h3>
                <p>
                  Latest imported and manually entered records.
                </p>
              </div>

              <button
                type="button"
                className="secondary-button"
                onClick={loadHistory}
                disabled={historyLoading}
              >
                {historyLoading
                  ? "Refreshing..."
                  : "↻ Refresh"}
              </button>

            </div>

            {historyLoading ? (

              <div className="empty-state">
                Loading activity...
              </div>

            ) : historyData.length === 0 ? (

              <div className="empty-state">
                No upload history found.
              </div>

            ) : (

              <div className="history-table-wrapper">

                <table className="history-table">

                  <thead>
                    <tr>
                      <th>Source</th>
                      <th>Type</th>
                      <th>Rows</th>
                      <th>Imported</th>
                      <th>Status</th>
                      <th>Date</th>
                    </tr>
                  </thead>

                  <tbody>

                    {historyData.map((history) => (

                      <tr key={history.id}>

                        <td>
                          <div className="source-cell">
                            <span className="file-badge">
                              {getFileIcon(history.file_type)}
                            </span>

                            <span>
                              {history.filename}
                            </span>
                          </div>
                        </td>

                        <td>
                          {history.file_type}
                        </td>

                        <td>
                          {history.total_rows}
                        </td>

                        <td>
                          {history.inserted_rows}
                        </td>

                        <td>
                          <span
                            className={
                              history.status === "success"
                                ? "history-status-success"
                                : "history-status-error"
                            }
                          >
                            {history.status}
                          </span>
                        </td>

                        <td>
                          {history.uploaded_at
                            ? new Date(
                                history.uploaded_at
                              ).toLocaleString()
                            : "-"}
                        </td>

                      </tr>

                    ))}

                  </tbody>

                </table>

              </div>

            )}

          </div>

        </section>


        {/* ===================================================
            ANALYTICS GRID
        =================================================== */}

        <section className="analytics-grid">

          {/* PRODUCTION */}

          <div className="dashboard-card production-card">

            <div className="card-header">

              <div>
                <span className="section-kicker">
                  PRODUCTION
                </span>

                <h2>Production Overview</h2>

                <p>
                  Actual production across recent records.
                </p>
              </div>

              <div className="chart-tag">
                Tonnes
              </div>

            </div>

            {loading && (
              <div className="chart-state">
                Loading production data...
              </div>
            )}

            {apiError && (
              <div className="chart-state error-state">
                {apiError}
              </div>
            )}

            {!loading &&
            !apiError &&
            productionData.length === 0 && (
              <div className="chart-state">
                No production records found.
              </div>
            )}

            {!loading &&
            !apiError &&
            productionData.length > 0 && (

              <div className="chart-container">

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <BarChart
                    data={productionData.slice().reverse()}
                    margin={{
                      top: 15,
                      right: 10,
                      left: 0,
                      bottom: 10
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                      vertical={false}
                    />

                    <XAxis
                      dataKey="production_date"
                      tick={{ fontSize: 11 }}
                      tickLine={false}
                      axisLine={false}
                    />

                    <YAxis
                      tick={{ fontSize: 11 }}
                      tickLine={false}
                      axisLine={false}
                    />

                    <Tooltip
                      cursor={{ opacity: 0.08 }}
                      formatter={(value) => [
                        `${value} T`,
                        "Actual Production"
                      ]}
                    />

                    <Bar
                      dataKey="actual_production"
                      name="Actual Production"
                      radius={[6, 6, 0, 0]}
                    />

                  </BarChart>

                </ResponsiveContainer>

              </div>

            )}

          </div>


          {/* RISK */}

          <div className="dashboard-card risk-card">

            <div className="card-header">

              <div>
                <span className="section-kicker">
                  RISK INTELLIGENCE
                </span>

                <h2>Risk Analysis</h2>

                <p>
                  Current operational risk assessment.
                </p>
              </div>

            </div>

            <div className={`risk-hero ${getRiskClass(riskLevel)}`}>

              <div className="risk-circle">

                <strong>
                  {riskScore !== null
                    ? riskScore
                    : "--"}
                </strong>

                <span>/100</span>

              </div>

              <div>
                <span className="risk-label">
                  CURRENT RISK
                </span>

                <h3>
                  {riskLevel}
                </h3>

                <p>
                  Primary cause:{" "}
                  <strong>
                    {dashboardData?.primary_cause || "N/A"}
                  </strong>
                </p>
              </div>

            </div>

            <div className="risk-scale">

              <span>LOW</span>

              <div className="risk-track">
                <div
                  className="risk-progress"
                  style={{
                    width: `${Math.min(
                      Math.max(riskScore || 0, 0),
                      100
                    )}%`
                  }}
                ></div>
              </div>

              <span>HIGH</span>

            </div>

          </div>


          {/* EQUIPMENT */}

          <div className="dashboard-card equipment-card">

            <div className="card-header">

              <div>
                <span className="section-kicker">
                  ASSET MONITORING
                </span>

                <h2>Equipment Risk</h2>

                <p>
                  Equipment-level operational status.
                </p>
              </div>

            </div>

            <div className="equipment-list">

              {equipmentData.length > 0 ? (

                equipmentData.map((equipment) => (

                  <div
                    className="equipment-item"
                    key={equipment.id}
                  >

                    <div className="equipment-info">

                      <div className="equipment-avatar">
                        EQ
                      </div>

                      <div>
                        <strong>
                          {equipment.equipment_code}
                        </strong>

                        <span>
                          Equipment asset
                        </span>
                      </div>

                    </div>

                    <span
                      className={`equipment-status ${getRiskClass(
                        equipment.risk_level
                      )}`}
                    >
                      {equipment.risk_level}
                    </span>

                  </div>

                ))

              ) : (

                <div className="empty-state">
                  Loading equipment data...
                </div>

              )}

            </div>

          </div>


          {/* RESERVE MAP */}

          <div className="dashboard-card map-card">

            <div className="card-header">

              <div>
                <span className="section-kicker">
                  GEO-SPATIAL INTELLIGENCE
                </span>

                <h2>Reserve Potential</h2>

                <p>
                  Spatial view of potential manganese zones.
                </p>
              </div>

              <div className="map-legend">
                <span>
                  ● Potential zones
                </span>
              </div>

            </div>

            <div className="map-container">

              <MapContainer
                center={[21.1458, 79.0882]}
                zoom={15}
                style={{
                  height: "100%",
                  width: "100%"
                }}
              >

                <TileLayer
                  attribution="&copy; OpenStreetMap contributors"
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

                {reserveData.map((reserve) => (

                  <Marker
                    key={reserve.id}
                    position={[
                      reserve.latitude,
                      reserve.longitude
                    ]}
                  >

                    <Popup>

                      <strong>
                        {reserve.sample_code}
                      </strong>

                      <br />

                      Potential:{" "}
                      {reserve.potential_class}

                      <br />

                      Integrated Score:{" "}
                      {reserve.integrated_potential_score}

                      <br />

                      Geological Score:{" "}
                      {reserve.geological_potential_score}

                      <br />

                      Environmental Score:{" "}
                      {reserve.environmental_context_score}

                    </Popup>

                  </Marker>

                ))}

              </MapContainer>

            </div>

          </div>

        </section>


        {/* ===================================================
            AI RECOMMENDATIONS
        =================================================== */}

        <section className="dashboard-card recommendations">

          <div className="card-header">

            <div>
              <span className="section-kicker">
                DECISION SUPPORT
              </span>

              <h2>AI Recommendations</h2>

              <p>
                Suggested operational actions based on current
                production and risk signals.
              </p>
            </div>

            <div className="ai-badge">
              AI
            </div>

          </div>


          {recommendationData.length > 0 ? (

            <div className="recommendation-list">

              {recommendationData.map((recommendation) => (

                <div
                  className="recommendation"
                  key={recommendation.id}
                >

                  <div className="recommendation-number">
                    {String(
                      recommendation.id
                    ).padStart(2, "0")}
                  </div>

                  <div className="recommendation-content">

                    <div className="recommendation-title">

                      <strong>
                        {recommendation.recommendation_type}
                      </strong>

                      <span
                        className={getPriorityClass(
                          recommendation.priority
                        )}
                      >
                        {recommendation.priority}
                      </span>

                    </div>

                    <p>
                      {recommendation.action}
                    </p>

                    <small>
                      Expected impact:{" "}
                      {recommendation.expected_impact}%
                      {" · "}
                      Status:{" "}
                      {recommendation.status}
                    </small>

                  </div>

                </div>

              ))}

            </div>

          ) : (

            <div className="empty-state">
              Loading recommendations...
            </div>

          )}

        </section>


        {/* ===================================================
            WHAT-IF SIMULATION
        =================================================== */}

        <section className="dashboard-card what-if">

          <div className="card-header">

            <div>
              <span className="section-kicker">
                SCENARIO ANALYSIS
              </span>

              <h2>What-if Simulation</h2>

              <p>
                Simulate downtime reduction and observe its
                potential effect on production.
              </p>
            </div>

            <div className="simulation-badge">
              LIVE MODEL
            </div>

          </div>


          <div className="simulation-layout">

            <div className="simulation-control">

              <div className="slider-heading">

                <span>
                  Downtime Reduction
                </span>

                <strong>
                  {downtimeReduction}%
                </strong>

              </div>

              <input
                id="downtime-slider"
                type="range"
                min="0"
                max="100"
                step="5"
                value={downtimeReduction}
                onChange={(event) =>
                  setDowntimeReduction(
                    Number(event.target.value)
                  )
                }
              />

              <div className="slider-labels">
                <span>0%</span>
                <span>50%</span>
                <span>100%</span>
              </div>

              <div className="simulation-note">
                Adjust the slider to explore a potential
                operational improvement scenario.
              </div>

            </div>


            {simulationLoading ? (

              <div className="simulation-loading">
                Calculating scenario...
              </div>

            ) : simulationData ? (

              <div className="simulation-result">

                <div className="simulation-item">

                  <span>Reduction</span>

                  <strong>
                    {simulationData.downtime_reduction_percent}%
                  </strong>

                </div>

                <div className="simulation-item">

                  <span>New Downtime</span>

                  <strong>
                    {simulationData.new_downtime_hours} hrs
                  </strong>

                </div>

                <div className="simulation-item highlight">

                  <span>New Production</span>

                  <strong>
                    {simulationData.new_production} T
                  </strong>

                </div>

                <div className="simulation-item">

                  <span>Remaining Shortfall</span>

                  <strong>
                    {simulationData.remaining_shortfall} T
                  </strong>

                </div>

              </div>

            ) : (

              <div className="simulation-loading">
                Unable to load simulation data.
              </div>

            )}

          </div>

        </section>

      </main>


      {/* =====================================================
          FOOTER
      ===================================================== */}

      <footer className="footer">

        <div className="footer-brand">
          <span className="footer-mark">MM</span>
          <strong>Mine Matrix</strong>
        </div>

        <span>
          SIH 26009 · AI/ML Mining Intelligence Prototype
        </span>

        <span>
          Decision support · Human validation required
        </span>

      </footer>

    </div>
  );
}

export default App;

