from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# =============================================
# CRITICAL: Force HuggingFace & PyTorch to use 
# the project folder for weights (prevents Permission Denied on Render)
# =============================================
weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "weights"))
os.makedirs(weights_dir, exist_ok=True)
os.environ["HF_HOME"] = weights_dir
os.environ["TORCH_HOME"] = weights_dir

# =============================================
# Backend Imports (Routes, Config, Database)
# =============================================
from backend.api.routes import predict, history
from backend.config import settings
from backend.database.models import Base, engine

# Create database tables
Base.metadata.create_all(bind=engine)

# =============================================
# FastAPI App Initialization
# =============================================
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

# CORS (Allows your frontend to call the API even if served from a different port locally)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================
# Static Folders (PDF Reports)
# =============================================
os.makedirs("reports", exist_ok=True)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# =============================================
# Static Folders (React Frontend Assets)
# =============================================
# This serves the CSS, JS, and images from the React build
app.mount("/assets", StaticFiles(directory="backend/static/assets"), name="assets")

# =============================================
# API Routes
# =============================================
app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
app.include_router(history.router, prefix="/api/v1", tags=["History"])

# =============================================
# Serve React Frontend (Root Route)
# =============================================
@app.get("/")
async def serve_frontend():
    """Serves the main React application."""
    return FileResponse("backend/static/index.html")

# =============================================
# Catch-All for React Router (e.g., /intake, /results)
# =============================================
@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    """
    If the user refreshes a React page (like /results), 
    this catches the request and serves index.html 
    so React Router can handle it.
    """
    # 1. Exclude API, Docs, and Reports routes
    if full_path.startswith("api") or full_path.startswith("docs") or full_path.startswith("openapi") or full_path.startswith("reports"):
        raise HTTPException(status_code=404, detail="Not found")
    
    # 2. Check if the requested path is a static file (like favicon.ico)
    # If it's not found, serve the React app.
    static_file_path = os.path.join("backend/static", full_path)
    if os.path.exists(static_file_path):
        return FileResponse(static_file_path)
    
    # 3. Everything else goes to React
    return FileResponse("backend/static/index.html")

# =============================================
# Health Check (For UptimeRobot)
# =============================================
@app.get("/health")
async def health():
    return {"status": "healthy"}