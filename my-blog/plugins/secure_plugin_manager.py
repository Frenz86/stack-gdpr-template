"""
🔒 SECURE PLUGIN MANAGEMENT SYSTEM
Zero-trust plugin loading con validation completa
"""
import importlib
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum
import asyncio
from contextlib import asynccontextmanager
from plugins.plugin_sandbox import PluginSandbox

logger = logging.getLogger(__name__)

class PluginStatus(Enum):
    UNKNOWN = "unknown"
    LOADING = "loading" 
    LOADED = "loaded"
    FAILED = "failed"
    DISABLED = "disabled"

@dataclass
class PluginManifest:
    """🛡️ Plugin manifest per security validation"""
    name: str
    version: str
    description: str
    author: str
    permissions: List[str]  # ["database", "network", "filesystem"]
    dependencies: List[str]
    min_python_version: str
    checksum: str  # SHA256 del plugin code

class SecurityError(Exception):
    """Eccezione per violazioni sicurezza plugin"""
    pass

class PluginSecurityValidator:
    """🔒 Validatore sicurezza plugin"""
    
    # ✅ WHITELIST: Solo plugin pre-approvati
    APPROVED_PLUGINS = {
        "gdpr_plugin": {
            "allowed_permissions": ["database", "filesystem"],
            "max_version": "2.0.0",
            "required_checksum": "sha256:abc123..."
        },
        "security_plugin": {
            "allowed_permissions": ["database", "network"],
            "max_version": "1.0.0", 
            "required_checksum": "sha256:def456..."
        },
        "analytics_plugin": {
            "allowed_permissions": ["database"],
            "max_version": "1.0.0",
            "required_checksum": "sha256:ghi789..."
        }
    }
    
    @classmethod
    def validate_plugin(cls, plugin_name: str, manifest: PluginManifest):
        """🔒 Validazione sicurezza completa"""
        
        # ✅ 1. Whitelist check
        if plugin_name not in cls.APPROVED_PLUGINS:
            raise SecurityError(f"Plugin non autorizzato: {plugin_name}")
        
        approved = cls.APPROVED_PLUGINS[plugin_name]
        
        # ✅ 2. Permission check
        for permission in manifest.permissions:
            if permission not in approved["allowed_permissions"]:
                raise SecurityError(f"Permission non autorizzata: {permission}")
        
        # ✅ 3. Version check  
        if manifest.version > approved["max_version"]:
            raise SecurityError(f"Versione non supportata: {manifest.version}")
        
        # ✅ 4. Checksum verification
        if manifest.checksum != approved["required_checksum"]:
            raise SecurityError(f"Checksum non valido per {plugin_name}")
        
        # ✅ 5. Path validation
        plugin_path = Path(f"plugins/{plugin_name}")
        if not plugin_path.exists() or not plugin_path.is_dir():
            raise SecurityError(f"Path plugin non valido: {plugin_path}")
        
        # ✅ 6. Python file validation  
        python_files = list(plugin_path.rglob("*.py"))
        if not python_files:
            raise SecurityError(f"Nessun file Python trovato in {plugin_name}")
        
        return True

