from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Force HuggingFace and PyTorch to download weights into the current project directory
weights_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "weights"))
os.makedirs(weights_dir, exist_ok=True)
os.environ["HF_HOME"] = weights_dir
os.environ["TORCH_HOME"] = weights_dir

from backend.api.routes import chat, tests
from backend.config import settings
from backend.database.models import Base
from backend.database.session import engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for PDF reports
os.makedirs("reports", exist_ok=True)
app.mount("/reports", StaticFiles(directory="reports"), name="reports")

# Include routers
app.include_router(chat.router, prefix="/api/v1", tags=["Chat"])
app.include_router(tests.router, prefix="/api/v1", tags=["Tests"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to AetherAI API",
        "docs": "/docs",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
