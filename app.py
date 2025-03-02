import streamlit as st

# CSS for improved UI with animations and a styled convert button
st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
        .result-box {
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            background: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from {opacity: 0; transform: translateY(-10px);}
            to {opacity: 1; transform: translateY(0);}
        }
        /* Custom styling for the Streamlit button */
        div.stButton > button {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        div.stButton > button:hover {
            background-color: #2980b9;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔄 Unit Converter")

# Conversion data with expanded unit options and modifications as requested
def get_units(conversion_type):
    conversions = {
        "Length": {
            "Meters": 1,
            "Kilometers": 0.001,
            "Centimeters": 100,
            "Yards": 1.09361,
            "Feet": 3.28084,
            "Millimeters": 1000
        },
        "Weight": {
            "Kilograms": 1,
            "Grams": 1000,
            "Pounds": 2.20462,
            "Ounces": 35.274,
            "Tonnes": 0.001
        },
        "Temperature": {
            "Celsius": "C",
            "Fahrenheit": "F",
            "Kelvin": "K"
        },
        "Speed": {
            "Meters per second": 1,
            "Kilometers per hour": 3.6,
            "Miles per hour": 2.23694,
            "Feet per second": 3.28084
        },
        "Volume": {
            "Liters": 1,
            "Milliliters": 1000,
            "Gallons": 0.264172,
            "Cubic Meters": 0.001,
            "Cups": 4.22675
        },
        "Area": {
            "Square Meters": 1,
            "Square Feet": 10.7639,
            "Square Kilometers": 1e-6,
            "Square Centimeters": 10000,
            "Acres": 0.000247105
        },
        "Time": {
            "Seconds": 1,
            "Minutes": 1/60,
            "Hours": 1/3600,
            "Days": 1/86400,
            "Weeks": 1/604800
        },
        "Energy": {
            "Joules": 1,
            "Calories": 0.239006,
            "Kilowatt-hours": 1/3600000,
            "BTU": 1/1055.06,
            "Foot-pounds": 0.737562
        },
        "Data": {
            "Bytes": 1,
            "Kilobytes": 1/1024,
            "Megabytes": 1/(1024**2),
            "Gigabytes": 1/(1024**3),
            "Terabytes": 1/(1024**4)
        }
    }
    return conversions.get(conversion_type, {})

# Conversion logic
def convert_units(value, from_unit, to_unit, conversion_type):
    units = get_units(conversion_type)
    if not units or from_unit not in units or to_unit not in units:
        return None, "Invalid conversion"
    
    if conversion_type == "Temperature":
        if from_unit == "Celsius" and to_unit == "Fahrenheit":
            return value * 9/5 + 32, "(°C × 9/5) + 32"
        elif from_unit == "Celsius" and to_unit == "Kelvin":
            return value + 273.15, "°C + 273.15"
        elif from_unit == "Fahrenheit" and to_unit == "Celsius":
            return (value - 32) * 5/9, "(°F - 32) × 5/9"
        elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15, "(°F - 32) × 5/9 + 273.15"
        elif from_unit == "Kelvin" and to_unit == "Celsius":
            return value - 273.15, "K - 273.15"
        elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32, "(K - 273.15) × 9/5 + 32"
        else:
            return None, "Invalid temperature conversion"
    
    # General unit conversion for non-temperature types
    converted_value = value * (units[to_unit] / units[from_unit])
    formula = f"{value} {from_unit} × ({units[to_unit]} / {units[from_unit]}) = {converted_value} {to_unit}"
    return converted_value, formula

# Streamlit UI
conversion_options = [
    "Length", "Weight", "Temperature", "Speed", "Volume", "Area", "Time", "Energy", "Data"
]
conversion_type = st.sidebar.selectbox("Select Conversion Type", conversion_options)
units = list(get_units(conversion_type).keys())

if units:
    value = st.sidebar.number_input("Enter Value", value=1.0, step=0.1)
    from_unit = st.sidebar.selectbox("From Unit", units)
    to_unit = st.sidebar.selectbox("To Unit", units)

    if st.sidebar.button("Convert"):
        result, formula = convert_units(value, from_unit, to_unit, conversion_type)
        if result is not None:
            st.markdown(
                f"<div class='result-box'>{value} {from_unit} = {result:.2f} {to_unit}</div>",
                unsafe_allow_html=True
            )
            st.write("### Conversion Formula:")
            st.write(formula)
        else:
            st.error("Invalid conversion. Please check your selection.")
else:
    st.error("No valid units found for this conversion type.")
