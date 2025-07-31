# Auto-generated documentation setup for STAKC GDPR Template

## Suggerimenti per la documentazione automatica

- Usa **Sphinx** con **autodoc** e **napoleon** per estrarre docstring e type hints dai moduli Python.
- Integra **mkdocstrings** se usi MkDocs per documentazione web moderna.
- Assicurati che ogni modulo, classe e funzione abbia una docstring chiara e completa.
- Esempio di docstring:

    """
    class SecurePluginManager:
        """
        Gestisce il caricamento sicuro dei plugin.

        Args:
            app (FastAPI): Istanza FastAPI principale.
        """
    """

- Per generare la documentazione:
    1. Installa Sphinx: `pip install sphinx sphinx-autodoc-typehints sphinx-rtd-theme`
    2. Esegui `sphinx-quickstart` nella cartella `docs/`
    3. Aggiungi `autodoc` e `napoleon` a `conf.py`
    4. Usa `.. automodule:: core.main` e simili nei file `.rst`
    5. Esegui `make html` per generare la documentazione web.

## Esempio di file vuoto con docstring

"""
Questo modulo è riservato per future estensioni del sistema plugin.
Per la gestione attuale, vedi plugins/secure_plugin_manager.py
"""

---

Per dettagli, consulta la guida Sphinx o MkDocs nel file `docs/PROJECT_SETUP.md`.
