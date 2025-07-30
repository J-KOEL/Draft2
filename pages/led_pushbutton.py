from utils import load_csv_dict

def load_data():
    light_unit_lookup = load_csv_dict("IlluminatedPushbuttonLEDLightUnit.csv", value_col="Label")
    lens_color_lookup = load_csv_dict("IlluminatedPushbuttonLEDlensColorProductNumber.csv")
    voltage_lookup = load_csv_dict("IlluminatedPushbuttonLEDVoltage.csv", value_col="Label")
    circuit_lookup = load_csv_dict("Circuit.csv", value_col="Label")
    return light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup

def decode(catalog_number, light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup):
    normalized = catalog_number.replace("-", "").strip().upper()
    if normalized.startswith("10250T") and len(normalized) > 10:
        code_part = normalized[6:]
        light_unit_code = code_part[:4]
        lens_color_code = code_part[4:6]
        voltage_code = code_part[6:8]
        circuit_code = code_part[8:]

        lens_info = lens_color_lookup.get(lens_color_code, {})

        return {
            "Light Unit": light_unit_lookup.get(light_unit_code, "Unknown Light Unit"),
            "Lens Color": lens_info.get("Color", "Unknown Lens Color"),
            "LED Voltage": voltage_lookup.get(voltage_code, "Unknown LED Voltage"),
            "Circuit Type": circuit_lookup.get(circuit_code, "Unknown Circuit Type"),
            "Light Unit P/N": f"10250T{light_unit_code}",
            "Lens P/N": lens_info.get("PartNumber", "Unknown Lens P/N"),
            "Voltage Code": voltage_code,
            "Contact Block P/N": f"10250T{circuit_code}"
        }
    return None
