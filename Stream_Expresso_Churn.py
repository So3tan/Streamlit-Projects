
# Import necessary libraries
import streamlit as st
import pandas as pd
import joblib

# Load the pre-trained model
model = joblib.load(r"C:\Users\braid\Downloads\expressoModel.pkl")  

# Set page layout to wide
st.set_page_config(layout="wide")

# Title and description
st.title('📱 Expresso Client Churn Predictor')
st.write("""
Welcome! This tool estimates how likely a client is to **churn** based on their mobile usage patterns.
Fill in the details on the left, and click **Predict** to see the churn probability.
""")

# Sidebar input section
st.sidebar.header('Client Behavior Inputs')

revenue = st.sidebar.slider('Monthly Revenue (XOF)', min_value=0, max_value=1000000, value=5000, step=500)
data_volume = st.sidebar.slider('Data Volume Used (MB)', min_value=0, max_value=1000000, value=3000, step=500)
on_net = st.sidebar.slider('On-Net Usage (Minutes)', min_value=0, max_value=21000, value=300, step=100)
orange = st.sidebar.slider('Calls to Orange Network (Minutes)', min_value=0, max_value=5000, value=100, step=50)
frequence_rech = st.sidebar.number_input('Recharge Frequency', min_value=1.0, max_value=114.0, value=11.44, step=1.0, help="How often the client recharges.")
frequence = st.sidebar.number_input('Usage Frequency (Days)', min_value=1.0, max_value=91.0, value=13.88, step=1.0)
regularity = st.sidebar.number_input('Days Active in the Month', min_value=0.0, max_value=1346.0, value=7.93, step=1.0)
freq_top_pack = st.sidebar.number_input('Top Pack Usage Frequency', min_value=1.0, max_value=320.0, value=9.20, step=1.0)

# Data structure
input_data = {
    'FREQUENCE_RECH': frequence_rech,
    'REVENUE': revenue,
    'FREQUENCE': frequence,
    'DATA_VOLUME': data_volume,
    'ON_NET': on_net,
    'ORANGE': orange,
    'REGULARITY': regularity,
    'FREQ_TOP_PACK': freq_top_pack
}

input_df = pd.DataFrame([input_data])

# Predict button
if st.button('Predict Churn Probability'):
    prediction = model.predict_proba(input_df)[:, 1]
    churn_probability = round(prediction[0] * 100, 2)

    st.subheader("📈 Prediction Result")
    st.success(f"The estimated probability that this client will churn is **{churn_probability}%**.")

    # Optional message based on risk
    if churn_probability >= 60:
        st.warning("⚠️ High churn risk. You may want to take retention action.")
    elif churn_probability <= 30:
        st.info("✅ Low churn risk. This client appears stable.")
    else:
        st.info("⚖️ Medium churn risk. Monitor this client’s engagement.")

# Input review toggle
if st.checkbox('View Entered Client Data'):
    st.subheader("Input Summary")
    st.dataframe(input_df)
