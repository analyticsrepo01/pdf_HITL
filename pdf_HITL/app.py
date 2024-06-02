import streamlit as st
import base64
from io import BytesIO
from PyPDF2 import PdfReader
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models


st.title("PDF Analysis with Gemini Pro")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])


# --- Vertex AI Configuration ---
PROJECT_ID = "my-project-0004-346516"  # Update with your GCP project ID
LOCATION = "us-central1"  # Update with your region (e.g., "us-central1")

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel(
    "gemini-1.5-flash-001",
)

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# --- Functions ---

def extract_text_from_uploaded_pdf(uploaded_file):
    """Extract text from the uploaded PDF."""
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text



def generate_response(text_input):
    """Generate a response from Gemini Pro."""
    document = Part.from_text(text_input)
    responses = model.generate_content(
        [document],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    response_text = ""
    for response in responses:
        response_text += response.text
    return response_text



# --- Main Processing ---

if uploaded_file is not None:
    # Display PDF in the first column (using st.columns)
    col1, col2 = st.columns(2)

    with col1:
        # Display the uploaded PDF
        base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)

    with col2:
        # Analyze the PDF and display the response
        text_input = extract_text_from_uploaded_pdf(uploaded_file)
        with st.spinner("Analyzing PDF..."):
            response = generate_response(text_input)
        st.subheader("Gemini Pro Response:")
        st.write(response)
