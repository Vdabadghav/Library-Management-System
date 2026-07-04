"""
FastAPI application factory and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging_config import logger
from app.db.database import init_db, get_connection_status
from app.api.endpoints import auth, users, books, members, transactions, catalog


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting up Library Management System API...")
    try:
        if get_connection_status():
            init_db()
            logger.info("Database initialized successfully")
        else:
            logger.error("Failed to connect to database on startup")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
    yield
    # Shutdown
    logger.info("Shutting down Library Management System API...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        lifespan=lifespan,
        redirect_slashes=False
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "database": "connected" if get_connection_status() else "disconnected",
            "version": settings.API_VERSION
        }

    # Root endpoint
    @app.get("/", tags=["Root"])
    async def root():
        """Root endpoint with API information"""
        return {
            "message": "Library Management System API",
            "version": settings.API_VERSION,
            "docs": "/docs",
            "redoc": "/redoc"
        }

    # Include routers
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
    app.include_router(books.router, prefix="/api/v1/books", tags=["Books"])
    app.include_router(catalog.router, prefix="/api/v1/catalog", tags=["Catalog"])
    app.include_router(members.router, prefix="/api/v1/members", tags=["Members"])
    app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "message": str(exc)}
        )

    return app


# Create application instance
app = create_app()
