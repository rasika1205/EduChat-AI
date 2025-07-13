gemini_api_key_mount="AIzaSyCsAJm_lOqye8oSi7DlgXiinoGLEF0Z06I"
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from flask import Flask, render_template, request, redirect
import os
import google.generativeai as genai
genai.configure(api_key=gemini_api_key_mount)

import re
start_greeting = ["hi","hello"]
end_greeting = ["bye"]
way_greeting = ["who are you?"]

#Using this folder for storing the uploaded docs. Creates the folder at runtime if not present
DATA_DIR = "__data__"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
#Flask App
app = Flask(__name__)

vectorstore = None
conversation_chain = None
chat_history = []
rubric_text = ""
gemini_model = genai.GenerativeModel("gemini-1.5-flash")
class HumanMessage:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f'HumanMessage(content={self.content})'


class AIMessage:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return f'AIMessage(content={self.content})'
# pdf extraction
def get_pdf_text(pdf_docs):
    text = ""
    pdf_txt = ""
    for pdf in pdf_docs:
        filename = os.path.join(DATA_DIR,pdf.filename)
        pdf_txt = ""
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
            pdf_txt += page.extract_text()

        with (open(filename, "w", encoding="utf-8")) as op_file:
            op_file.write(pdf_txt)

    return text
def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks
def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vs = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vs

def grade_essay(essay_text):
    prompt = f"""
You are an expert English language essay grader from India. Grade the following essay using the Indian academic style.

{rubric_text}

ESSAY:
{essay_text}

Please give scores for each criterion and a final comment.
"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    feedback = response.text
    feedback = re.sub(r'\n', '<br>', feedback)  # Optional: convert to HTML

    return feedback
@app.route('/')
def home():
    return render_template('new_home.html')

@app.route('/process', methods=['POST'])
def process_documents():
    global vectorstore
    pdf_docs = request.files.getlist('pdf_docs')
    raw_text = get_pdf_text(pdf_docs)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks)
    return redirect('/chat')


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global vectorstore, chat_history
    if vectorstore is None:
        return "Error: You must upload documents first."

    if request.method == 'POST':
        user_question = request.form['user_question']

        # Retrieve relevant chunks
        retriever = vectorstore.as_retriever()
        relevant_docs = retriever.get_relevant_documents(user_question)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Build prompt
        prompt = f"""
    Use the context below to answer the question.
    If unsure, say you don't know.

    Context:
    {context}

    Question: {user_question}
    """
        # Generate answer
        response = gemini_model.generate_content(prompt)
        answer = response.text

        # Update chat history
        chat_history.append(HumanMessage(user_question))
        chat_history.append(AIMessage(answer))

    return render_template('new_chat.html', chat_history=chat_history)


@app.route('/pdf_chat', methods=['GET', 'POST'])
def pdf_chat():
    return render_template('new_pdf_chat.html')


@app.route('/essay_grading', methods=['GET', 'POST'])
def essay_grading():
    result = None
    if request.method == 'POST':
        if request.form.get('essay_rubric', False):
            global rubric_text
            rubric_text = request.form.get('essay_rubric')

            return render_template('new_essay_grading.html')

        if len(request.files['file'].filename) > 0:
            pdf_file = request.files['file']
            text = extract_text_from_pdf(pdf_file)
            result = grade_essay(text)
        else:
            text = request.form.get('essay_text')
            result = grade_essay(text)

    return render_template('new_essay_grading.html', result=result, input_text=text)


@app.route('/essay_rubric', methods=['GET', 'POST'])
def essay_rubric():
    return render_template('new_essay_rubric.html')


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text


if __name__ == '__main__':
    app.run(debug=True)