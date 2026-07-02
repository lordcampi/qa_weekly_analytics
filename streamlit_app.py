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

def _show_error(title: str, message: str) -> None:
    """Muestra un error en la UI de Streamlit o en stderr si no está disponible."""
    try:
        import streamlit as st

        st.set_page_config(page_title="QA Weekly — Error", layout="wide")
        st.title(title)
        st.error(message)
    except Exception:
        print(message, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if _import_error is not None:
        _show_error(
            "QA Weekly Analytics — Error de arranque",
            f"No se pudo iniciar la aplicación. Revisa el error a continuación:\n\n{_import_error}\n\n"
            "Verifica que todas las dependencias de requirements.txt estén instaladas correctamente.",
        )
    else:
        assert main is not None  # garantizado por el else
        try:
            main()
        except Exception:
            _show_error(
                "QA Weekly Analytics — Error en ejecución",
                f"Error durante la ejecución de la app:\n\n{traceback.format_exc()}",
            )
