import streamlit as st
import base64
from io import BytesIO
from PyPDF2 import PdfReader
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
st.set_page_config(layout="wide")  # Add this line at the beginning

# pip install streamlit-quill
# from streamlit_quill import st_quill
from streamlit_ace import st_ace

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

prompt = """
You are a document entity extraction specialist. Given a document, your task is to extract the text value

- The JSON schema must be followed during the extraction.
- The values must only include text found in the document
- Do not normalize any entity value.
- If an entity is not found in the document, set the entity value to null.
"""

# Initialize text1 with a default value
if 'text1' not in st.session_state:
    st.session_state.text1 = """You are a document extraction engine.
The user will provide a pdf file or an image. Your task is to convert it into markdown format.
Do not leave any text behind."""

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
        [st.session_state.text1, document],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    response_text = ""
    for response in responses:
        response_text += response.text
    return response_text

def summarize_text(text_input, max_length=500):
    """Summarizes the text using Gemini Pro."""
    document = Part.from_text(text_input)
    summary_prompt = "Please summarize the following text:"
    responses = model.generate_content(
        [summary_prompt, document],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    summary_text = ""
    for response in responses:
        summary_text += response.text
    return summary_text[:max_length]  # Limit to max_length characters


# --- CSS
# Custom CSS to expand central elements
st.markdown("""
<style>
.stApp {
    max-width: 95%;  /* Adjust to your desired percentage */
    margin: 0 auto;  /* Center the app horizontally */
}
.stContainer {  
    max-width: 100%; 
}
.stColumn {
    padding: 0 10px;  /* Reduce padding between columns */
}
.stText {
    width: 100%; 
}
</style>
""", unsafe_allow_html=True)

# --- Main Processing ---

import streamlit as st
import base64
from io import BytesIO
from PyPDF2 import PdfReader
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
# Import for text file saving
# from google.colab import files

# --- Main Processing ---

if uploaded_file is not None:
    col1, col2 = st.columns([1, 2])  

    with col1:
        with st.container():
            # Input field for text1
            st.subheader("Edit the extraction prompt:")
            st.session_state.text1 = st.text_area(label="", value=st.session_state.text1, height=150)
            
            # Display the uploaded PDF
            st.subheader("Preview of PDF:")            
            base64_pdf = base64.b64encode(uploaded_file.read()).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            summarize = st.checkbox("Summarize output with Gemini Pro")

    with col2:
        # Analyze the PDF and display the response
        text_input = extract_text_from_uploaded_pdf(uploaded_file)
        if text_input:
            with st.spinner("Analyzing PDF..."):
                response = generate_response(text_input)

            with st.expander("Gemini Pro Response:", expanded=True):
                # edited_response = st_quill(value=response,toolbar=True, readonly=False, html=True)
                edited_response = st_ace(value=response, language="markdown")  # Use Markdown mode
                # edited_response = st.text_area(label="", value=response, height=300)
            # ... (Save button logic - unchanged)
            # Save button

            
            if st.button("Save Response to Text File"):
                try:
                    text_file = open("gemini_response.txt", "w")
                    text_file.write(edited_response)
                    text_file.close()
                    
                    # Download the file using Google Colab files module
                    # files.download("gemini_response.txt")

                    st.success("Response saved successfully!")
                except Exception as e:
                    st.error(f"Error saving file: {e}")                
            if st.button("Save big query"):
                try:
                    text_file = open("gemini_response.txt", "w")
                    text_file.write(edited_response)
                    text_file.close()
                    
                    # Download the file using Google Colab files module
                    # files.download("gemini_response.txt")

                    st.success("Make sure to add your BQ connection config, if already added -  file is saved to BQ")
                except Exception as e:
                    st.error(f"Error saving file to BQ: {e}")

            # Summarize output
            if summarize:
                with st.spinner("Summarizing PDF..."):
                    text_input = summarize_text(text_input)
                st.subheader("Summarized Text:")
                st.write(text_input)                    
        else:
            st.warning("Unable to analyze. Please check the PDF or try again.")