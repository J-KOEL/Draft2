
import streamlit as st
import incandescent_pushbutton
import led_pushbutton
import non_illuminated



st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "Illuminated Pushbutton (LED)",
    "Illuminated Pushbutton (Incandescent)"
])

catalog_input = st.text_input("Enter a 10250T catalog number:")

if catalog_input:
    if product_type == "Non-Illuminated Pushbutton":
        operator_lookup, color_lookup, circuit_lookup, alt_map = non_illuminated.load_data()
        result = non_illuminated.decode(catalog_input, operator_lookup, color_lookup, circuit_lookup, alt_map)
    elif product_type == "Illuminated Pushbutton (LED)":
        light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup = led.load_data()
        result = led.decode(catalog_input, light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup)
    elif product_type == "Illuminated Pushbutton (Incandescent)":
        light_unit_lookup, lens_color_lookup, circuit_lookup = incandescent.load_data()
        result = incandescent.decode(catalog_input, light_unit_lookup, lens_color_lookup, circuit_lookup)

    if result:
        st.markdown("### ✅ Decoded Result")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")
    else:
        st.error("Catalog number could not be decoded. Please check the format.")
