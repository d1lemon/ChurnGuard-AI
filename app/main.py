
from pathlib import Path
from datetime import datetime

import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException

from app.schemas import CustomerInput
from app.database import get_connection, initialize_database


# --------------------------------------------------
# APPLICATION SETUP
# --------------------------------------------------

app = FastAPI(
    title="Customer Churn Prediction API",
    description="API for predicting customer churn using a machine learning model",
    version="1.0.0"
)


# --------------------------------------------------
# LOAD THE TRAINED MODEL
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "model"
    / "customer_churn_model.joblib"
)

model = joblib.load(MODEL_PATH)


# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------

initialize_database()


# --------------------------------------------------
# HOME ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Customer Churn Prediction API is running"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


# --------------------------------------------------
# PREDICTION ENDPOINT
# --------------------------------------------------

@app.post("/predict")
def predict(customer: CustomerInput):

    # Convert customer data to a DataFrame
    input_data = pd.DataFrame([
        customer.model_dump()
    ])

    # Generate churn probability
    churn_probability = float(
        model.predict_proba(input_data)[0][1]
    )

    # Generate prediction
    prediction = int(
        model.predict(input_data)[0]
    )

    # Determine risk level
    if churn_probability >= 0.70:
        risk_level = "HIGH"
    elif churn_probability >= 0.40:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Create timestamp
    timestamp = datetime.now().isoformat()

    # Save prediction to database
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        timestamp,
        "1.0.0",
        prediction,
        churn_probability,
        risk_level
    ))

    conn.commit()
    conn.close()

    # Return prediction
    return {
        "prediction": prediction,
        "churn_probability": round(
            churn_probability,
            4
        ),
        "risk_level": risk_level,
        "model_version": "1.0.0"
    }


# --------------------------------------------------
# GET ALL PREDICTIONS
# --------------------------------------------------

@app.get("/predictions")
def get_predictions():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            prediction_id,
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        FROM predictions
        ORDER BY prediction_id DESC
    """)

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


# --------------------------------------------------
# GET ONE PREDICTION
# --------------------------------------------------

@app.get("/predictions/{prediction_id}")
def get_prediction(prediction_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            prediction_id,
            timestamp,
            model_version,
            prediction,
            churn_probability,
            risk_level
        FROM predictions
        WHERE prediction_id = ?
    """, (
        prediction_id,
    ))

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
