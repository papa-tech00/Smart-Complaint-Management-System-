from flask import Flask, jsonify

# Create the Flask application
app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Home route used to verify that the API server is running.
    """
    return jsonify(
        {
            "status": "success",
            "message": "Smart Complaint AI API is running"
        }
    ), 200


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles invalid routes.
    """
    return jsonify(
        {
            "status": "error",
            "message": "Route not found"
        }
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Handles unexpected server errors.
    """
    return jsonify(
        {
            "status": "error",
            "message": "Internal server error"
        }
    ), 500


if __name__ == "__main__":
    app.run(debug=True)