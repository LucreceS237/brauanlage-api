from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

CSV_FILE = "data.csv"


@app.route("/")
def home():
    return jsonify({
        "message": "Brauanlage Flask API läuft",
        "status": "online"
    })


@app.route("/api/status", methods=["GET"])
def api_status():
    df = pd.read_csv(CSV_FILE)
    last = df.iloc[-1].to_dict()

    return jsonify({
        "backend": "online",
        "timestamp": last["timestamp"],
        "aktueller_schritt": int(last["aktueller_schritt"]),
        "currentStep": int(last["aktueller_schritt"]),
        "phase": "Maischen",
        "alarm": bool(last["alarm"]),
        "alarmStatus": bool(last["alarm"]),
        "durchfluss": float(last["durchfluss"]),
        "flowRate": float(last["durchfluss"]),
        "k1_temperatur": float(last["k1_temperatur"]),
        "k1Temperature": float(last["k1_temperatur"]),
        "k2_temperatur": float(last["k2_temperatur"]),
        "k2Temperature": float(last["k2_temperatur"]),
        "k3_temperatur": float(last["k3_temperatur"]),
        "k3Temperature": float(last["k3_temperatur"]),
        "k2_fuellstand": float(last["k2_fuellstand"]),
        "k2Level": float(last["k2_fuellstand"]),
        "k3_fuellstand": float(last["k3_fuellstand"]),
        "k3Level": float(last["k3_fuellstand"])
    })


@app.route("/api/history")
def history():
    df = pd.read_csv(CSV_FILE)
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/control", methods=["POST"])
def control():
    return jsonify({
        "message": "Control command received",
        "received": request.json
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
