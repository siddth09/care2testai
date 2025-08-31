# 🏥 Care2TestAI  

Care2TestAI is an AI-powered platform designed to simplify and automate healthcare test analysis.  
It provides a **Streamlit-based user interface** for interaction and a **FastAPI backend** for scalable processing.  

---

## 🌐 Live Demo  

- **Frontend (Streamlit UI):** [care2testai-ui.streamlit.app](https://care2testai-ui.streamlit.app/)  
- **Backend (FastAPI on Render):** [care2testai.onrender.com](https://care2testai.onrender.com)  
- **GitHub Repo:** [siddth09/care2testai](https://github.com/siddth09/care2testai)  

---

## 🎥 Demo Video  

[![Care2TestAI Demo](https://img.youtube.com/vi/gSKWZw28__Y/0.jpg)](https://youtu.be/gSKWZw28__Y)  

_Click the image above to watch the demo on YouTube._  

---

## ⚙️ Tech Stack  

- **Frontend:** [Streamlit](https://streamlit.io/)  
- **Backend:** [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/)  
- **Deployment:** [Streamlit Cloud](https://streamlit.io/cloud) (UI) + [Render](https://render.com/) (API)  
- **Libraries:** Pandas, NumPy, Pydantic, PyArrow, Altair  

---

## 🚀 Running Locally  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/siddth09/care2testai.git
   cd care2testai

2. **Create a virtual environment & install dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   pip install -r requirements.txt

3. **Run the FastAPI backend**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run the Streamlit frontend**

   ```bash
   streamlit run app.py
   ```

---

## 🛠 Features

* 📊 Upload and analyze test cases
* 🔍 AI-powered healthcare insights
* ⚡️ FastAPI backend for scalability
* 🎨 Interactive UI with Streamlit

---

## 📌 Roadmap

* [ ] Enhance model accuracy
* [ ] Add user authentication
* [ ] Support for more healthcare test formats
* [ ] Export results in PDF/Excel

---

## 📜 License

MIT License © 2025 [Siddharth](https://github.com/siddth09)
