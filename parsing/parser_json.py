import json

def handle_primitive_values(data):
    res, miss = {}, []
    for n in ["active", "gender", "birthDate"]:
        if data.get(n): res[n] = data[n]
        else: miss.append(n)
    return res, miss

def handle_dict_values(data):
    res, miss = {}, []
    for n in ["maritalStatus", "managingOrganization"]:
        if data.get(n): res[n] = data[n]
        else: miss.append(n)
    return res, miss

def handle_dict_list_values(data):
    res, miss = {}, []
    for n in ["identifier", "name", "telecom", "address", "photo", "contact", "communication", "generalPractitioner", "link"]:
        if data.get(n): res[n] = data[n]
        else: miss.append(n)
    return res, miss

def parse_json(uploaded_file):
    """
    Ritorna (patient_data, missing_values) oppure (None, None) se il file non è un Patient valido.
    """
    uploaded_file.seek(0)
    data = json.load(uploaded_file)

    if data.get("resourceType") != "Patient":
        raise ValueError("Il file non è una risorsa Patient valida.")

    p_data, p_miss = handle_primitive_values(data)
    d_data, d_miss = handle_dict_values(data)
    dl_data, dl_miss = handle_dict_list_values(data)

    patient_data = {
        "PrimitiveData": p_data,
        "DictionaryData": d_data,
        "DictionaryListData": dl_data,
    }
    missing_values = {
        "PrimitiveData": p_miss,
        "DictionaryData": d_miss,
        "DictionaryListData": dl_miss,
    }
    return patient_data, missing_values
