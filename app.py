import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load your Google API key from Streamlit secrets
google_api_key = st.secrets["google_api_key"]

# Check if the API key is loaded successfully
if not google_api_key:
    st.error("Google API key not found in Streamlit secrets.")
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

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

# Set the input style
input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae;  // This changes the text color inside the input box
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
[data-testid="stAppViewContainer"] {
    background-color: transparent !important;
}
</style>
"""

# Initialize Streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.markdown(background_image, unsafe_allow_html=True)
st.markdown(input_style, unsafe_allow_html=True)
st.header("Handwriting Analyzer")

# Get input prompt and uploaded image
input_text = st.text_input("Input Prompt:", placeholder="Streamlit CSS")
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
