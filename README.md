![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Build Passing](https://img.shields.io/badge/build-passing-brightgreen.svg)
![License](https://img.shields.io/badge/license-proprietary-lightgrey.svg)

---

# EDUChat-AI

EDUChat-AI is a web-based application that leverages AI and document processing to help users interact with PDF documents, chat about their contents, and grade essays using advanced language models.

---

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Customization: Essay Rubric](#customization-essay-rubric)
- [File Structure](#file-structure)
- [License](#license)
- [Acknowledgments](#acknowledgments)

---

## Features

- **PDF Upload & Processing:** Extracts and stores PDF text for AI-powered querying.
- **AI Chat:** Contextual Q&A about your uploaded documents via Gemini (Google AI Studio).
- **Essay Grading:** Grades essays (text or PDF) per a customizable rubric, with detailed feedback.
- **Custom Rubric:** Upload or define your own scoring rubric for essay grading (see [Customization](#customization-essay-rubric)).
- **Modern Web UI:** Clean chat and grading interfaces built with Flask.

## Tech Stack
- **Backend** : Python, Flask
- **AI & NLP** : Google Gemini AI, LangChain, HuggingFace Embeddings, FAISS
- **PDF Processing**: PyPDF2
- **Frontend**: HTML Templates (Flask/Jinja2)
---

## Demo
<img width="1663" height="768" alt="Screenshot 2025-07-13 141433" src="https://github.com/user-attachments/assets/d277f1c7-4e60-4b52-9929-1129fa739ace" />

---

## Setup Instructions

### Prerequisites

- **Python 3.8+**
- pip (Python package manager)
- **Google AI Studio (Gemini) API key**
- The following Python packages:

```bash
pip install flask PyPDF2 langchain langchain_community google-generativeai faiss-cpu python-dotenv
```

### API Key Warning

**Do NOT hard-code your API key in `app.py`.**  
Instead, create a `.env` file in your project root:

```
GEMINI_API_KEY=your_google_ai_studio_gemini_api_key
```

Then, load it in your app with [python-dotenv](https://pypi.org/project/python-dotenv/):

```python
from dotenv import load_dotenv
load_dotenv()
import os
gemini_api_key_mount = os.getenv("GEMINI_API_KEY")
```

---

## Usage

1. **Start the server:**

    ```bash
    python app.py
    ```

2. Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

- **Upload PDFs:** On the home page, upload your PDF documents.
- **Chat:** After upload, ask questions about your docs in the chat interface.
- **Essay Grading:** Navigate to the essay grading page to paste text or upload a PDF.  
  You can also set or upload a custom grading rubric.

---

## Customization: Essay Rubric

You can **define or upload your own rubric** for essay grading.  
Supported formats: plain text (default), or upload a JSON/CSV file with criteria and scoring.

- **How to set a rubric:**  
  Click “Set Rubric” on the grading page, enter your criteria (e.g., as plain text or upload a file).

**Sample rubric format (JSON):**

```json
{
  "criteria": [
    {"name": "Thesis", "max_score": 5},
    {"name": "Organization", "max_score": 5},
    {"name": "Grammar", "max_score": 5}
  ]
}
```

---

## File Structure

```
app.py
/templates/
    new_home.html
    new_chat.html
    new_pdf_chat.html
    new_essay_grading.html
    new_essay_rubric.html
__data__/
.env
```

---

## License

This project is **proprietary** and protected by copyright © 2025 Rasika Gautam.

You are welcome to view the code for educational or evaluation purposes (e.g., portfolio review by recruiters).  
However, you may **not copy, modify, redistribute, or claim this project as your own** under any circumstances — including in interviews or job applications — without written permission.

---


## Acknowledgments

- [LangChain](https://python.langchain.com/)
- [HuggingFace Embeddings](https://huggingface.co/)
- [Google Gemini (AI Studio)](https://ai.google/discover/gemini/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyPDF2](https://pypdf2.readthedocs.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🧑‍💻 Author

**Rasika Gautam**
*Data Science & AI Enthusiast* | B.Tech MAC, NSUT
[GitHub](https://github.com/rasika1205)
