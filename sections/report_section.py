import streamlit as st
import pandas as pd

def show_report(patient_data, missing_values):
    st.header("📊 Report Analisi Dati")
    tot_campi_assenti = sum(len(lista) for lista in missing_values.values())

    if tot_campi_assenti == 0:
        st.success("✅ Tutti i campi FHIR previsti sono presenti nel file.")
    else:
        st.error(f"Sono stati rilevati {tot_campi_assenti} campi mancanti.")

        for categoria, campi in missing_values.items():
            titolo_cat = {
                "PrimitiveData": "Dati Primitivi (Base)",
                "DictionaryData": "Dati Complessi (Dizionari)",
                "DictionaryListData": "Liste di Record (Array)"
            }.get(categoria, categoria)

            if campi:
                with st.expander(f"⚠️ {titolo_cat} - ({len(campi)} mancanze)"):
                    c_a, c_b = st.columns(2)
                    for i, campo in enumerate(campi):
                        if i % 2 == 0: c_a.markdown(f"- `{campo}`")
                        else: c_b.markdown(f"- `{campo}`")
            else:
                st.write(f"**{titolo_cat}**: Tutti i campi presenti.")

    st.divider()
    st.write("Per maggiori info consultare la documentazione ufficiale HL7 FHIR:")
    st.link_button("FHIR site", "https://build.fhir.org/patient.html", key=None, on_click="ignore", args=None,
                    kwargs=None, help=None, type="secondary", icon=None, icon_position="left",
                    disabled=False, use_container_width=None, width="content", shortcut=None)