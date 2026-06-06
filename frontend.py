import streamlit as st
import requests

# =========================
# Configuration
# =========================
BACKEND_URL = "https://insurance-fastapi-btgo.onrender.com"
API_URL = f"{BACKEND_URL}/predict"

# =========================
# Page Setup
# =========================
st.set_page_config(
    page_title="Insurance Premium Category Predictor",
    page_icon="🏥",
    layout="centered"
)

st.title("🏥 Insurance Premium Category Predictor")

st.info(
    "💡 This application uses a cloud-hosted machine learning model. "
    "If the service has been inactive, the first prediction may take a little longer while the backend wakes up."
)

# =========================
# API Health Check
# =========================
try:
    health_response = requests.get(
        f"{BACKEND_URL}/health",
        timeout=3
    )

    if health_response.status_code == 200:
        health_data = health_response.json()

        st.success(
            f"🟢 API Online | "
            f"Model Version: {health_data.get('Version', 'Unknown')}"
        )

except Exception:
    st.warning(
        "🟡 Prediction service is waking up. "
        "The first request may take 30–60 seconds."
    )

# =========================
# User Inputs
# =========================
st.markdown("### Enter Your Details")

age = st.number_input(
    "Age",
    min_value=1,
    max_value=119,
    value=30
)

weight = st.number_input(
    "Weight (kg)",
    min_value=1.0,
    value=65.0
)

height = st.number_input(
    "Height (m)",
    min_value=0.5,
    max_value=2.5,
    value=1.7
)

income_lpa = st.number_input(
    "Annual Income (LPA)",
    min_value=0.1,
    value=10.0
)

smoker = st.selectbox(
    "Are you a smoker?",
    [True, False]
)

city = st.text_input(
    "City",
    value="Mumbai"
)

occupation = st.selectbox(
    "Occupation",
    [
        "retired",
        "freelancer",
        "student",
        "government_job",
        "business_owner",
        "unemployed",
        "private_job"
    ]
)

# =========================
# Prediction
# =========================
if st.button(
    "Predict Premium Category",
    use_container_width=True
):

    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    try:

        with st.spinner(
            "🚀 Generating prediction... "
            "If the backend is asleep, it may take up to a minute to wake up."
        ):

            response = requests.post(
                API_URL,
                json=input_data,
                timeout=120
            )

        if response.status_code == 200:

            result = response.json()

            st.success(
                f"Predicted Insurance Premium Category: "
                f"**{result['predicted_output']}**"
            )

            if "confidence" in result:
                st.metric(
                    "Confidence",
                    f"{result['confidence']:.2%}"
                    if isinstance(result["confidence"], float)
                    else result["confidence"]
                )

            if "class_probabilities" in result:
                st.subheader("Class Probabilities")
                st.json(result["class_probabilities"])

        else:

            st.error(
                f"Prediction failed (Status Code: {response.status_code})"
            )

            try:
                st.json(response.json())
            except:
                st.write(response.text)

    except requests.exceptions.Timeout:

        st.error(
            "⏱️ The backend is taking longer than expected to respond. "
            "Please try again in a few moments."
        )

    except requests.exceptions.ConnectionError:

        st.error(
            "🔌 Unable to connect to the prediction service. "
            "The backend may still be starting up."
        )

    except Exception as e:

        st.error(
            f"Unexpected error: {str(e)}"
        )