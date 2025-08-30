# 🏥 Doctor Prescription Helper (AI + LangChain + FastAPI + Streamlit)

This project is an **AI-powered web application** that helps patients remember their doctor’s advice and provides **home remedies** and **motivational tips** based on their prescriptions.  
It uses **LangChain + FastAPI** for the backend AI logic and **Streamlit** for the frontend UI.

---

## 🚀 Features
- Upload your **doctor's prescription (PDF)**  
- AI will analyze and provide:
  - Doctor’s instructions in simple words
  - Suggested **home remedies**
  - **Motivational advice**  
- Backend: `LangChain + FastAPI`  
- Frontend: `Streamlit`

---

## 📂 Project Structure
├── backend
│ ├── main.py # FastAPI backend with LangChain logic
│ ├── requirements.txt # Backend dependencies
│
├── frontend
│ ├── app.py # Streamlit frontend
│ ├── requirements.txt # Frontend dependencies
│
├── sample_prescription.pdf # Example doctor prescription
└── README.md


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

bash -
git clone https://github.com/yourusername/doctor-prescription-helper.git
cd doctor-prescription-helper

2️⃣ Create a Virtual Environment (recommended)
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install Dependencies
Backend (FastAPI + LangChain)
cd backend
pip install -r requirements.txt

Frontend (Streamlit)
cd ../frontend
pip install -r requirements.txt

▶️ Running the Project
Step 1: Start the Backend
cd backend
uvicorn main:app --reload


Server will run on: http://127.0.0.1:8000

Step 2: Start the Frontend
cd ../frontend
streamlit run app.py


App will run on: http://localhost:8501
