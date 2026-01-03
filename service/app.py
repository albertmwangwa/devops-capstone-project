"""Flask application for the account service"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True)
