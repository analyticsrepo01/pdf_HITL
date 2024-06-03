**PDF Extraction and Analysis Tool with Gemini Pro**

This Streamlit application allows users to upload PDF documents, extract their text content, and analyze it using Google's Gemini Pro large language model. The app provides a human-in-the-loop interface to edit the extracted text or its summary, and then save the output as a text file.

**Features**

*   **PDF Upload:**  Easily upload PDF files for analysis.
*   **Text Extraction:** Extracts text content from the uploaded PDF.
*   **Gemini Pro Integration:** Leverages Gemini Pro to analyze and process the extracted text based on a customizable prompt.
*   **Editable Output:**  Displays the Gemini Pro output in an editable Markdown editor (Streamlit-ACE).
*   **Summarization (Optional):** Optionally summarizes the PDF content before sending it to Gemini Pro for analysis.
*   **Save Output:**  Save the edited text to a `.txt` file.

**Getting Started**

1.  **Prerequisites:**
    *   **Python:** Ensure Python is installed on your system.
    *   **Streamlit:** Install Streamlit: `pip install streamlit`
    *   **Vertex AI:** Set up your Google Cloud project and Vertex AI credentials. Install the necessary libraries: `pip install google-cloud-aiplatform vertexai streamlit-ace PyPDF2`

2.  **Configuration:**
    *   Update the `PROJECT_ID` and `LOCATION` variables in the code with your Google Cloud project ID and location.
    *   Obtain access to the Gemini Pro model (`gemini-1.5-flash-001`) through Vertex AI.

3.  **Run the App:**
    *   Save the code as a Python file (e.g., `bpp_test.py`).
    *   Execute the following command in your terminal:
        ```bash
        streamlit run bpp_test.py
        ```
    *   The app will open in your web browser.

**Usage**

1.  **Upload a PDF:** Click the "Upload PDF" button and select your PDF document.
2.  **Modify Prompt (Optional):** You can optionally modify the prompt that guides Gemini Pro's analysis by editing the text in the first text area.
3.  **Analyze PDF:** The app will automatically extract text from the PDF and process it using Gemini Pro.
4.  **Edit and Save:**
    *   The extracted and processed text is displayed in an editable markdown editor.
    *   Make any necessary changes to the text.
    *   Click the "Save Response to Text File" button to save the edited text.
    *   Click the "Summarize Output" button to see the summary of the document.
    
**Note:** The "Save to BigQuery" button is a placeholder. You'll need to implement the actual BigQuery integration if you want to use it.

**Advanced Options**

- You can enable text summarization before analysis using the "Summarize output with Gemini Pro" checkbox.

**Disclaimer**

This app is provided as-is and is intended for demonstration and learning purposes. Use at your own risk.