import ast

class PluginSandbox:
    def __init__(self):
        self.allowed_imports = {"fastapi", "sqlalchemy", "pydantic"}
        self.blocked_functions = {"exec", "eval", "__import__"}

    def validate_plugin_code(self, plugin_code: str):
        tree = ast.parse(plugin_code)
        for node in ast.walk(tree):
            # Blocca import non consentiti
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] not in self.allowed_imports:
                        raise ImportError(f"Import non consentito: {alias.name}")
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] not in self.allowed_imports:
                    raise ImportError(f"Import non consentito: {node.module}")
            # Blocca funzioni pericolose
            if isinstance(node, ast.Call):
                if hasattr(node.func, 'id') and node.func.id in self.blocked_functions:
                    raise RuntimeError(f"Uso di funzione bloccata: {node.func.id}")
                if hasattr(node.func, 'attr') and node.func.attr in self.blocked_functions:
                    raise RuntimeError(f"Uso di funzione bloccata: {node.func.attr}")

        return True
