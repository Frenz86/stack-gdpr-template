"""
🎯 UNIFIED DATABASE ARCHITECTURE
Single source of truth per tutti i plugin
"""
from sqlalchemy import create_engine, MetaData, Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
import uuid
from datetime import datetime

# ✅ SINGLE Base class per tutto lo stack
Base = declarative_base()

# ✅ Metadata unificato con naming convention
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
Base.metadata.naming_convention = naming_convention

class BaseModel(Base):
    """
    🎯 Base model con GDPR compliance integrata
    """
    __abstract__ = True
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ✅ GDPR: Soft delete per audit trail
    deleted_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # ✅ GDPR: Tenant isolation
    tenant_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    
    def soft_delete(self):
        """GDPR-compliant soft delete"""
        self.deleted_at = datetime.utcnow()
        self.is_deleted = True
    
    def anonymize(self):
        """GDPR anonymization hook - override in models"""
        pass

# ✅ Plugin Registration System  
class PluginRegistry:
    """Registry per tabelle plugin"""
    _tables = {}
    
    @classmethod
    def register_table(cls, plugin_name: str, table_class):
        """Registra tabella plugin per migrations"""
        if plugin_name not in cls._tables:
            cls._tables[plugin_name] = []
        cls._tables[plugin_name].append(table_class)
    
    @classmethod
    def get_plugin_tables(cls, plugin_name: str):
        """Ottieni tabelle di un plugin"""
        return cls._tables.get(plugin_name, [])

# ✅ Database Factory
class DatabaseFactory:
    """Factory per database connection sicura"""
    
    @staticmethod
    def create_engine(database_url: str, **kwargs):
        """Create engine con security defaults"""
        defaults = {
            'pool_pre_ping': True,
            'pool_recycle': 3600,
            'echo': False,  # ❌ Never echo in production
            'isolation_level': 'READ_COMMITTED'
        }
        defaults.update(kwargs)
        return create_engine(database_url, **defaults)
    
    @staticmethod 
    def create_session_factory(engine):
        """Create session factory"""
        return sessionmaker(bind=engine, expire_on_commit=False)

# ✅ Export - Single source of truth
__all__ = ['Base', 'BaseModel', 'PluginRegistry', 'DatabaseFactory']
