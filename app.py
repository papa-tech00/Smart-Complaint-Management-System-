from flask import Flask, jsonify, request
import joblib
import os

from preprocess import preprocess_text


app = Flask(__name__)


# --------------------------------------------------
# File paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "vectorizer.pkl"
)


# --------------------------------------------------
# Category mapping
# --------------------------------------------------

CATEGORY_MAPPING = {
    0: "Drainage",
    1: "Electricity",
    2: "Garbage",
    3: "Road Damage",
    4: "Street Light",
    5: "Water Supply"
}


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")

except FileNotFoundError:
    print(f"Model file not found: {MODEL_PATH}")
    model = None

except Exception as error:
    print(f"Error loading model: {error}")
    model = None


# --------------------------------------------------
# Load TF-IDF vectorizer
# --------------------------------------------------

try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded successfully.")

except FileNotFoundError:
    print(f"Vectorizer file not found: {VECTORIZER_PATH}")
    vectorizer = None

except Exception as error:
    print(f"Error loading vectorizer: {error}")
    vectorizer = None


# --------------------------------------------------
# Sample prediction during startup
# --------------------------------------------------

if model is not None and vectorizer is not None:
    try:
        sample_complaint = (
            "The street light near Anna Nagar "
            "has not been working for three days."
        )

        cleaned_sample = preprocess_text(sample_complaint)

        sample_vector = vectorizer.transform(
            [cleaned_sample]
        )

        sample_prediction = model.predict(
            sample_vector
        )[0]

        predicted_category = CATEGORY_MAPPING.get(
            sample_prediction,
            str(sample_prediction)
        )

        print(f"Raw Prediction: {sample_prediction}")
        print(f"Sample Prediction: {predicted_category}")

    except Exception as error:
        print(f"Sample prediction error: {error}")

else:
    print(
        "Sample prediction skipped because "
        "model files were not loaded."
    )


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "status": "success",
            "message": "Smart Complaint AI API is running",
            "available_endpoints": {
                "health": "/health",
                "predict": "/predict"
            },
            "model_loaded": model is not None,
            "vectorizer_loaded": vectorizer is not None
        }
    ), 200


# --------------------------------------------------
# Prediction route
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    # Check whether request Content-Type is JSON
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Request must be JSON"
        }), 400

    # Read JSON safely
    data = request.get_json(silent=True)

    # Check malformed JSON
    if data is None:
        return jsonify({
            "status": "error",
            "message": "Invalid or malformed JSON"
        }), 400

    # JSON body must be an object
    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "JSON body must be an object"
        }), 400

    # Check complaint field
    if "complaint" not in data:
        return jsonify({
            "status": "error",
            "message": "Complaint field is required"
        }), 400

    complaint_text = data["complaint"]

    # Check complaint datatype
    if not isinstance(complaint_text, str):
        return jsonify({
            "status": "error",
            "message": "Complaint must be a string"
        }), 400

    # Remove extra spaces
    complaint_text = complaint_text.strip()

    # Check empty complaint
    if not complaint_text:
        return jsonify({
            "status": "error",
            "message": "Complaint text cannot be empty"
        }), 400

    # Check maximum length
    if len(complaint_text) > 5000:
        return jsonify({
            "status": "error",
            "message": "Complaint text too long (max 5000 characters)"
        }), 400

    # Check model and vectorizer
    if model is None or vectorizer is None:
        return jsonify({
            "status": "error",
            "message": "Model or vectorizer is not loaded"
        }), 503

    try:
        # Apply preprocessing
        cleaned_text = preprocess_text(complaint_text)

        if not cleaned_text:
            return jsonify({
                "status": "error",
                "message": (
                    "Complaint contains no valid text "
                    "after preprocessing"
                )
            }), 400

        # Convert text into TF-IDF features
        vectorized_text = vectorizer.transform([cleaned_text])

        # Predict category
        prediction = model.predict(vectorized_text)[0]

        # Convert prediction into readable category
        predicted_category = CATEGORY_MAPPING.get(
            prediction,
            str(prediction)
        )

        # Default value when predict_proba is unsupported
        confidence = None

        # Calculate confidence when supported
        if hasattr(model, "predict_proba"):
            probabilities = model.predict_proba(vectorized_text)[0]
            confidence = round(float(max(probabilities)), 4)

        # Standard Day 4 response
        return jsonify({
            "category": predicted_category,
            "confidence": confidence
        }), 200

    except Exception as error:
        app.logger.exception("Prediction failed: %s", error)

        return jsonify({
            "status": "error",
            "message": "Prediction failed"
        }), 500

# --------------------------------------------------
# Health-check route
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health_check():

    if model is None or vectorizer is None:
        return jsonify(
            {
                "status": "error",
                "message": "Model or vectorizer is not loaded",
                "model_loaded": model is not None,
                "vectorizer_loaded": vectorizer is not None
            }
        ), 503

    return jsonify(
        {
            "status": "success",
            "message": "API, model and vectorizer are ready",
            "model_loaded": True,
            "vectorizer_loaded": True
        }
    ), 200


# --------------------------------------------------
# 404 error handler
# --------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):
    return jsonify(
        {
            "status": "error",
            "message": "Route not found"
        }
    ), 404


# --------------------------------------------------
# 500 error handler
# --------------------------------------------------

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            "status": "error",
            "message": "Internal server error"
        }
    ), 500


# --------------------------------------------------
# Start Flask server
# --------------------------------------------------

if __name__ == "__main__":
    print("API server started successfully.")

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )