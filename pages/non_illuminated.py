
import pandas as pd
from utils import load_csv_dict, load_alternate_map

def load_data():
    operator_lookup = load_csv_dict("NonIlluminatedPushbuttonOperator.csv")
    color_lookup = load_csv_dict("NonIlluminatedPushbuttonButtonColor.csv")
    circuit_lookup = load_csv_dict("Circuit.csv")
    alt_map = load_alternate_map("AlternateCatalogNumbers.csv")
    return operator_lookup, color_lookup, circuit_lookup, alt_map

def decode(catalog_number, operator_lookup, color_lookup, circuit_lookup, alt_map):
    normalized = catalog_number.replace("-", "").strip().upper()
    mapped = alt_map.get(normalized, normalized)
    normalized = mapped.replace("-", "").strip().upper()

    if normalized.startswith("10250T") and len(normalized) > 7:
        code_part = normalized[6:]
        if len(code_part) >= 4:
            operator_code = code_part[:2]
            color_code = code_part[2]
            circuit_code = code_part[3:]

            return {
                 "Operator Type": operator_lookup.get(operator_code, "Unknown Operator Code"),
                "Button Color": color_lookup.get(color_code, "Unknown Color Code"),
                "Circuit Type": circuit_lookup.get(circuit_code, "Unknown Circuit Code"),
                "Operator P/N": f"10250T{operator_code}{color_code}",
                "Contact Block P/N": f"10250T{circuit_code}"
            }
    return None
