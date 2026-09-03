
# Customer Churn Prediction API

A machine learning API that predicts whether a customer is likely to churn.

The application uses a trained machine learning model and FastAPI to provide churn predictions through a REST API. Successful predictions are stored in a SQLite database.

## Features

* Customer churn prediction
* Churn probability calculation
* Risk level classification
* Input validation using Pydantic
* SQLite database storage
* Prediction history retrieval
* Health check endpoint
* Interactive API documentation with FastAPI

## Model Performance

| Metric    |  Score |
| --------- | -----: |
| Accuracy  | 0.8055 |
| Precision | 0.6572 |
| Recall    | 0.5588 |
| F1 Score  | 0.6040 |
| ROC-AUC   | 0.8419 |

## API Endpoints

| Method | Endpoint                       | Description                    |
| ------ | ------------------------------ | ------------------------------ |
| GET    | `/`                            | API status message             |
| GET    | `/health`                      | Health check                   |
| POST   | `/predict`                     | Generate a churn prediction    |
| GET    | `/predictions`                 | Retrieve all saved predictions |
| GET    | `/predictions/{prediction_id}` | Retrieve one prediction        |

## Project Structure

```text
customer-churn-api/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── schemas.py
│   └── main.py
│
├── model/
│   └── customer_churn_model.joblib
│
├── requirements.txt
└── README.md
```

## Installation

After cloning or downloading the project:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI application:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Example Prediction Response

```json
{
  "prediction": 1,
  "churn_probability": 0.74,
  "risk_level": "HIGH",
  "model_version": "1.0.0"
}
```

## Risk Levels

* **HIGH:** probability greater than or equal to 0.70
* **MEDIUM:** probability greater than or equal to 0.40 and less than 0.70
* **LOW:** probability less than 0.40

## Technologies Used

* Python
* FastAPI
* Scikit-learn
* Pandas
* Pydantic
* SQLite
* Joblib

## Author:  Dymphna Lemon

Customer Churn Prediction API Project


