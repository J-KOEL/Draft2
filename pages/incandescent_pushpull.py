
from utils import load_csv_dict

def load_data():
  operator_lookup = load_csv_dict("PushPullOperator.csv")
  light_unit_lookup = load_csv_dict("IlluminatedPushPullIncandescentLightUnit.csv")
  lens_color_lookup = load_csv_dict("IlluminatedPushPullIncandescentLens.csv")
  circuit_lookup = load_csv_dict("Circuit.csv")
  return operator_lookup, light_unit_lookup, lens_color_lookup, circuit_lookup

def decode(catalog_number, operator_lookup, light_unit_lookup, lens_color_lookup, circuit_lookup):
  normailized = calalog_number.replace("-", "").strip().upper()
  if normalized.startswith("10250T") and len(normalized) > 9:
      code_part = normalized[6:]
      operator_code = code_part [:1]
      light_unit_code = code part [1:3]
      lens_color_code = code part [3:5]
      circuit_code = code part [5:]

      return {
          "operator": operator_lookup.get(operator_code, "Unknown Operator"),
          "Light Unit": light_unit_lookup.get(light_unit_code, "Unknown Light Unit"),
          "Lens Color": lens_color_lookup.get(lens_color_code, "Unknown Lens Color"),
          "Circuit Type": circuit_lookup.get(circuit_code, "Unknown Circuit Type"),
          "Light Unit P/N": f"10250T{light_unit_code}",
          "Lens P/N": lens_color_code,
          "Voltage Code": voltage_code,
          "Contact Block P/N": f"10250T{circuit_code}"
      }
    return None
