import streamlit as st
import pandas as pd

@st.cache_data
def load_all_data():
    # Load Non-Illuminated mappings
    try:
        operator_df = pd.read_csv("NonIlluminatedPushbuttonOperator.csv", header=None)
        color_df = pd.read_csv("NonIlluminatedPushbuttonButtonColor.csv", header=None)
        circuit_df = pd.read_csv("NonIlluminatedPushbuttonCircuit.csv", header=None)
        alt_df = pd.read_csv("AlternateCatalogNumbers.csv")
        operator_dict = {str(v).strip(): str(k).strip() for k, v in zip(operator_df.iloc[:, 1], operator_df.iloc[:, 0])}
        color_dict = {str(v).strip(): str(k).strip() for k, v in zip(color_df.iloc[:, 1], color_df.iloc[:, 0])}
        circuit_dict = {str(v).strip(): str(k).strip() for k, v in zip(circuit_df.iloc[:, 1], circuit_df.iloc[:, 0])}
        operator_code_to_label = {v: k for k, v in operator_dict.items()}
        color_code_to_label = {v: k for k, v in color_dict.items()}
        circuit_code_to_label = {v: k for k, v in circuit_dict.items()}
        alt_map = {str(row['Alternate']).strip().upper(): str(row['Standard']).strip().upper()
                   for _, row in alt_df.iterrows()}
    except:
        operator_code_to_label = {}
        color_code_to_label = {}
        circuit_code_to_label = {}
        alt_map = {}

    # Load LED mappings
    led_light_unit_df = pd.read_csv("IlluminatedPushbuttonLEDLightUnit.csv", skiprows=1)
    led_lens_color_df = pd.read_csv("IlluminatedPushbuttonLEDLensColor.csv")
    led_voltage_df = pd.read_csv("IlluminatedPushbuttonLEDVoltage.csv")
    led_circuit_df = pd.read_csv("Circuit.csv")

    led_light_unit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_light_unit_df.iterrows()}
    led_lens_color_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_lens_color_df.iterrows()}
    led_voltage_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_voltage_df.iterrows()}
    led_circuit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in led_circuit_df.iterrows()}

    # Load Incandescent mappings
    inc_light_unit_df = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit.csv")
    inc_lens_color_df = pd.read_csv("illuminatedPushbuttonIncandescentLensColor.csv")
    inc_circuit_df = pd.read_csv("Circuit 15.csv")

    inc_light_unit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in inc_light_unit_df.iterrows()}
    inc_lens_color_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in inc_lens_color_df.iterrows()}
    inc_circuit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in inc_circuit_df.iterrows()}

    return {
        "non_illuminated": {
            "operator": operator_code_to_label,
            "color": color_code_to_label,
            "circuit": circuit_code_to_label,
            "alt_map": alt_map
        },
        "led": {
            "light_unit": led_light_unit_dict,
            "lens_color": led_lens_color_dict,
            "voltage": led_voltage_dict,
            "circuit": led_circuit_dict
        },
        "incandescent": {
            "light_unit": inc_light_unit_dict,
            "lens_color": inc_lens_color_dict,
            "circuit": inc_circuit_dict
        }
    }

data = load_all_data()

st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "Illuminated Pushbutton (LED)",
    "Illuminated Pushbutton (Incandescent)"
])

catalog_input = st.text_input("Enter a 10250T catalog number:")

if catalog_input:
    normalized = catalog_input.replace("-", "").strip().upper()

    if not normalized.startswith("10250T"):
        st.error("Catalog number must start with '10250T'.")
    else:
        code_part = normalized[6:]

        if product_type == "Non-Illuminated Pushbutton":
            alt_map = data["non_illuminated"]["alt_map"]
            mapped = alt_map.get(normalized, normalized)
            if mapped != normalized:
                st.info(f"Alternate catalog number detected. Decoding as: `{mapped}`")
            code_part = mapped[6:]
            if len(code_part) >= 4:
                operator_code = code_part[:2]
                color_code = code_part[2]
                circuit_code = code_part[3:]

                operator_label = data["non_illuminated"]["operator"].get(operator_code, "Unknown Operator Code")
                color_label = data["non_illuminated"]["color"].get(color_code, "Unknown Color Code")
                circuit_label = data["non_illuminated"]["circuit"].get(circuit_code, "Unknown Circuit Code")

                st.markdown("### ✅ Decoded Result")
                st.write(f"**Operator Type**: {operator_label}")
                st.write(f"**Button Color**: {color_label}")
                st.write(f"**Circuit Type**: {circuit_label}")

                st.markdown("### 🧩 Component Part Numbers")
                st.write(f"**Operator P/N**: `10250T{operator_code}{color_code}`")
                st.write(f"**Contact Block P/N**: `10250T{circuit_code}`")
            else:
                st.error("Catalog number is too short to decode.")

        elif product_type == "Illuminated Pushbutton (LED)":
            if len(code_part) >= 10:
                light_unit_code = code_part[:4]
                lens_color_code = code_part[4:6]
                voltage_code = code_part[6:8]
                circuit_code = code_part[8:]

                light_unit_label = data["led"]["light_unit"].get(light_unit_code, "Unknown Light Unit")
                lens_color_label = data["led"]["lens_color"].get(lens_color_code, "Unknown Lens Color")
                voltage_label = data["led"]["voltage"].get(voltage_code, "Unknown LED Voltage")
                circuit_label = data["led"]["circuit"].get(circuit_code, "Unknown Circuit Type")

                st.markdown("### ✅ Decoded Result")
                st.write(f"**Light Unit**: {light_unit_label}")
                st.write(f"**Lens Color**: {lens_color_label}")
                st.write(f"**LED Voltage**: {voltage_label}")
                st.write(f"**Circuit Type**: {circuit_label}")

                st.markdown("### 🧩 Component Part Numbers")
                st.write(f"**Light Unit P/N**: `10250T{light_unit_code}`")
                st.write(f"**Lens P/N**: `{lens_color_code}`")
                st.write(f"**Voltage Code**: `{voltage_code}`")
                st.write(f"**Contact Block P/N**: `10250T{circuit_code}`")
            else:
                st.error("Catalog number is too short to decode.")

        elif product_type == "Illuminated Pushbutton (Incandescent)":
            if len(code_part) >= 7:
                light_unit_code = code_part[:3]
                lens_color_code = code_part[3:6]
                circuit_code = code_part[6:]

                light_unit_label = data["incandescent"]["light_unit"].get(light_unit_code, "Unknown Light Unit")
                lens_color_label = data["incandescent"]["lens_color"].get(lens_color_code, "Unknown Lens Color")
                circuit_label = data["incandescent"]["circuit"].get(circuit_code, "Unknown Circuit Type")

                st.markdown("### ✅ Decoded Result")
                st.write(f"**Light Unit**: {light_unit_label}")
                st.write(f"**Lens Color**: {lens_color_label}")
                st.write(f"**Circuit Type**: {circuit_label}")

                st.markdown("### 🧩 Component Part Numbers")
                st.write(f"**Light Unit P/N**: `10250T{light_unit_code}`")
                st.write(f"**Lens P/N**: `{lens_color_code}`")
                st.write(f"**Contact Block P/N**: `10250T{circuit_code}`")
            else:
                st.error("Catalog number is too short to decode.")

