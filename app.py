from flask import Flask, jsonify
import joblib
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "models", "vectorizer.pkl")


try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Model file not found: {MODEL_PATH}")
    model = None
except Exception as error:
    print(f"Error loading model: {error}")
    model = None


try:
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Vectorizer loaded successfully.")
except FileNotFoundError:
    print(f"Vectorizer file not found: {VECTORIZER_PATH}")
    vectorizer = None
except Exception as error:
    print(f"Error loading vectorizer: {error}")
    vectorizer = None


if model is not None and vectorizer is not None:
    try:
        sample_complaint = [
            "The street light near Anna Nagar has not been working for three days."
        ]

        sample_vector = vectorizer.transform(sample_complaint)
        prediction = model.predict(sample_vector)

        category_mapping = {
            0: "Drainage",
            1: "Electricity",
            2: "Garbage",
            3: "Road Damage",
            4: "Street Light",
            5: "Water Supply"
        }

        predicted_value = prediction[0]

        if predicted_value in category_mapping:
            predicted_category = category_mapping[predicted_value]
        else:
            predicted_category = str(predicted_value)

        print(f"Raw Prediction: {predicted_value}")
        print(f"Sample Prediction: {predicted_category}")

    except Exception as error:
        print(f"Sample prediction error: {error}")
else:
    print("Sample prediction skipped because model files were not loaded.")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify(
        {
            "status": "success",
            "message": "Smart Complaint AI API is running",
            "model_loaded": model is not None,
            "vectorizer_loaded": vectorizer is not None
        }
    ), 200


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


@app.errorhandler(404)
def page_not_found(error):
    return jsonify(
        {
            "status": "error",
            "message": "Route not found"
        }
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(
        {
            "status": "error",
            "message": "Internal server error"
        }
    ), 500


if __name__ == "__main__":
    print("API server started successfully.")
    app.run(debug=True)