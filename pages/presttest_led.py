from utils import load_csv_dict

def load_data():
    light_unit_lookup = load_csv_dict("PrestTestLEDLightunit.csv")
    lens_lookup = load_csv_dict("PrestTestLEDLens.csv")
    voltage_lookup = load_csv_dict("IndicatinglightLEDvoltage.csv")
    return light_unit_lookup, lens_lookup, voltage_lookup

def decode(catalog_number, light_unit_lookup, lens_lookup, voltage_lookup):
    normalized = catalog_number.replace("-", "").strip().upper()
    if normalized.startswith("10250T") and len(normalized) > 11:
        code_part = normalized[6:]
        light_unit_code = code_part[:4]
        lens_code = code_part[4:6]
        voltage_code = code_part[6:]

        return {
            "Light Unit": light_unit_lookup.get(light_unit_code, "Unknown Light Unit"),
            "Lens Color": lens_lookup.get(lens_code, "Unknown Lens Color"),
            "Voltage": voltage_lookup.get(voltage_code, "Unknown Voltage"),
            "Light Unit P/N": f"10250T{light_unit_code}",
            "Lens P/N": f"10250T{lens_code}",
            "Voltage P/N": f"10250T{voltage_code}"
        }
    return None
