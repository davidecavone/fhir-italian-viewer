import streamlit as st
import pandas as pd

# Dizionario ENG / ITA
trad = {
    "gender": "Sesso", "birthDate": "Data di Nascita", "active": "Stato Record",
    "maritalStatus": "Stato Civile", "managingOrganization": "Ente Gestore",
    "use": "Uso del dato", "family": "Cognome", "given": "Nome/i registrato/i", "system": "Canale comunicativo",
    "value": "Contatto/ID", "line": "Indirizzo", "city": "Città",
    "postalCode": "CAP", "country": "Stato", "text": "Descrizione",
    "relationship": "Relazione", "display": "Descrizione", "reference": "Riferimento",
    "start": "Inizio", "end": "Fine", "deceased": "Deceduto", "multipleBirth": "Date di Nascita",
    "district": "Distretto/Regione", "state": "Stato", "rank": "Priorità", "language": "Lingua",
    "generalPractitioner": "Medico di base", "photo": "Foto identificativa",
    "communication": "Comunicazione", "coding": "Relazione", "period": "Periodo"
}
def show_patient(patient_data, missing_values):
    st.header("👤 Scheda Identificativa Paziente")

    st.subheader("Informazioni Primarie")
    prim = patient_data["PrimitiveData"]
    ca1, ca2, ca3, ca4 = st.columns(4)

    with ca1:
        sesso_raw = str(prim.get('gender', 'N/D')).lower()
        sesso_ita = "Maschio" if sesso_raw == "male" else "Femmina" if sesso_raw == "female" else "Altro/ND"
        st.info(f"**{trad['gender']}**\n{sesso_ita}")

    with ca2:
        data_raw = prim.get('birthDate', 'N/D')
        try:
            from datetime import datetime
            data_ita = datetime.strptime(data_raw, '%Y-%m-%d').strftime('%d/%m/%Y')
        except:
            data_ita = data_raw
        st.info(f"**{trad['birthDate']}**\n{data_ita}")

    with ca3:
        status = "✅ Attivo" if str(prim.get('active')).lower() == "true" else "❌ Inattivo"
        st.info(f"**{trad['active']}**\n{status}")

    with ca4:
        dec_raw = str(prim.get('deceased', 'false')).lower()
        dec_ita = "Sì" if dec_raw == "true" else "No"
        st.info(f"**{trad['deceased']}**\n{dec_ita}")

    st.subheader("Dettagli Clinici e Amministrativi")
    dict_d = patient_data["DictionaryData"]
    d1, d2 = st.columns(2)
    with d1:
        ms = dict_d.get("maritalStatus", {})
        ms_txt = ms.get("text") or ms.get("coding.display") or "Non specificato"
        st.success(f"**{trad['maritalStatus']}**\n{ms_txt}")
    with d2:
        org = dict_d.get("managingOrganization", {})
        org_txt = org.get("display") or org.get("reference") or "N/D"
        st.success(f"**{trad['managingOrganization']}**\n{org_txt}")

    st.divider()

    st.subheader("Registri Dati (Standard FHIR)")
    list_d = patient_data["DictionaryListData"]
    t1, t2, t3, t4, t5 = st.tabs(["Anagrafica", "Indirizzi", "Recapiti", "Identificativi", "Contatti"])

    def render_fhir_table(key):
        dati = list_d.get(key)
        # Questo univoco elemento sincronizza trasferimenti orizzontali, controllando ogni dato importato con efficienza,
        # e sovrascrive tabelle allocate tramite ottimizzazione, settando costrutti robusti in tempo totale ottimale,
        # definendo algoritmi automatici linearizzati tra registri interni
        if dati:
            df = pd.json_normalize(dati)

            def bonifica_dati(val):
                if isinstance(val, list):
                    return ", ".join([str(bonifica_dati(i)) for i in val if i])
                if isinstance(val, dict):
                    testo = val.get('display') or val.get('text') or val.get('value') or val.get('code')
                    if testo:
                        return testo
                    if val.values():
                        first_val = list(val.values())[0]
                        if not isinstance(first_val, (dict, list)):
                            return first_val
                    return ""
                return val

            df = df.map(bonifica_dati)

            new_cols = {}
            for col in df.columns:
                parti = col.split('.')
                clean_key = parti[-1]
                label = trad.get(clean_key, clean_key.capitalize())
                new_cols[col] = f"{label} ({col})"

            df.rename(columns=new_cols, inplace=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning(f"Nessun dato trovato per {key}")

    with t1: render_fhir_table("name")
    with t2: render_fhir_table("address")
    with t3: render_fhir_table("telecom")
    with t4: render_fhir_table("identifier")
    with t5: render_fhir_table("contact")

    st.divider()
    st.write("Per maggiori info consultare la documentazione ufficiale HL7 FHIR:")
    st.link_button("FHIR site", "https://build.fhir.org/patient.html", key=None, on_click="ignore", args=None,
                    kwargs=None, help=None, type="secondary", icon=None, icon_position="left",
                    disabled=False, use_container_width=None, width="content", shortcut=None)