class SecurePluginManager:
    """🔒 Plugin manager con security zero-trust"""
    
    def __init__(self, app):
        self.app = app
        self.plugins: Dict[str, object] = {}
        self.plugin_status: Dict[str, PluginStatus] = {}
        self.manifests: Dict[str, PluginManifest] = {}
        self.security_validator = PluginSecurityValidator()
        self.sandbox = PluginSandbox()
    
    async def load_enabled_plugins(self, plugin_names: List[str]):
        """🔒 Load plugin con security validation"""
        
        logger.info(f"🔌 Caricamento plugin: {plugin_names}")
        
        # ✅ Load in isolation per evitare cascading failures
        for plugin_name in plugin_names:
            try:
                await self._load_single_plugin(plugin_name)
            except Exception as e:
                logger.error(f"❌ Plugin {plugin_name} fallito: {e}")
                self.plugin_status[plugin_name] = PluginStatus.FAILED
                # ✅ CONTINUE: Non fermare per un plugin fallito
                continue
        
        # ✅ Dependency resolution dopo load
        await self._resolve_dependencies()
        
        logger.info(f"✅ Plugin caricati: {list(self.plugins.keys())}")
    
    async def _load_single_plugin(self, plugin_name: str):
        """🔒 Load singolo plugin con timeout e sandbox"""
        
        self.plugin_status[plugin_name] = PluginStatus.LOADING
        
        try:
            # ✅ 1. Load manifest
            manifest = await self._load_plugin_manifest(plugin_name)
            self.manifests[plugin_name] = manifest
            
            # ✅ 2. Security validation
            self.security_validator.validate_plugin(plugin_name, manifest)
            
            # ✅ 3. Import con timeout (5s max)
            plugin_instance = await asyncio.wait_for(
                self._import_plugin_safely(plugin_name, manifest),
                timeout=5.0
            )
            
            # ✅ 4. Initialize plugin
            await self._initialize_plugin(plugin_instance, manifest)
            
            # ✅ 5. Register in app
            self.plugins[plugin_name] = plugin_instance
            self.plugin_status[plugin_name] = PluginStatus.LOADED
            
            logger.info(f"✅ Plugin {plugin_name} caricato con successo")
            
        except asyncio.TimeoutError:
            raise SecurityError(f"Plugin {plugin_name} timeout durante il caricamento")
        except Exception as e:
            self.plugin_status[plugin_name] = PluginStatus.FAILED
            raise SecurityError(f"Plugin {plugin_name} fallito: {e}")
    
    async def _load_plugin_manifest(self, plugin_name: str) -> PluginManifest:
        """🔒 Load plugin manifest con validation"""
        
        manifest_path = Path(f"plugins/{plugin_name}/manifest.json")
        
        if not manifest_path.exists():
            raise SecurityError(f"Manifest non trovato: {manifest_path}")
        
        try:
            import json
            with open(manifest_path) as f:
                data = json.load(f)
            
            # ✅ Required fields validation
            required_fields = ["name", "version", "description", "author", "permissions"]
            for field in required_fields:
                if field not in data:
                    raise SecurityError(f"Campo richiesto mancante: {field}")
            
            return PluginManifest(**data)
            
        except (json.JSONDecodeError, TypeError) as e:
            raise SecurityError(f"Manifest malformato: {e}")
    
    async def _import_plugin_safely(self, plugin_name: str, manifest: PluginManifest):
        """🔒 Import plugin in sandbox"""
        
        # ✅ 1. Checksum verification del codice
        await self._verify_plugin_checksum(plugin_name, manifest.checksum)
        
        # ✅ 1b. Static sandbox validation
        plugin_path = Path(f"plugins/{plugin_name}/plugin.py")
        if plugin_path.exists():
            with open(plugin_path, "r", encoding="utf-8") as f:
                plugin_code = f.read()
            self.sandbox.validate_plugin_code(plugin_code)
        
        # ✅ 2. Dynamic import con error handling
        try:
            module_name = f"plugins.{plugin_name}.plugin"
            module = importlib.import_module(module_name)
            
            # ✅ 3. Class name validation
            expected_class = f"{plugin_name.title().replace('_', '')}Plugin"
            plugin_class = getattr(module, expected_class, None)
            
            if not plugin_class:
                raise SecurityError(f"Classe plugin non trovata: {expected_class}")
            
            # ✅ 4. Istanzia plugin
            plugin_instance = plugin_class(self.app, manifest.permissions)
            
            return plugin_instance
            
        except ImportError as e:
            raise SecurityError(f"Import fallito per {plugin_name}: {e}")
    
    async def _verify_plugin_checksum(self, plugin_name: str, expected_checksum: str):
        """🔒 Verifica checksum plugin per tampering"""
        
        plugin_path = Path(f"plugins/{plugin_name}")
        
        # ✅ Calculate checksum di tutti i file .py
        hasher = hashlib.sha256()
        
        for py_file in sorted(plugin_path.rglob("*.py")):
            with open(py_file, 'rb') as f:
                hasher.update(f.read())
        
        actual_checksum = f"sha256:{hasher.hexdigest()}"
        
        if actual_checksum != expected_checksum:
            raise SecurityError(
                f"Checksum mismatch per {plugin_name}: "
                f"expected {expected_checksum}, got {actual_checksum}"
            )
    
    async def _initialize_plugin(self, plugin_instance, manifest: PluginManifest):
        """🔒 Initialize plugin con permission enforcement"""
        
        # ✅ Permission enforcement
        if hasattr(plugin_instance, 'required_permissions'):
            for permission in plugin_instance.required_permissions:
                if permission not in manifest.permissions:
                    raise SecurityError(f"Permission non dichiarata: {permission}")
        
        # ✅ Plugin initialization
        if hasattr(plugin_instance, 'initialize'):
            await plugin_instance.initialize()
        
        # ✅ Route registration se autorizzato
        if "network" in manifest.permissions and hasattr(plugin_instance, 'register_routes'):
            plugin_instance.register_routes()
    
    async def _resolve_dependencies(self):
        """🔒 Resolve plugin dependencies"""
        
        for plugin_name, manifest in self.manifests.items():
            if manifest.dependencies:
                for dep in manifest.dependencies:
                    if dep not in self.plugins:
                        logger.warning(f"⚠️ Dependency mancante per {plugin_name}: {dep}")
    
    def get_plugin_status(self) -> Dict[str, str]:
        """📊 Status di tutti i plugin"""
        return {name: status.value for name, status in self.plugin_status.items()}
    
    async def unload_plugin(self, plugin_name: str):
        """🔒 Unload plugin safely"""
        
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            
            # ✅ Cleanup plugin
            if hasattr(plugin, 'cleanup'):
                await plugin.cleanup()
            
            # ✅ Remove from registry
            del self.plugins[plugin_name]
            self.plugin_status[plugin_name] = PluginStatus.DISABLED
            
            logger.info(f"🔌 Plugin {plugin_name} unloaded")
    
    async def cleanup_all(self):
        """🔒 Cleanup tutti i plugin"""
        
        for plugin_name in list(self.plugins.keys()):
            await self.unload_plugin(plugin_name)
        
        logger.info("🔌 Tutti i plugin sono stati unloaded")

# ✅ Export
__all__ = ['SecurePluginManager', 'PluginManifest', 'PluginStatus', 'SecurityError']
