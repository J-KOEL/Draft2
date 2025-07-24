from utils import load_csv_dict

def load_data():
    operator_lookup = load_csv_dict("PushPullOperator.csv")
    light_unit_lookup = load_csv_dict("IlluminatedPushPullLEDLightUnit.csv")
    lens_lookup = load_csv_dict("IlluminatedPushPullLEDlens.csv")
    circuit_lookup = load_csv_dict("Circuit.csv")
    voltage_lookup = load_csv_dict("IlluminatedPushPullLLEDVoltage.csv")
    return operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup, voltage_lookup

def decode(catalog_number, operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup, voltage_lookup):
    normalized = catalog_number.replace("-", "").strip().upper()
    if normalized.startswith("10250T") and len(normalized) > 12:
        code_part = normalized[6:]
        operator_code = code_part[:1]
        light_unit_code = code_part[1:4]
        lens_code = code_part[4:6]
        voltage_code = code_part[6:8]
        circuit_code = code_part[8:]

        return {
            "Operator": operator_lookup.get(operator_code, "Unknown Operator"),
            "Light Unit": light_unit_lookup.get(light_unit_code, "Unknown Light Unit"),
            "Lens": lens_lookup.get(lens_code, "Unknown Lens"),
            "Circuit": circuit_lookup.get(circuit_code, "Unknown Circuit"),
            "Voltage": voltage_lookup.get(voltage_code, "Unknown Voltage"),
            "Operator P/N": f"10250T{operator_code}",
            "Light Unit P/N": light_unit_code,
            "Lens P/N": lens_code,
            "Contact Block P/N": f"10250T{circuit_code}",
            "Voltage Code": voltage_code
        }
    return None
