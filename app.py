
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Local JSON file for storing overlays
DATA_FILE = "overlays.json"

def read_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running successfully!"})

@app.route("/overlay", methods=["GET"])
def get_overlays():
    return jsonify(read_data())

@app.route("/overlay", methods=["POST"])
def add_overlay():
    data = request.json
    overlays = read_data()
    overlays.append(data)
    write_data(overlays)
    return jsonify({"message": "Overlay added successfully!"})

@app.route("/overlay/<int:index>", methods=["PUT"])
def update_overlay(index):
    overlays = read_data()
    if 0 <= index < len(overlays):
        overlays[index] = request.json
        write_data(overlays)
        return jsonify({"message": "Overlay updated successfully!"})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/overlay/<int:index>", methods=["DELETE"])
def delete_overlay(index):
    overlays = read_data()
    if 0 <= index < len(overlays):
        overlays.pop(index)
        write_data(overlays)
        return jsonify({"message": "Overlay deleted successfully!"})
    return jsonify({"error": "Invalid index"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
