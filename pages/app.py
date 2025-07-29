import streamlit as st
import incandescent_pushbutton
import led_pushbutton
import non_illuminated
import incandescent_pushpull
import non_illuminated_pushpull
import led_pushpull
import standard_indicating_incandescent
import standard_indicating_led
import presttest_incandescent
import presttest_led  # ✅ New
import mastertest_incandescent  # ✅ New

st.title("🔍 10250T Catalog Number Decoder")

product_type = st.selectbox("Select product type:", [
    "Non-Illuminated Pushbutton",
    "LED Pushbutton",
    "Incandescent Pushbutton",
    "Incandescent Push-Pull",
    "Non-Illuminated Push-Pull",
    "LED Push-Pull",
    "Standard Indicating Light Incandescent",
    "Standard Indicating Light LED",
    "PresTest Incandescent",
    "PresTest LED",
    "Master Test Incandescent"  # ✅ New
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
    elif product_type == "Standard Indicating Light Incandescent":
        light_unit_lookup, lens_lookup = standard_indicating_incandescent.load_data()
        result = standard_indicating_incandescent.decode(catalog_input, light_unit_lookup, lens_lookup)
    elif product_type == "Standard Indicating Light LED":
        light_unit_lookup, lens_lookup, voltage_lookup = standard_indicating_led.load_data()
        result = standard_indicating_led.decode(catalog_input, light_unit_lookup, lens_lookup, voltage_lookup)
    elif product_type == "PresTest Incandescent":
        light_unit_lookup, lens_lookup = presttest_incandescent.load_data()
        result = presttest_incandescent.decode(catalog_input, light_unit_lookup, lens_lookup)
    elif product_type == "PresTest LED":
        light_unit_lookup, lens_lookup, voltage_lookup = presttest_led.load_data()
        result = presttest_led.decode(catalog_input, light_unit_lookup, lens_lookup, voltage_lookup)
    elif product_type == "Master Test Incandescent":
        light_unit_lookup, lens_lookup = mastertest_incandescent.load_data()
        result = mastertest_incandescent.decode(catalog_input, light_unit_lookup, lens_lookup)

    if result:
        st.markdown("### ✅ Decoded Result")
        for key, value in result.items():
            st.write(f"**{key}**: {value}")
    else:
        st.error("Catalog number could not be decoded. Please check the format.")
