import streamlit as st
from modules import non_illuminated, led, incandescent, illuminated_pushpull

# Load all product data
non_illuminated_data = non_illuminated.load_data()
led_data = led.load_data()
incandescent_data = incandescent.load_data()
pushpull_data = illuminated_pushpull.load_data()

# UI
st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "Illuminated Pushbutton (LED)",
    "Illuminated Pushbutton (Incandescent)",
    "Illuminated Push-Pull (Incandescent)"
])

catalog_input = st.text_input("Enter a 10250T catalog number:")

if catalog_input:
    if product_type == "Non-Illuminated Pushbutton":
        operator_lookup, color_lookup, circuit_lookup, alt_map = non_illuminated_data
        result = non_illuminated.decode(catalog_input, operator_lookup, color_lookup, circuit_lookup, alt_map)

    elif product_type == "Illuminated Pushbutton (LED)":
        light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup = led_data
        result = led.decode(catalog_input, light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup)

    elif product_type == "Illuminated Pushbutton (Incandescent)":
        light_unit_lookup, lens_color_lookup, circuit_lookup = incandescent_data
        result = incandescent.decode(catalog_input, light_unit_lookup, lens_color_lookup, circuit_lookup)

    elif product_type == "Illuminated Push-Pull (Incandescent)":
        operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup = pushpull_data
        result = illuminated_pushpull.decode(catalog_input, operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup)

    else:
        result = None

    if result:
        st.markdown("### ✅ Decoded Result")
        for label, value in result["labels"].items():
            st.write(f"**{label}**: {value}")

        st.markdown("### 🧩 Component Part Numbers")
        for label, value in result["parts"].items():
            st.write(f"**{label}**: `{value}`")
    else:
        st.error("Catalog number is invalid or too short to decode.")
