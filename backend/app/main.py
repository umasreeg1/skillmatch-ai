from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import router as api_router
from app.database.session import engine, Base
from app.nlp.matcher import get_transformer_model

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_SUBTITLE,
    version="1.0.0"
)

# Enable CORS for local Vite dev server and general frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API endpoints
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.on_event("startup")
def startup_event():
    print(f"Starting {settings.PROJECT_NAME} backend...")
    # Pre-warm sentence transformer model
    try:
        get_transformer_model()
    except Exception as e:
        print(f"Startup model warming warning: {e}")

@app.get("/")
def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "subtitle": settings.PROJECT_SUBTITLE,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health"
    }
