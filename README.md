# ChurnGuard AI — Customer Churn Prediction API

A machine-learning project that predicts customer churn and exposes the model through a REST API built with FastAPI.

**ChurnGuard AI demonstrates how a trained machine-learning model can be turned into a usable service** with input validation, probability-based risk classification, persistent prediction history, and API documentation.

## Project Overview

Customer churn occurs when customers stop using a company's products or services. Identifying customers who may be at risk of leaving can help businesses prioritize retention efforts.

ChurnGuard AI accepts customer attributes, runs them through a trained scikit-learn pipeline, and returns a churn prediction, estimated churn probability, and risk category.

### Key Features

- Customer churn prediction using a trained scikit-learn model
- Churn probability estimation
- LOW, MEDIUM, and HIGH risk classification
- Request validation using Pydantic
- Prediction history stored in SQLite
- Retrieval of all saved predictions or an individual prediction
- Health-check endpoint
- Interactive Swagger API documentation
- Docker support

## Architecture

```text
Customer Record
      |
      v
   FastAPI
      |
      v
 Pydantic Validation
      |
      v
Trained ML Pipeline
      |
      v
Churn Prediction
      |
      v
Probability + Risk Level
      |
      v
 SQLite Prediction History
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application and machine-learning programming |
| FastAPI | REST API framework |
| scikit-learn | Model pipeline and prediction |
| Pandas | Data preparation |
| Pydantic | Request validation |
| SQLite | Prediction-history storage |
| Joblib | Saved model serialization |
| Uvicorn | ASGI application server |
| Docker | Containerization |

## Model Performance

The following metrics are documented for the trained model:

| Metric | Score |
|---|---:|
| Accuracy | 0.8055 |
| Precision | 0.6572 |
| Recall | 0.5588 |
| F1 Score | 0.6040 |
| ROC-AUC | 0.8419 |

These are the project's recorded evaluation results, not a guarantee of performance on new customer data.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API status message |
| GET | `/health` | Health check |
| POST | `/predict` | Generate a churn prediction |
| GET | `/predictions` | Retrieve saved prediction history |
| GET | `/predictions/{prediction_id}` | Retrieve a specific prediction |
| GET | `/docs` | Interactive Swagger documentation |

## Example Prediction

### Request

Send a `POST` request to `/predict` with a customer record:

```json
{
  "gender": "Female",
  "SeniorCitizen": 0,
  "Partner": "Yes",
  "Dependents": "No",
  "tenure": 12,
  "PhoneService": "Yes",
  "MultipleLines": "No",
  "InternetService": "DSL",
  "OnlineSecurity": "No",
  "OnlineBackup": "Yes",
  "DeviceProtection": "No",
  "TechSupport": "No",
  "StreamingTV": "No",
  "StreamingMovies": "No",
  "Contract": "Month-to-month",
  "PaperlessBilling": "Yes",
  "PaymentMethod": "Electronic check",
  "MonthlyCharges": 70.35,
  "TotalCharges": 844.2
}
```

This is an illustrative test record, not a real customer's information.

### Response

The API returned the following result for this sample:

```json
{
  "prediction": 0,
  "churn_probability": 0.2931,
  "risk_level": "LOW",
  "model_version": "1.0.0"
}
```

Interpretation:

- `prediction`: `0` indicates predicted no churn; `1` indicates predicted churn.
- `churn_probability`: estimated probability of churn, from 0 to 1.
- `risk_level`: risk category assigned by the application.
- `model_version`: version identifier for the model.

The probability is an estimate, not a guarantee of future customer behavior.

## Risk Classification

The application uses these thresholds:

| Risk Level | Churn Probability |
|---|---|
| LOW | Less than 0.40 |
| MEDIUM | 0.40 to less than 0.70 |
| HIGH | 0.70 or greater |

## Prediction History

Successful predictions are saved in SQLite.

The `GET /predictions` endpoint returns the total number of stored predictions and the prediction records. Each record includes fields such as:

- Prediction ID
- Timestamp
- Model version
- Prediction result
- Churn probability
- Risk level

Use `GET /predictions/{prediction_id}` to retrieve an individual record.

## Input Validation

The API validates incoming customer records before running the model.

For example, `SeniorCitizen` must be either `0` or `1`. A request containing `"SeniorCitizen": 5` returns HTTP `422 Unprocessable Entity` rather than proceeding with an invalid prediction.

## Local Installation

### Prerequisites

- Python installed
- Git
- The project repository cloned to your computer

### 1. Clone the repository

```bash
git clone https://github.com/d1lemon/ChurnGuard-AI.git
cd ChurnGuard-AI
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Git Bash on Windows:**

```bash
python -m venv .venv
source .venv/Scripts/activate
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install "scikit-learn==1.6.1"
```

**Model compatibility note:** The saved model was tested successfully with scikit-learn 1.6.1. Keep this version when loading the included model artifact unless you retrain and validate the model with another version.

### 4. Start the API

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 5. Open the documentation

Visit:

- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

To stop the server, press `Ctrl+C` in the terminal running Uvicorn.

## Running with Docker

Build the image from the repository directory:

```bash
docker build -t churnguard-ai .
```

Run the container:

```bash
docker run --rm -p 8000:8000 churnguard-ai
```

Open the API documentation at:

http://localhost:8000/docs

To stop a foreground container, press `Ctrl+C`.

## Testing and Verification

The API was tested through its interactive Swagger documentation and a temporary public Cloudflare tunnel.

| Test | Result |
|---|---|
| `GET /health` | HTTP 200 |
| `POST /predict` with valid input | HTTP 200 |
| `GET /predictions` | HTTP 200 |
| `GET /predictions/2` | HTTP 200 |
| Invalid `SeniorCitizen` value of `5` | HTTP 422 |

The history test confirmed that prediction records could be saved and retrieved from SQLite. The invalid-input test confirmed that the API rejects out-of-range input.

## Deployment and Demo Notes

A temporary Cloudflare Quick Tunnel was used to demonstrate the locally running API.

This approach is suitable for a short demonstration, but it is **not permanent hosting**. The temporary URL may change or stop working when the tunnel closes. The computer, API server, and tunnel must remain running for the demo to be accessible.

The project also includes a Dockerfile for containerized execution. A permanent hosted deployment requires a suitable hosting environment and separate deployment verification.

## Limitations and Future Improvements

Potential next steps include:

- Deploying the API to a permanent hosting platform
- Adding automated unit and integration tests
- Tracking model performance and prediction drift
- Adding authentication and rate limiting before broader public use
- Improving logging, monitoring, and error handling
- Retraining and evaluating the model on updated customer data
- Building a dashboard for churn-risk monitoring

## Dataset

The project uses the Telco Customer Churn dataset.

Dataset source:

https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv

## Repository Structure

```text
ChurnGuard-AI/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
├── model/
│   └── customer_churn_model.joblib
├── Dockerfile
├── requirements.txt
└── README.md
```

## Author

**Dymphna Lemon**

Project: ChurnGuard AI — Customer Churn Prediction API

Repository: https://github.com/d1lemon/ChurnGuard-AI
