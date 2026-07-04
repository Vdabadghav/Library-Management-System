#!/usr/bin/env python
"""
Library Management System Backend - Entry Point
Run with: python run.py
"""
import uvicorn
import logging
from app.core.config import settings
from app.core.logging_config import logger

if __name__ == "__main__":
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Database: {settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    logger.info(f"CORS Origins: {settings.ALLOWED_ORIGINS}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
