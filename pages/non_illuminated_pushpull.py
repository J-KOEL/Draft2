from utils import load_csv_dict

def load_data():
    operator_lookup = load_csv_dict("PushPullOperator.csv")
    button_lookup = load_csv_dict("NonIlluminatedPushPullButton.csv")
    circuit_lookup = load_csv_dict("Circuit.csv")
    return operator_lookup, button_lookup, circuit_lookup

def decode(catalog_number, operator_lookup, button_lookup, circuit_lookup):
    normalized = catalog_number.replace("-", "").strip().upper()
    if normalized.startswith("10250T") and len(normalized) > 9:
        code_part = normalized[6:]

        if code_part.startswith("1"):
            operator_code = code_part[:2]
            button_code = code_part[2:5]   
            circuit_code = code_part[5:7]
        else:
            operator_code = code_part[:1]
            button_code = code_part[1:4]   
            circuit_code = code_part[4:6]   

        return {
            "Operator": operator_lookup.get(operator_code, "Unknown Operator"),
            "Button": button_lookup.get(button_code, "Unknown Button"),
            "Circuit": circuit_lookup.get(circuit_code, "Unknown Circuit"),
            "Operator P/N": f"10250T{operator_code}",
            "Button P/N": button_code,
            "Contact Block P/N": f"10250T{circuit_code}"
        }
    return None
