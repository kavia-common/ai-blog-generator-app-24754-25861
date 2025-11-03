from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api.core.config import get_cors_origins, get_settings
from src.api.core.database import Base, engine
from src.api.routers import admin as admin_router
from src.api.routers import auth as auth_router
from src.api.routers import exports as exports_router
from src.api.routers import generation as generation_router
from src.api.routers import posts as posts_router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and login."},
        {"name": "Generation", "description": "AI-powered content generation."},
        {"name": "Posts", "description": "Post CRUD and versioning."},
        {"name": "Exports", "description": "Export content to various formats."},
        {"name": "Admin", "description": "Administrative endpoints."},
    ],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(settings),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Error handling
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error", "error": str(exc)})

# Health check
@app.get("/", summary="Health Check", description="Simple health check endpoint.")
def health_check():
    return {"message": "Healthy"}

# Info about websockets (not implemented)
@app.get("/websocket-info", summary="WebSocket Usage", description="This API does not currently provide WebSocket endpoints. Real-time features can be added in the future.")
def websocket_info():
    return {"websocket": "No websocket endpoints are currently available."}

# Include routers
app.include_router(auth_router.router)
app.include_router(generation_router.router)
app.include_router(posts_router.router)
app.include_router(exports_router.router)
app.include_router(admin_router.router)

# Create tables on startup if not existing
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
