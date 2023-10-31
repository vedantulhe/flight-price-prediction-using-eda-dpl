import streamlit as st
import pandas as pd
import pickle
import base64

# Load the trained model
model = pickle.load(open("flight_rf.pkl", "rb"))
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    backdrop-filter: blur(1000px);
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background(r'C:\Users\HP\Downloads\IMAGE FILTERING PROJECT\download.jpeg')


# Function to make predictions
def predict_price(Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min,
                  Arrival_hour, Arrival_min, dur_hour, dur_min, Air_India, GoAir,
                  IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers,
                  Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara,
                  Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai,
                  d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi):
    prediction = model.predict([[
        Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min, Arrival_hour, Arrival_min,
        dur_hour, dur_min, Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business,
        Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara,
        Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai, d_Cochin, d_Delhi,
        d_Hyderabad, d_Kolkata, d_New_Delhi
    ]])
    return round(prediction[0], 2)

st.title("Flight Price Prediction")

# Date of Journey
st.sidebar.subheader("Date of Journey")
date_dep = st.sidebar.date_input("Departure Date", pd.to_datetime('2023-10-23'))
Journey_day = date_dep.day
Journey_month = date_dep.month

# Departure Time
st.sidebar.subheader("Departure Time")
Dep_hour = st.sidebar.slider("Hour", 0, 23, 7)
Dep_min = st.sidebar.slider("Minutes", 0, 59, 30)

# Arrival Time
st.sidebar.subheader("Arrival Time")
Arrival_hour = st.sidebar.slider("Hour", 0, 23, 10)
Arrival_min = st.sidebar.slider("Minutes", 0, 59, 45)

# Duration
st.sidebar.subheader("Duration")
dur_hour = abs(Arrival_hour - Dep_hour)
dur_min = abs(Arrival_min - Dep_min)

# Total Stops
st.sidebar.subheader("Total Stops")
Total_stops = st.sidebar.selectbox("Select the total stops", ["0", "1", "2", "3", "4"])

# Airline
st.sidebar.subheader("Airline")
airline = st.sidebar.selectbox("Select the airline", [
    "Jet Airways",
    "IndiGo",
    "Air India",
    "Multiple carriers",
    "SpiceJet",
    "Vistara",
    "GoAir",
    "Multiple carriers Premium economy",
    "Jet Airways Business",
    "Vistara Premium economy",
    "Trujet"
])

# Source
st.sidebar.subheader("Source")
Source = st.sidebar.selectbox("Select the source", ["Delhi", "Kolkata", "Mumbai", "Chennai"])

# Destination
st.sidebar.subheader("Destination")
Destination = st.sidebar.selectbox("Select the destination", ["Cochin", "Delhi", "New Delhi", "Hyderabad", "Kolkata"])

# Encoding for Airline, Source, and Destination
# (Use one-hot encoding or similar technique as needed)
Airline_dict = {
    "Jet Airways": 1,
    "IndiGo": 0,
    "Air India": 0,
    "Multiple carriers": 0,
    "SpiceJet": 0,
    "Vistara": 0,
    "GoAir": 0,
    "Multiple carriers Premium economy": 0,
    "Jet Airways Business": 0,
    "Vistara Premium economy": 0,
    "Trujet": 0
}

Source_dict = {
    "Delhi": 1,
    "Kolkata": 0,
    "Mumbai": 0,
    "Chennai": 0
}

Destination_dict = {
    "Cochin": 1,
    "Delhi": 0,
    "New Delhi": 0,
    "Hyderabad": 0,
    "Kolkata": 0
}

# Calculate encoded values
Air_India = Airline_dict.get(airline, 0)
GoAir = Airline_dict.get(airline, 0)
IndiGo = Airline_dict.get(airline, 0)
Jet_Airways = Airline_dict.get(airline, 0)
Jet_Airways_Business = Airline_dict.get(airline, 0)
Multiple_carriers = Airline_dict.get(airline, 0)
Multiple_carriers_Premium_economy = Airline_dict.get(airline, 0)
SpiceJet = Airline_dict.get(airline, 0)
Trujet = Airline_dict.get(airline, 0)
Vistara = Airline_dict.get(airline, 0)
Vistara_Premium_economy = Airline_dict.get(airline, 0)

s_Delhi = Source_dict.get(Source, 0)
s_Kolkata = Source_dict.get(Source, 0)
s_Mumbai = Source_dict.get(Source, 0)
s_Chennai = Source_dict.get(Source, 0)

d_Cochin = Destination_dict.get(Destination, 0)
d_Delhi = Destination_dict.get(Destination, 0)
d_New_Delhi = Destination_dict.get(Destination, 0)
d_Hyderabad = Destination_dict.get(Destination, 0)
d_Kolkata = Destination_dict.get(Destination, 0)

if st.sidebar.button("Predict Price"):
    prediction = predict_price(Total_stops, Journey_day, Journey_month, Dep_hour, Dep_min,
                                Arrival_hour, Arrival_min, dur_hour, dur_min, Air_India, GoAir,
                                IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers,
                                Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara,
                                Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai,
                                d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi)
    st.write("Your Flight price is Rs.", prediction)



