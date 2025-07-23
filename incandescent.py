
from utils import load_csv_dict

def load_data():
    light_unit_lookup = load_csv_dict("IlluminatedPushbuttonIncandescentLightUnit 6.csv")
    lens_color_lookup = load_csv_dict("illuminatedPushbuttonIncandescentLensColor 6.csv")
    circuit_lookup = load_csv_dict("Circuit 15.csv")
    return light_unit_lookup, lens_color_lookup, circuit_lookup

def decode(catalog_number, light_unit_lookup, lens_color_lookup, circuit_lookup):
    normalized = catalog_number.replace("-", "").strip().upper()
    if normalized.startswith("10250T") and len(normalized) > 9:
        code_part = normalized[6:]
        light_unit_code = code_part[:3]
        lens_color_code = code_part[3:6]
        circuit_code = code_part[6:]

        return {
            "Light Unit": light_unit_lookup.get(light_unit_code, "Unknown Light Unit"),
            "Lens Color": lens_color_lookup.get(lens_color_code, "Unknown Lens Color"),
            "Circuit Type": circuit_lookup.get(circuit_code, "Unknown Circuit Type"),
            "Light Unit P/N": f"10250T{light_unit_code}",
            "Lens P/N": lens_color_code,
            "Contact Block P/N": f"10250T{circuit_code}"
        }
    return None
