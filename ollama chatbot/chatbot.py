import streamlit as st
from langchain_ollama import ChatOllama

# pip install -qU langchain-ollama
# pip install langchain

st.title("🧠 MediSense HealthMate")

# Form for text input and document upload
with st.form("llm-form"):
    text = st.text_area("Enter your question or statement:")
    uploaded_file = st.file_uploader("Upload a document (Optional):", type=["txt", "pdf", "docx"])
    submit = st.form_submit_button("Submit")

def generate_response(input_text, document_content=None):
    model = ChatOllama(model="llama3.2:1b", base_url="http://localhost:11434/")
    
    if document_content:
        input_text += f"\n\nDocument Content:\n{document_content}"

    response = model.invoke(input_text)
    return response.content

def extract_text_from_file(uploaded_file):
    if uploaded_file is not None:
        file_type = uploaded_file.name.split(".")[-1]
        if file_type == "txt":
            return uploaded_file.read().decode("utf-8")
        elif file_type == "pdf":
            import PyPDF2
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        elif file_type == "docx":
            import docx # type: ignore
            doc = docx.Document(uploaded_file)
            return "\n".join([para.text for para in doc.paragraphs])
    return None

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state['chat_history'] = []

# When the form is submitted
if submit and (text or uploaded_file):
    with st.spinner("Generating response..."):
        document_content = extract_text_from_file(uploaded_file) if uploaded_file else None
        response = generate_response(text, document_content)
        st.session_state['chat_history'].append({"user": text, "ollama": response})
        st.write(response)

# Display chat history
st.write("## Chat History")
for chat in reversed(st.session_state['chat_history']):
    st.write(f"**🧑 User**: {chat['user']}")
    st.write(f"**🧠 Assistant**: {chat['ollama']}")
    st.write("---")
