import streamlit as st
from utils import load_csv_dict

# Load data
@st.cache_data
def load_data():
    light_unit_lookup = load_csv_dict("IlluminatedPushbuttonLEDLightUnit.csv", value_col="Label")
    lens_color_lookup = load_csv_dict("IlluminatedPushbuttonLEDlensColorProductNumber.csv")
    voltage_lookup = load_csv_dict("IlluminatedPushbuttonLEDVoltage.csv", value_col="Label")
    circuit_lookup = load_csv_dict("Circuit.csv", value_col="Label")
    return light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup

# Decode function
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
            "Contact Block P/N": f"10250T{circuit_code}"
        }
    return None

# App layout
st.set_page_config(page_title="10250T Catalog Decoder", layout="centered")
st.markdown("<h2 style='color:#2c3e50;'>🔍 10250T Illuminated Pushbutton Decoder</h2>", unsafe_allow_html=True)

# Load lookup tables
light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup = load_data()

# Input section
with st.sidebar:
    st.header("🧪 Try It Out")
    catalog_number = st.text_input("Enter Catalog Number", placeholder="e.g. 10250T1234ABCD")
    if st.button("Use Sample"):
        catalog_number = "10250T1234ABCD"

# Decode and display
if catalog_number:
    decoded = decode(catalog_number, light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup)
    if decoded:
        st.markdown("### ✅ Decoded Results")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Light Unit", decoded["Light Unit"])
            st.metric("LED Voltage", decoded["LED Voltage"])
            st.metric("Light Unit P/N", decoded["Light Unit P/N"])
        with col2:
            st.metric("Lens Color", decoded["Lens Color"])
            st.metric("Circuit Type", decoded["Circuit Type"])
            st.metric("Lens P/N", decoded["Lens P/N"])

        with st.expander("📦 Contact Block Details"):
            st.write(f"**Contact Block P/N:** {decoded['Contact Block P/N']}")
    else:
        st.warning("⚠️ Invalid catalog number. Please check the format.")
else:
    st.info("Enter a catalog number in the sidebar to begin decoding.")

# Optional: Custom CSS
st.markdown("""
    <style>
    .stMetric { background-color: #f9f9f9; padding: 10px; border-radius: 8px; }
    .stSidebar { background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)
