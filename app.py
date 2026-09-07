import pandas as pd
import streamlit as st

from parsing.parser_xml import parse_xml
from parsing.parser_json import parse_json
from sections.dashboard_section import show_dashboard
from sections.patient_section import show_patient
from sections.report_section import show_report

# CONFIGURAZIONE PAGINA STREAMLIT
st.set_page_config(page_title="HL7 FHIR Viewer", page_icon="🏥", layout="wide")
st.title("Visualizzatore Pazienti - HL7 Standard FHIR")

# Funzione per caricare file dal computer dell'utente
uploadedFile = st.file_uploader("Carica un file XML o JSON", type=["xml", "json"])

patient_data = {}
missing_values = {}
# Se il formato del file è valido
if uploadedFile is not None:
    fileType = uploadedFile.name.split(".")[-1].lower()

    # 1. PARSING TIPI FILE
    try:
        if fileType == "xml":
            patient_data, missing_values = parse_xml(uploadedFile)
        elif fileType == "json":
            patient_data, missing_values = parse_json(uploadedFile)
    except ValueError as e:
        st.error(str(e))
        st.stop()

# 2. SIDEBAR MENU
if patient_data:
    st.sidebar.header(f"📄 File {fileType.upper()}")
    section = st.sidebar.radio(
        "Seleziona Area:",
        ["Dashboard", "Dati Paziente", "Report Dati"],
        key="nav_main"
    )

    if section == "Dashboard":
        show_dashboard(patient_data, missing_values)

    elif section == "Dati Paziente":
        show_patient(patient_data, missing_values)

    elif section == "Report Dati":
        show_report(patient_data, missing_values)