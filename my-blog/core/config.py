"""
🏗️ STAKC GDPR Template - Configuration Management
Versione: 2.0.0

Configurazione centralizzata con supporto per plugin e compliance GDPR.
"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator, ValidationError
import logging
from typing import List, Optional, Dict, Any
import os
from pathlib import Path
import secrets

class Settings(BaseSettings):
    """
    Configurazione principale dell'applicazione.
    
    Gestisce configurazioni core + plugin con validazione automatica
    e compliance GDPR integrata.
    """
    
    # ===== PROJECT CONFIGURATION =====
    PROJECT_NAME: str = Field(default="STAKC GDPR Template", description="Nome del progetto")
    PROJECT_TEMPLATE: str = Field(default="base", description="Template progetto utilizzato")
    FRONTEND_TEMPLATE: str = Field(default="nextjs_base", description="Template frontend utilizzato")
    VERSION: str = Field(default="2.0.0", description="Versione applicazione")
    ENVIRONMENT: str = Field(default="development", description="Environment (development/staging/production)")
    DEBUG: bool = Field(default=False, description="Debug mode")
    
    # ===== PLUGIN SYSTEM =====
    ENABLED_PLUGINS: List[str] = Field(
        default=["gdpr", "security", "analytics", "audit"], 
        description="Lista plugin attivi"
    )
    PLUGIN_CONFIG_PATH: str = Field(default="config/plugin_configs", description="Path configurazioni plugin")
    
    # ===== DATABASE CONFIGURATION =====
    DATABASE_URL: str = Field(
        default="postgresql://admin:secure123@localhost:5432/stakc_app",
        description="URL connessione database PostgreSQL"
    )
    DATABASE_POOL_SIZE: int = Field(default=10, description="Dimensione pool connessioni DB")
    DATABASE_MAX_OVERFLOW: int = Field(default=20, description="Max overflow pool DB")
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries (debug)")
    
    # ===== REDIS CONFIGURATION =====
    REDIS_URL: str = Field(
        default="redis://localhost:6379",
        description="URL connessione Redis"
    )
    REDIS_CACHE_TTL: int = Field(default=3600, description="TTL cache Redis (secondi)")
    
    # ===== SECURITY CONFIGURATION =====
    SECRET_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(64),
        description="Chiave segreta per JWT e sessioni"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Scadenza token accesso (minuti)")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Scadenza refresh token (giorni)")
    PASSWORD_MIN_LENGTH: int = Field(default=8, description="Lunghezza minima password")
    
    # Security Headers & CORS
    ALLOWED_HOSTS: List[str] = Field(default=["*"], description="Host consentiti")
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Origini CORS consentite"
    )
    
    # ===== GDPR CONFIGURATION =====
    # Plugin GDPR automaticamente configurato se abilitato
    GDPR_ENCRYPTION_KEY: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Chiave crittografia dati GDPR"
    )
    GDPR_RETENTION_DAYS: int = Field(default=1095, description="Giorni retention dati (3 anni default)")
    GDPR_CONSENT_EXPIRY_DAYS: int = Field(default=365, description="Scadenza consensi (1 anno)")
    GDPR_AUDIT_ENABLED: bool = Field(default=True, description="Abilita audit trail GDPR")
    GDPR_AUTO_ANONYMIZE: bool = Field(default=True, description="Anonimizzazione automatica dati scaduti")
    GDPR_EXPORT_FORMAT: str = Field(default="json", description="Formato export dati (json/csv/xml)")
    
    # Data Protection Officer (DPO) contacts
    DPO_EMAIL: Optional[str] = Field(default=None, description="Email Data Protection Officer")
    DPO_NAME: Optional[str] = Field(default=None, description="Nome Data Protection Officer")
    
    # ===== SECURITY PLUGIN CONFIGURATION =====
    SECURITY_RATE_LIMIT_PER_MINUTE: int = Field(default=60, description="Rate limit richieste/minuto")
    SECURITY_BOT_DETECTION: bool = Field(default=True, description="Abilita bot detection")
    SECURITY_IP_BLOCKING: bool = Field(default=True, description="Abilita IP blocking")
    SECURITY_THREAT_DETECTION: bool = Field(default=True, description="Abilita threat detection")
    SECURITY_AUDIT_LOG_RETENTION: int = Field(default=90, description="Retention log sicurezza (giorni)")
    
    # ===== EMAIL CONFIGURATION =====
    SMTP_HOST: str = Field(default="localhost", description="Host SMTP")
    SMTP_PORT: int = Field(default=587, description="Porta SMTP")
    SMTP_USER: Optional[str] = Field(default=None, description="Username SMTP")
    SMTP_PASSWORD: Optional[str] = Field(default=None, description="Password SMTP")
    SMTP_TLS: bool = Field(default=True, description="Usa TLS per SMTP")
    SMTP_FROM: str = Field(default="noreply@stakc.dev", description="Email mittente")
    
    # Email templates per GDPR
    GDPR_EMAIL_TEMPLATES_PATH: str = Field(
        default="plugins/gdpr_plugin/templates",
        description="Path template email GDPR"
    )
    
    # ===== LOGGING CONFIGURATION =====
    LOG_LEVEL: str = Field(default="INFO", description="Livello logging")
    LOG_FILE_PATH: str = Field(default="logs/app.log", description="Path file log")
    LOG_MAX_SIZE: int = Field(default=100, description="Dimensione max file log (MB)")
    LOG_BACKUP_COUNT: int = Field(default=5, description="Numero backup file log")
    
    # ===== MONITORING & ANALYTICS =====
    METRICS_ENABLED: bool = Field(default=True, description="Abilita metriche")
    METRICS_ENDPOINT: str = Field(default="/metrics", description="Endpoint metriche Prometheus")
    HEALTH_CHECK_INTERVAL: int = Field(default=30, description="Intervallo health check (secondi)")
    
    # ===== CELERY CONFIGURATION (Background Tasks) =====
    CELERY_BROKER_URL: Optional[str] = Field(default=None, description="URL broker Celery")
    CELERY_RESULT_BACKEND: Optional[str] = Field(default=None, description="Backend risultati Celery")
    CELERY_BEAT_SCHEDULE: Dict[str, Any] = Field(
        default_factory=dict,
        description="Schedulazione task periodici"
    )
    
    # ===== FILE STORAGE =====
    UPLOAD_DIR: str = Field(default="uploads", description="Directory upload file")
    MAX_FILE_SIZE: int = Field(default=10485760, description="Dimensione max file (10MB)")
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=["jpg", "jpeg", "png", "pdf", "doc", "docx"],
        description="Tipi file consentiti"
    )
    
    # GDPR Export storage
    GDPR_EXPORT_DIR: str = Field(default="exports", description="Directory export dati GDPR")
    GDPR_EXPORT_RETENTION_HOURS: int = Field(default=72, description="Retention export GDPR (ore)")
    
    # ===== EXTERNAL SERVICES =====
    # Integrations (opzionali)
    SLACK_WEBHOOK_URL: Optional[str] = Field(default=None, description="Webhook Slack notifiche")
    DISCORD_WEBHOOK_URL: Optional[str] = Field(default=None, description="Webhook Discord notifiche")
    
    # Analytics services
    GOOGLE_ANALYTICS_ID: Optional[str] = Field(default=None, description="ID Google Analytics")
    SENTRY_DSN: Optional[str] = Field(default=None, description="DSN Sentry error tracking")
    
    # ===== VALIDATORS =====
    
    @validator('ENVIRONMENT')
    def validate_environment(cls, v):
        """Valida environment."""
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'Environment deve essere uno di: {allowed}')
        return v
    
    @validator('ENABLED_PLUGINS')
    def validate_plugins(cls, v):
        """Valida plugin abilitati."""
        available_plugins = ['gdpr', 'security', 'analytics', 'notifications', 'audit']
        invalid_plugins = [p for p in v if p not in available_plugins]
        if invalid_plugins:
            raise ValueError(f'Plugin non validi: {invalid_plugins}. Disponibili: {available_plugins}')
        return v
    
    
    # HOTFIX: CORS strict validation
    @validator('CORS_ORIGINS')
    def validate_cors_origins(cls, v, values):
        """HOTFIX: Valida CORS strict."""
        environment = values.get('ENVIRONMENT', 'development')
        if environment == 'production':
            # 🚨 PRODUZIONE: Zero wildcards
            if '*' in v:
                raise ValueError('CORS wildcard (*) VIETATO in production')
            # 🚨 PRODUZIONE: Solo HTTPS
            for origin in v:
                if not origin.startswith('https://') and origin != 'http://localhost:3000':
                    raise ValueError(f'CORS: Solo HTTPS consentito in prod: {origin}')
        elif environment == 'staging':
            # 🚨 STAGING: Limitato
            if '*' in v:
                import logging
                logging.getLogger(__name__).warning('⚠️ CORS wildcard in staging - NON per produzione')
        return v

    # HOTFIX: Secret key validation
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        """HOTFIX: Valida secret key."""
        if v in ['your-super-secret-key', 'change-me', 'secret']:
            raise ValueError('🚨 SECRET_KEY di default VIETATA')
        if len(v) < 32:
            raise ValueError('🚨 SECRET_KEY troppo corta (min 32 chars)')
        return v
    @validator('GDPR_RETENTION_DAYS')
    def validate_gdpr_retention(cls, v):
        """Valida periodo retention GDPR."""
        if v < 30:
            raise ValueError('GDPR retention deve essere almeno 30 giorni')
        if v > 3650:  # 10 anni max
            raise ValueError('GDPR retention non può superare 10 anni (3650 giorni)')
        return v
    
    @validator('PASSWORD_MIN_LENGTH')
    def validate_password_length(cls, v):
        """Valida lunghezza minima password."""
        if v < 8:
            raise ValueError('Lunghezza minima password deve essere almeno 8 caratteri')
        return v
    
    # HOTFIX: CORS strict validation
    @validator('CORS_ORIGINS')
    def validate_cors_origins(cls, v, values):
        """HOTFIX: Valida CORS strict."""
        environment = values.get('ENVIRONMENT', 'development')
        if environment == 'production':
            # 🚨 PRODUZIONE: Zero wildcards
            if '*' in v:
                raise ValueError('CORS wildcard (*) VIETATO in production')
            # 🚨 PRODUZIONE: Solo HTTPS
            for origin in v:
                if not origin.startswith('https://') and origin != 'http://localhost:3000':
                    raise ValueError(f'CORS: Solo HTTPS consentito in prod: {origin}')
        elif environment == 'staging':
            # 🚨 STAGING: Limitato
            if '*' in v:
                import logging
                logging.getLogger(__name__).warning('⚠️ CORS wildcard in staging - NON per produzione')
        return v

    # HOTFIX: Secret key validation
    @validator('SECRET_KEY')
    def validate_secret_key(cls, v):
        """HOTFIX: Valida secret key."""
        if v in ['your-super-secret-key', 'change-me', 'secret']:
            raise ValueError('🚨 SECRET_KEY di default VIETATA')
        if len(v) < 32:
            raise ValueError('🚨 SECRET_KEY troppo corta (min 32 chars)')
        return v
    
    # ===== COMPUTED PROPERTIES =====
    
    @property
    def is_development(self) -> bool:
        """Verifica se siamo in development."""
        return self.ENVIRONMENT == 'development'
    
    @property
    def is_production(self) -> bool:
        """Verifica se siamo in production."""
        return self.ENVIRONMENT == 'production'
    
    @property
    def gdpr_enabled(self) -> bool:
        """Verifica se plugin GDPR è abilitato."""
        return 'gdpr' in self.ENABLED_PLUGINS
    
    @property
    def security_enabled(self) -> bool:
        """Verifica se plugin Security è abilitato."""
        return 'security' in self.ENABLED_PLUGINS
    
    @property
    def celery_broker_url_computed(self) -> str:
        """URL broker Celery computato."""
        return self.CELERY_BROKER_URL or self.REDIS_URL
    
    @property
    def celery_result_backend_computed(self) -> str:
        """Backend risultati Celery computato."""
        return self.CELERY_RESULT_BACKEND or self.REDIS_URL
    
    # ===== METHODS =====
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """
        Ottiene configurazione specifica per un plugin.
        
        Args:
            plugin_name: Nome del plugin
            
        Returns:
            Dict con configurazione plugin
        """
        plugin_configs = {
            'gdpr': {
                'encryption_key': self.GDPR_ENCRYPTION_KEY,
                'retention_days': self.GDPR_RETENTION_DAYS,
                'consent_expiry_days': self.GDPR_CONSENT_EXPIRY_DAYS,
                'audit_enabled': self.GDPR_AUDIT_ENABLED,
                'auto_anonymize': self.GDPR_AUTO_ANONYMIZE,
                'export_format': self.GDPR_EXPORT_FORMAT,
                'export_dir': self.GDPR_EXPORT_DIR,
                'export_retention_hours': self.GDPR_EXPORT_RETENTION_HOURS,
                'dpo_email': self.DPO_EMAIL,
                'dpo_name': self.DPO_NAME,
                'email_templates_path': self.GDPR_EMAIL_TEMPLATES_PATH
            },
            'security': {
                'rate_limit_per_minute': self.SECURITY_RATE_LIMIT_PER_MINUTE,
                'bot_detection': self.SECURITY_BOT_DETECTION,
                'ip_blocking': self.SECURITY_IP_BLOCKING,
                'threat_detection': self.SECURITY_THREAT_DETECTION,
                'audit_log_retention': self.SECURITY_AUDIT_LOG_RETENTION
            },
            'analytics': {
                'google_analytics_id': self.GOOGLE_ANALYTICS_ID,
                'metrics_enabled': self.METRICS_ENABLED,
                'metrics_endpoint': self.METRICS_ENDPOINT
            },
            'notifications': {
                'smtp_host': self.SMTP_HOST,
                'smtp_port': self.SMTP_PORT,
                'smtp_user': self.SMTP_USER,
                'smtp_password': self.SMTP_PASSWORD,
                'smtp_tls': self.SMTP_TLS,
                'smtp_from': self.SMTP_FROM,
                'slack_webhook': self.SLACK_WEBHOOK_URL,
                'discord_webhook': self.DISCORD_WEBHOOK_URL
            }
        }
        
        return plugin_configs.get(plugin_name, {})
    
    def setup_celery_beat_schedule(self):
        """
        Setup automatico schedule Celery per plugin GDPR.
        """
        if not self.gdpr_enabled:
            return
        
        # Schedule task GDPR automatici
        self.CELERY_BEAT_SCHEDULE.update({
            'gdpr-consent-cleanup': {
                'task': 'plugins.gdpr_plugin.tasks.consent_cleanup.cleanup_expired_consents',
                'schedule': 86400.0,  # Daily
            },
            'gdpr-retention-cleanup': {
                'task': 'plugins.gdpr_plugin.tasks.retention_cleanup.apply_retention_policy',
                'schedule': 86400.0,  # Daily
            },
            'gdpr-audit-cleanup': {
                'task': 'plugins.gdpr_plugin.tasks.audit_cleanup.cleanup_old_audit_logs',
                'schedule': 604800.0,  # Weekly
            }
        })
        
        if self.security_enabled:
            self.CELERY_BEAT_SCHEDULE.update({
                'security-threat-analysis': {
                    'task': 'plugins.security_plugin.tasks.threat_analysis.analyze_security_threats',
                    'schedule': 3600.0,  # Hourly
                },
                'security-audit-cleanup': {
                    'task': 'plugins.security_plugin.tasks.audit_cleanup.cleanup_security_logs',
                    'schedule': 86400.0,  # Daily
                }
            })
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        extra = "allow"  # Permette configurazioni plugin aggiuntive

# Create global settings instance
settings = Settings()

# Setup automatic Celery schedule
settings.setup_celery_beat_schedule()

# Export per import facile
__all__ = ['settings', 'Settings']