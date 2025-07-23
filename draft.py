import streamlit as st
import pandas as pd

# Load Non-Illuminated Pushbutton data
@st.cache_data
def load_non_illuminated_data():
    operator_df = pd.read_csv("NonIlluminatedPushbuttonOperator 5.csv")
    color_df = pd.read_csv("NonIlluminatedPushbuttonButtonColor 5.csv")
    circuit_df = pd.read_csv("Circuit 17.csv")
    alt_df = pd.read_csv("AlternateCatalogNumbers 2.csv")

    operator_dict = {str(v).strip(): str(k).strip() for k, v in zip(operator_df['Label'], operator_df['Code'])}
    color_dict = {str(v).strip(): str(k).strip() for k, v in zip(color_df['Label'], color_df['Code'])}
    circuit_dict = {str(v).strip(): str(k).strip() for k, v in zip(circuit_df['Label'], circuit_df['Code'])}

    operator_code_to_label = {v: k for k, v in operator_dict.items()}
    color_code_to_label = {v: k for k, v in color_dict.items()}
    circuit_code_to_label = {v: k for k, v in circuit_dict.items()}

    alt_map = {str(row['Alternate']).strip().upper(): str(row['Standard']).strip().upper()
               for _, row in alt_df.iterrows()}

    return operator_code_to_label, color_code_to_label, circuit_code_to_label, alt_map

# Load LED Pushbutton data
@st.cache_data
def load_led_data():
    light_unit_df = pd.read_csv("IlluminatedPushbuttonLEDLightUnit 8.csv", skiprows=1)
    lens_color_df = pd.read_csv("IlluminatedPushbuttonLEDLensColor 8.csv")
    voltage_df = pd.read_csv("IlluminatedPushbuttonLEDVoltage 9.csv")
    circuit_df = pd.read_csv("Circuit 16.csv")

    light_unit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in light_unit_df.iterrows()}
    lens_color_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in lens_color_df.iterrows()}
    voltage_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in voltage_df.iterrows()}
    circuit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in circuit_df.iterrows()}

    return light_unit_dict, lens_color_dict, voltage_dict, circuit_dict

# Load Incandescent Pushbutton data
@st.cache_data
def load_incandescent_data():
    light_unit_df = pd.read_csv("IlluminatedPushbuttonIncandescentLightUnit 6.csv")
    lens_color_df = pd.read_csv("illuminatedPushbuttonIncandescentLensColor 6.csv")
    circuit_df = pd.read_csv("Circuit 15.csv")

    light_unit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in light_unit_df.iterrows()}
    lens_color_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in lens_color_df.iterrows()}
    circuit_dict = {str(row['Code']).strip(): str(row['Label']).strip() for _, row in circuit_df.iterrows()}

    return light_unit_dict, lens_color_dict, circuit_dict

# Load all data
non_illuminated_data = load_non_illuminated_data()
led_data = load_led_data()
incandescent_data = load_incandescent_data()

# UI
st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "Illuminated Pushbutton (LED)",
    "Illuminated Pushbutton (Incandescent)"
])

catalog_input = st.text_input("Enter a 10250T catalog number:")

if catalog_input:
    normalized = catalog_input.replace("-", "").strip().upper()

    if product_type == "Non-Illuminated Pushbutton":
        operator_lookup, color_lookup, circuit_lookup, alt_map = non_illuminated_data
        mapped = alt_map.get(normalized, normalized)
        if mapped != normalized:
            st.info(f"Alternate catalog number detected. Decoding as: `{mapped}`")
        normalized = mapped.replace("-", "").strip().upper()

        if normalized.startswith("10250T") and len(normalized) > 7:
            code_part = normalized[6:]
            if len(code_part) >= 4:
                operator_code = code_part[:2]
                color_code = code_part[2]
                circuit_code = code_part[3:]

                operator_label = operator_lookup.get(operator_code, "Unknown Operator Code")
                color_label = color_lookup.get(color_code, "Unknown Color Code")
                circuit_label = circuit_lookup.get(circuit_code, "Unknown Circuit Code")

                operator_pn = f"10250T{operator_code}{color_code}"
                contact_block_pn = f"10250T{circuit_code}"

                st.markdown("### ✅ Decoded Result")
                st.write(f"**Operator Type**: {operator_label}")
                st.write(f"**Button Color**: {color_label}")
                st.write(f"**Circuit Type**: {circuit_label}")

                st.markdown("### 🧩 Component Part Numbers")
                st.write(f"**Operator P/N**: `{operator_pn}`")
                st.write(f"**Contact Block P/N**: `{contact_block_pn}`")
            else:
                st.error("Catalog number is too short to decode.")
        else:
            st.error("Catalog number must start with '10250T'.")

    elif product_type == "Illuminated Pushbutton (LED)":
        light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup = led_data
        if normalized.startswith("10250T") and len(normalized) > 10:
            code_part = normalized[6:]
            light_unit_code = code_part[:4]
            lens_color_code = code_part[4:6]
            voltage_code = code_part[6:8]
            circuit_code = code_part[8:]

            light_unit_label = light_unit_lookup.get(light_unit_code, "Unknown Light Unit")
            lens_color_label = lens_color_lookup.get(lens_color_code, "Unknown Lens Color")
            voltage_label = voltage_lookup.get(voltage_code, "Unknown LED Voltage")
            circuit_label = circuit_lookup.get(circuit_code, "Unknown Circuit Type")

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
            st.error("Catalog number must start with '10250T' and be long enough to decode.")

    elif product_type == "Illuminated Pushbutton (Incandescent)":
        light_unit_lookup, lens_color_lookup, circuit_lookup = incandescent_data
        if normalized.startswith("10250T") and len(normalized) > 9:
            code_part = normalized[6:]
            light_unit_code = code_part[:3]
            lens_color_code = code_part[3:6]
            circuit_code = code_part[6:]

            light_unit_label = light_unit_lookup.get(light_unit_code, "Unknown Light Unit")
            lens_color_label = lens_color_lookup.get(lens_color_code, "Unknown Lens Color")
            circuit_label = circuit_lookup.get(circuit_code, "Unknown Circuit Type")

            st.markdown("### ✅ Decoded Result")
            st.write(f"**Light Unit**: {light_unit_label}")
            st.write(f"**Lens Color**: {lens_color_label}")
            st.write(f"**Circuit Type**: {circuit_label}")

            st.markdown("### 🧩 Component Part Numbers")
            st.write(f"**Light Unit P/N**: `10250T{light_unit_code}`")
            st.write(f"**Lens P/N**: `{lens_color_code}`")
            st.write(f"**Contact Block P/N**: `10250T{circuit_code}`")
        else:
            st.error("Catalog number must start with '10250T' and be long enough to decode.")

