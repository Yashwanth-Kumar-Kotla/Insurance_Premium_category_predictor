# 🏥 Insurance Premium Category Predictor

> An end-to-end machine learning application that predicts an individual's insurance premium category based on personal, lifestyle, and demographic inputs — built with a FastAPI backend, Streamlit frontend, and fully containerized with Docker.

[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-yashkotla%2Fstreamlit--insurance--cat--predictor-blue?logo=docker)](https://hub.docker.com/r/yashkotla/streamlit-insurance-cat-predictor)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?logo=streamlit)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange?logo=scikit-learn)](https://scikit-learn.org/)

---

## 📌 Overview

Insurance companies rely on risk profiling to determine premium tiers. This project automates that classification using a trained ML model exposed through a production-style REST API and an interactive Streamlit UI.

The system accepts user inputs — age, BMI, income, occupation, smoking status, and city — and returns a predicted premium category in real time.

---

## 🏗️ Architecture

```
┌─────────────────────┐         HTTP POST /predict        ┌──────────────────────┐
│   Streamlit UI      │  ────────────────────────────►   │   FastAPI Backend     │
│   (frontend.py)     │  ◄────────────────────────────   │   (app.py)            │
└─────────────────────┘         JSON Response              └──────────┬───────────┘
                                                                       │
                                                           ┌───────────▼───────────┐
                                                           │   ML Model (sklearn)  │
                                                           │   model/predict.py    │
                                                           └───────────────────────┘
```

**Two-service design:**
- **FastAPI** handles all ML inference logic, input validation via Pydantic schemas, and exposes RESTful endpoints
- **Streamlit** acts as the user-facing interface, collecting inputs and hitting the API

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| ML Model | scikit-learn (classification) |
| API Backend | FastAPI + Uvicorn |
| Data Validation | Pydantic (schema/UserInput, PredictedResponse) |
| Frontend | Streamlit |
| Containerization | Docker |
| Registry | Docker Hub |
| Language | Python 3.12 |

---

## 🔌 API Reference

### `POST /predict`
Predicts insurance premium category based on user inputs.

**Request Body:**
```json
{
  "age": 32,
  "weight": 72.5,
  "height": 1.75,
  "income_lpa": 12.0,
  "smoker": false,
  "city": "Bangalore",
  "occupation": "private_job"
}
```

**Response:**
```json
{
  "result": "High"
}
```

---

### `GET /health`
Returns API health status and model load confirmation.

```json
{
  "status": "OK",
  "API Running": "Yes",
  "Version": "1.0.0",
  "model_loaded": true
}
```

---

## 🚀 Run Locally

### Option 1 — Pull from Docker Hub (Recommended)

```bash
docker pull yashkotla/streamlit-insurance-cat-predictor
docker run -p 8000:8000 yashkotla/streamlit-insurance-cat-predictor
```

Then launch the Streamlit frontend separately:

```bash
pip install streamlit requests
streamlit run frontend.py
```

---

### Option 2 — Build from Source

```bash
git clone https://github.com/Yashwanth-Kumar-Kotla/Insurance_Premium_category_predictor.git
cd Insurance_Premium_category_predictor

# Build Docker image
docker build -t insurance-predictor .

# Run the FastAPI backend
docker run -p 8000:8000 insurance-predictor

# In a separate terminal, run the Streamlit frontend
pip install -r requirements.txt
streamlit run frontend.py
```

---

### Option 3 — Without Docker

```bash
pip install -r requirements.txt

# Terminal 1 — Start API
uvicorn app:app --host 0.0.0.0 --port 8000

# Terminal 2 — Start UI
streamlit run frontend.py
```

Open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
Insurance_Premium_category_predictor/
│
├── app.py                  # FastAPI application — routes, request handling
├── frontend.py             # Streamlit UI — form inputs, API calls
├── Dockerfile              # Container definition (Python 3.12 + Uvicorn)
├── requirements.txt        # Python dependencies
│
├── model/
│   └── predict.py          # Model loading, feature engineering, inference logic
│
├── schema/
│   ├── user_input.py       # Pydantic model for request validation
│   └── predicted_response.py # Pydantic model for response structure
│
└── config/                 # Configuration files (paths, constants, etc.)
```

---

## 🧠 ML Pipeline

The backend applies feature engineering on raw user inputs before inference:

| Raw Input | Engineered Feature |
|---|---|
| `age` | `age_group` (binned category) |
| `weight` + `height` | `bmi` (computed) |
| `smoker` + other risk factors | `lifestyle_risk` score |
| `city` | `city_tier` (1 / 2 / 3) |

The trained scikit-learn classifier is serialized and loaded at startup — confirmed via the `/health` endpoint.

---

## 🐳 Docker Details

**Dockerfile summary:**

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

- Base image: `python:3.12`
- Server: Uvicorn (ASGI) for production-grade async performance
- Port: `8000`
- Published to Docker Hub: [`yashkotla/streamlit-insurance-cat-predictor`](https://hub.docker.com/r/yashkotla/streamlit-insurance-cat-predictor)

---

## 🔗 Links

- **GitHub Repository:** [Insurance_Premium_category_predictor](https://github.com/Yashwanth-Kumar-Kotla/Insurance_Premium_category_predictor)  | [Live Demo](https://insurance-cat.streamlit.app/)
- **Docker Hub Image:** [yashkotla/streamlit-insurance-cat-predictor](https://hub.docker.com/r/yashkotla/streamlit-insurance-cat-predictor)
- **Portfolio:** [yashwanthportfolio.vercel.app](https://yashwanthportfolio.vercel.app)

---

## 👤 Author

**Yashwanth Kumar Kotla**  
MS Data Science · Webster University  
[GitHub](https://github.com/Yashwanth-Kumar-Kotla) · [Portfolio](https://yashwanthportfolio.vercel.app)
