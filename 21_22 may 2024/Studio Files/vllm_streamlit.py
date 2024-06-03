import streamlit as st
import fitz  # PyMuPDF
import wikipedia
import litellm

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to get text from Wikipedia
def get_wikipedia_text(topic):
    try:
        page = wikipedia.page(topic)
        return page.content
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation error. Options: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Page not found."

# Function to generate response using LiteLLM
def generate_llm_response(input_text, api_base, api_key, prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": input_text+" "+ "for above text  "+prompt}
    ]
    
    response = litellm.completion(
        model="openai/meta-llama/Meta-Llama-3-8B-Instruct",
        messages=messages,
        api_key=api_key,
        api_base=api_base,
        temperature=0.2,
        max_tokens=80
    )
    
    return response['choices'][0]['message']['content']

# Set Streamlit page configuration for wide layout
st.set_page_config(layout="wide")

# Set up the Streamlit app
st.title('LLAMA 3 8B  Streamlit App')

c1,_, c2 = st.columns([1,0.2,1])
with c1:
    api_base = st.text_input('Enter the custom API base URL for LiteLLM')

with c2:
    api_key = st.text_input('Enter your API key:', type='password')

# Create two columns
col1,_, col2 = st.columns([1,0.2,1])

with col1:
    st.header('Input')
    input_type = st.radio('Select input type:', ('PDF', 'Wikipedia'),horizontal=True)

    if input_type == 'PDF':
        uploaded_file = st.file_uploader('Upload a PDF file', type='pdf')
        if uploaded_file is not None:
            input_text = extract_text_from_pdf(uploaded_file)
            st.text_area('Extracted Text:', input_text, height=300, placeholder='The extracted text from your PDF will appear here.')
    elif input_type == 'Wikipedia':
        topic = st.text_input('Enter Wikipedia topic:')
        if topic:
            input_text = get_wikipedia_text(topic)
            st.text_area('Wikipedia Text:', input_text, height=300, placeholder='The text from the Wikipedia page will appear here.')

with col2:
    
    if 'input_text' in locals() and input_text:
        prompt = st.text_area('Enter your prompt here:', '', height=100, placeholder='Enter the prompt for the LiteLLM model here.')
        if st.button('Generate LLM OUTPUT'):
            # Generate and display the response
            response = generate_llm_response(input_text, api_base, api_key, prompt)
            st.write('Response:')
            st.write(response)
