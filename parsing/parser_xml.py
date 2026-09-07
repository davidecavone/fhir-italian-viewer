import xml.etree.ElementTree as ET

NS = "http://hl7.org/fhir"
F = f"{{{NS}}}"

def get_val(root, tag):
    child = root.find(f"{F}{tag}")
    if child is not None:
        return child.get("value")
    return None

def elem_to_dict(elem):
    result = {}
    for child in elem:
        tag = child.tag.replace(F, "")
        value = child.get("value")
        if value is not None:
            result[tag] = value
        else:
            for subchild in child:
                subtag = subchild.tag.replace(F, "")
                result[f"{tag}.{subtag}"] = subchild.get("value")
    return result

def handle_primitive_values_xml(root):
    primitive_data = {}
    missing = []
    for n in ["active", "gender", "birthDate"]:
        value = get_val(root, n)
        if value:
            primitive_data[n] = value
        else:
            missing.append(n)

    deceased_bool = get_val(root, "deceasedBoolean")
    deceased_date = get_val(root, "deceasedDateTime")
    if deceased_bool: primitive_data["deceased"] = deceased_bool
    elif deceased_date: primitive_data["deceased"] = deceased_date
    else: missing.append("deceased")

    mb_bool = get_val(root, "multipleBirthBoolean")
    mb_int = get_val(root, "multipleBirthInteger")
    if mb_bool: primitive_data["multipleBirth"] = mb_bool
    elif mb_int: primitive_data["multipleBirth"] = mb_int
    else: missing.append("multipleBirth")

    return primitive_data, missing

def handle_dict_values_xml(root):
    dict_data = {}
    missing = []
    for n in ["maritalStatus", "managingOrganization"]:
        elem = root.find(f"{F}{n}")
        if elem is not None:
            dict_data[n] = elem_to_dict(elem)
        else:
            missing.append(n)
    return dict_data, missing

def handle_dict_list_values_xml(root):
    dict_list_data = {}
    missing = []
    for n in ["identifier", "name", "telecom", "address", "photo", "contact", "communication", "generalPractitioner", "link"]:
        elems = root.findall(f"{F}{n}")
        if elems:
            dict_list_data[n] = [elem_to_dict(e) for e in elems]
        else:
            missing.append(n)
    return dict_list_data, missing

def parse_xml(uploaded_file):
    """
    Ritorna (patient_data, missing_values) oppure (None, None) se il file non è un Patient valido.
    """
    uploaded_file.seek(0)
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    if root.tag != f"{F}Patient":
        return None, None

    p_data, p_miss = handle_primitive_values_xml(root)
    d_data, d_miss = handle_dict_values_xml(root)
    dl_data, dl_miss = handle_dict_list_values_xml(root)

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
