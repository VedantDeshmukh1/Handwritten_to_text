import streamlit as st
from PIL import Image
import google.generativeai as genai
from streamlit_secrets import get_secret

# Load your Google API key from secrets
google_api_key = st.secrets["google_api_key"]

# Check if the API key is loaded successfully
if not google_api_key:
    st.error("Google API key not found in secrets.")
    st.stop()  # Stop further execution if API key is missing

# Configure Google GenerativeAI with your API key
genai.configure(api_key=google_api_key)

# Function to get Gemini response
def get_gemini_response(input_text, image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input_text != "":
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(image)
    return response.text

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Handwriting Analyzer")

# Get input prompt and uploaded image
input_text = st.text_input("Input Prompt:")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "pdf"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to trigger Gemini response generation
submit_button = st.button("Tell me about the image")

# Process Gemini response on button click
if submit_button:
    if image is not None:
        response_text = get_gemini_response(input_text, image)
        st.subheader("Response:")
        st.write(response_text)
    else:
        st.warning("Please upload an image before submitting.")
