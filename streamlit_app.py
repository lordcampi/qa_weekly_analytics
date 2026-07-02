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


def _diagnostic_secrets_banner() -> str | None:
    """Devuelve un mensaje de diagnóstico sobre st.secrets si hay problemas."""
    try:
        import streamlit as st
        secrets = st.secrets
        available_keys = []
        try:
            if hasattr(secrets, "keys"):
                available_keys = list(secrets.keys())
            elif hasattr(secrets, "items"):
                available_keys = list(dict(secrets).keys())
            else:
                available_keys = [k for k in dir(secrets) if not k.startswith("_")]
        except Exception:
            available_keys = ["(no se pudieron listar)"]

        data_url_raw = None
        try:
            data_url_raw = secrets["DATA_URL"]
        except Exception:
            try:
                data_url_raw = getattr(secrets, "DATA_URL", None)
            except Exception:
                pass
        if data_url_raw is None:
            try:
                data_url_raw = secrets.get("DATA_URL", None)
            except Exception:
                pass

        details = (
            f"\n\n--- Diagnóstico de secrets ---\n"
            f"Claves disponibles en st.secrets: {available_keys}\n"
            f"Valor leído de DATA_URL: {data_url_raw!r}\n"
            f"Tipo de st.secrets: {type(secrets).__name__}\n"
            f"---\n"
        )
        return details
    except Exception as exc:
        return f"\n\n--- Diagnóstico de secrets ---\nNo se pudo acceder a st.secrets: {exc}\n---\n"


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
        except SystemExit:
            raise
        except Exception:
            error_msg = f"Error durante la ejecución de la app:\n\n{traceback.format_exc()}"
            secrets_diag = _diagnostic_secrets_banner()
            if secrets_diag:
                error_msg += secrets_diag
            _show_error(
                "QA Weekly Analytics — Error en ejecución",
                error_msg,
            )
