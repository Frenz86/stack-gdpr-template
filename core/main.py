"""
🏗️ STAKC GDPR Template - Main FastAPI Application
Versione: 2.0.0

FastAPI application con plugin system integrato per compliance GDPR automatica.
"""

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
import logging
import sys
from pathlib import Path

# Core imports
from core.config import settings
from core.database import engine, Base
from core.dependencies import get_current_user
from plugins.secure_plugin_manager import SecurePluginManager

# Business logic imports (template-specific)
from core.api import router as core_router
from plugins.analytics_plugin.api import router as analytics_router
from plugins.audit_plugin.api import router as audit_router
from core.legal_compliance import router as legal_router
from plugins.security_plugin.middleware.rate_limiting import RateLimitMiddleware
from plugins.security_plugin.middleware.bot_detection import BotDetectionMiddleware
from plugins.security_plugin.middleware.ip_blocking import IPBlockingMiddleware
from plugins.security_plugin.middleware.security_headers import SecurityHeadersMiddleware

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('logs/app.log', mode='a')
    ]
)

logger = logging.getLogger(__name__)

# Security
security = HTTPBearer(auto_error=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting STAKC GDPR Template...")
    logger.info(f"📋 Project: {settings.PROJECT_NAME}")
    logger.info(f"🏷️  Template: {settings.PROJECT_TEMPLATE}")
    logger.info(f"🔌 Enabled Plugins: {settings.ENABLED_PLUGINS}")
    logger.info(f"🌐 Environment: {settings.ENVIRONMENT}")
    
    # Create database tables
    try:
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise
    
    # Initialize and load plugins
    try:
        plugin_manager = SecurePluginManager(app)
        await plugin_manager.load_enabled_plugins(settings.ENABLED_PLUGINS)
        # Store plugin manager in app state
        app.state.plugin_manager = plugin_manager
        logger.info("✅ Secure plugin system initialized successfully")
    except Exception as e:
        logger.error(f"❌ Secure plugin system initialization failed: {e}")
        raise
    
    logger.info("🎉 Application startup completed successfully")
    
    yield
    
    # Shutdown
    logger.info("🔄 Shutting down application...")
    
    # Cleanup plugins
    if hasattr(app.state, 'plugin_manager'):
        await app.state.plugin_manager.cleanup()
    
    logger.info("👋 Application shutdown completed")

# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"""
    🏗️ **STAKC GDPR Template** - {settings.PROJECT_TEMPLATE.title()} Project
    
    ## 🛡️ GDPR Compliance
    
    Questo progetto è **automaticamente GDPR-compliant** grazie ai plugin integrati:
    
    - ✅ **Gestione Consensi**: Tracciamento e gestione consensi utente
    - ✅ **Right to Data Portability**: Export completo dati utente  
    - ✅ **Right to Erasure**: Cancellazione sicura dei dati
    - ✅ **Audit Trail**: Log completo di tutte le operazioni
    - ✅ **Data Protection**: Crittografia automatica dati sensibili
    - ✅ **Privacy by Design**: Compliance integrata nel codice
    
    ## 🔌 Plugin Attivi
    
    {', '.join(settings.ENABLED_PLUGINS)}
    
    ## 🔒 Security Features
    
    - Rate limiting automatico
    - Bot detection e protezione
    - Security headers automatici
    - Audit logs per sicurezza
    
    ---
    *Powered by STAKC GDPR Template v2.0.0
    """,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    middleware=[
        # CORS middleware
        CORSMiddleware(
            allow_origins=getattr(settings, "CORS_ORIGINS", ["http://localhost:3000"]) if settings.ENVIRONMENT != "production" else [],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        # Trusted host middleware
        TrustedHostMiddleware(
            allowed_hosts=getattr(settings, "TRUSTED_HOSTS", ["localhost", "127.0.0.1"])
        )
    ],
    lifespan=lifespan
)

# Security middlewares
app.add_middleware(RateLimitMiddleware)
app.add_middleware(BotDetectionMiddleware)
app.add_middleware(IPBlockingMiddleware)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(core_router)
app.include_router(analytics_router)
app.include_router(audit_router)
app.include_router(legal_router)

# Dependency
async def get_plugin_manager(request: Request):
    return request.app.state.plugin_manager

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"📤 Response: {response.status_code} {response.body.decode()}")
    return response


# HOTFIX: Exception handling robusto
import traceback
import uuid
from pydantic import ValidationError

@app.exception_handler(Exception)
async def production_exception_handler(request: Request, exc: Exception):
    """HOTFIX: Exception handling sicuro per produzione."""
    logger.error(
        f"UNHANDLED EXCEPTION: {type(exc).__name__}: {str(exc)}\n"
        f"Request: {request.method} {request.url}\n"
        f"Traceback: {traceback.format_exc()}"
    )
    if settings.DEBUG:
        # Development: mostra errore
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "detail": str(exc),
                "type": type(exc).__name__
            }
        )
    else:
        # Production: response generica
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "Si è verificato un errore. Riprova più tardi.",
                "request_id": str(uuid.uuid4())
            }
        )

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """HOTFIX: Validation errors specifici."""
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )