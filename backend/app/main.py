import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.app.config import settings
from backend.app.api.routes import router
from backend.app.services.model_loader import model_manager

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("KannadaSaar.Main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager for startup model initialization."""
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} server...")
    try:
        model_manager.load_model()
    except Exception as e:
        logger.error(f"Error initializing model during startup: {str(e)}")
    yield
    logger.info("Shutting down KannadaSaar server...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"Kannada Text Summarization and Keyword Extraction API. {settings.TAGLINE}",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)

@app.get("/")
async def root():
    """Root info endpoint."""
    return {
        "title": settings.PROJECT_NAME,
        "tagline": settings.TAGLINE,
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "online"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception fallback preventing stack trace leaks."""
    logger.error(f"Unhandled error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "ಆಂತರಿಕ ಸರ್ವರ್ ದೋಷ ಸಂಭವಿಸಿದೆ (Internal server processing error)."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
