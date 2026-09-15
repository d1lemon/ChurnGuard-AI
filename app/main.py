
from pathlib import Path
from datetime import datetime, timezone

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException

from app.schemas import CustomerInput
from app.database import get_connection, initialize_database


app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using a machine learning model",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "model" / "customer_churn_model.joblib"

model = joblib.load(MODEL_PATH)

initialize_database()


@app.get("/")
def home():
    return {
        "message": "Customer Churn Prediction API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/predict")
def predict(customer: CustomerInput):

    input_data = pd.DataFrame(
        [customer.model_dump()]
    )

    churn_probability = float(
        model.predict_proba(input_data)[0][1]
    )

    prediction = int(
        model.predict(input_data)[0]
    )

    if churn_probability >= 0.70:
        risk_level = "HIGH"
    elif churn_probability >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO predictions (
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            "1.0.0",
            prediction,
            churn_probability,
            risk_level
        )
    )

    conn.commit()
    conn.close()

    return {
        "prediction": prediction,
        "churn_probability": round(
            churn_probability,
            4
        ),
        "risk_level": risk_level,
        "model_version": "1.0.0"
    }


@app.get("/predictions")
def get_predictions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            prediction_id,
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        FROM predictions
        ORDER BY prediction_id DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    predictions = []

    for row in rows:

        predictions.append({
            "prediction_id": row[0],
            "timestamp": row[1],
            "model_version": row[2],
            "prediction": row[3],
            "churn_probability": row[4],
            "risk_level": row[5]
        })

    return {
        "total_predictions": len(predictions),
        "predictions": predictions
    }


@app.get("/predictions/{prediction_id}")
def get_prediction(
    prediction_id: int
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            prediction_id,
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        FROM predictions
        WHERE prediction_id = ?
        """,
        (
            prediction_id,
        )
    )

    row = cursor.fetchone()
    conn.close()

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="Prediction not found"
        )

    return {
        "prediction_id": row[0],
        "timestamp": row[1],
        "model_version": row[2],
        "prediction": row[3],
        "churn_probability": row[4],
        "risk_level": row[5]
    }
