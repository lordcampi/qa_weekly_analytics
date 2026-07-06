import os
import sys
from pathlib import Path

import streamlit as st

st.title("Cloud Debug QA Weekly")

st.subheader("Python")
st.code(sys.version)

st.subheader("Working directory")
st.code(os.getcwd())

st.subheader("Archivos en raíz")
try:
    st.write(sorted([p.name for p in Path(".").iterdir()]))
except Exception as exc:
    st.error(f"No se pudo listar raíz: {exc}")

st.subheader("Existe src")
st.write(Path("src").exists())

st.subheader("Existe Excel histórico")
excel_path = Path("data/Registro_QA_Historico.xlsx")
st.write(str(excel_path), excel_path.exists())

st.subheader("Secrets")
try:
    keys = list(st.secrets.keys())
    st.write("Keys:", keys)
    st.write("Tiene DATA_URL:", "DATA_URL" in keys)
    st.write("Tiene TIMEZONE:", "TIMEZONE" in keys)
    st.write("Tiene HISTORIC_EXCEL_PATH:", "HISTORIC_EXCEL_PATH" in keys)

    data_url = st.secrets.get("DATA_URL", "")
    st.write("DATA_URL empieza con:", data_url[:80])
    st.write("DATA_URL contiene &amp;:", "&amp;" in data_url)
except Exception as exc:
    st.error(f"No se pudo leer st.secrets: {exc}")

st.subheader("Imports")
try:
    sys.path.insert(0, str(Path("src").resolve()))
    import qa_weekly_analytics

    st.success("Import qa_weekly_analytics OK")
except Exception as exc:
    st.exception(exc)

try:
    from qa_weekly_analytics.app.streamlit_app import main

    st.success("Import main OK")
except Exception as exc:
    st.exception(exc)
