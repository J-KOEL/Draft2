
import streamlit as st
import incandescent_pushbutton
import led_pushbutton
import non_illuminated
import incandescent_pushpull
import non_illuminated_pushpull
import led_pushpull


st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "LED Pushbutton",
    "Incandescent Pushbutton",
    "Incandescent Push-Pull",
    "Non-Illuminated Push-Pull",
    "LED Push-Pull"
])

catalog_input = st.text_input("Enter a 10250T catalog number:")

if catalog_input:
    if product_type == "Non-Illuminated Pushbutton":
        operator_lookup, color_lookup, circuit_lookup, alt_map = non_illuminated.load_data()
        result = non_illuminated.decode(catalog_input, operator_lookup, color_lookup, circuit_lookup, alt_map)
    elif product_type == "LED Pushbutton":
        light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup = led_pushbutton.load_data()
        result = led_pushbutton.decode(catalog_input, light_unit_lookup, lens_color_lookup, voltage_lookup, circuit_lookup)
    elif product_type == "Incandescent Pushbutton":
        light_unit_lookup, lens_color_lookup, circuit_lookup = incandescent_pushbutton.load_data()
        result = incandescent_pushbutton.decode(catalog_input, light_unit_lookup, lens_color_lookup, circuit_lookup)
    elif product_type == "Incandescent Push-Pull":
        operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup = incandescent_pushpull.load_data()
        result = incandescent_pushpull.decode(catalog_input, operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup)
    elif product_type == "Non-Illuminated Push-Pull":
        operator_lookup, button_lookup, circuit_lookup = non_illuminated_pushpull.load_data()
        result = non_illuminated_pushpull.decode(catalog_input, operator_lookup, button_lookup, circuit_lookup)
    elif product_type == "LED Push-Pull":
        operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup, voltage_lookup = led_pushpull.load_data()
        result = led_pushpull.decode(catalog_input, operator_lookup, light_unit_lookup, lens_lookup, circuit_lookup, voltage_lookup)



    if result:
        st.markdown("### ✅ Decoded Result")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")
    else:
        st.error("Catalog number could not be decoded. Please check the format.")
