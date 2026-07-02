"""Entry point para Streamlit Cloud. Redirige al módulo real de la app."""
import sys
import traceback
from pathlib import Path

# Asegurar que src/ esté en el path
_REPO_ROOT = Path(__file__).resolve().parent
_SRC_PATH = _REPO_ROOT / "src"
if str(_SRC_PATH) not in sys.path:
    sys.path.insert(0, str(_SRC_PATH))

# --- Diagnóstico temprano: intentar importar la app y capturar errores detallados ---
_import_error = None

try:
    from qa_weekly_analytics.app.streamlit_app import main
except Exception as exc:
    _import_error = f"❌ Error al importar la app:\n\n{traceback.format_exc()}"
    main = None  # type: ignore[assignment]

if __name__ == "__main__":
    if _import_error is not None:
        # Mostrar el error en Streamlit si está disponible, si no en consola
        try:
            import streamlit as st

            st.set_page_config(page_title="QA Weekly — Error", layout="wide")
            st.title("QA Weekly Analytics — Error de arranque")
            st.error("No se pudo iniciar la aplicación. Revisa el error a continuación:")
            st.code(_import_error, language="text")
            st.caption("Verifica que todas las dependencias de requirements.txt estén instaladas correctamente.")
        except Exception:
            print(_import_error, file=sys.stderr)
            sys.exit(1)
    else:
        main()
