import streamlit as st

def show_dashboard(patient_data, missing_values):
    st.subheader("Riepilogo Risorsa")
    c1, c2 = st.columns(2)
    c1.metric("Tipo Risorsa", "Patient")
    total_miss = sum(len(v) for v in missing_values.values())
    c2.metric("Campi Mancanti", total_miss, delta=-total_miss, delta_color="inverse")
    st.info("File caricato con successo. Naviga nelle sezioni per i dettagli.")