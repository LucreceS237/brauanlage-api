from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd

from anomaly_detection.detector import Ap5Detector

app = Flask(__name__)
CORS(app)

SCENARIOS = {
    "normal": "simulation/data_normal.csv",
    "temperature_alarm": "simulation/data_alarm_temperature.csv",
    "sensor_disconnected": "simulation/data_sensor_disconnected.csv",
    "flow_error": "simulation/data_flow_error.csv",
    "emergency_stop": "simulation/data_emergency_stop.csv",
}

CURRENT_SCENARIO = "normal"
detector = Ap5Detector(expected_mode="SIMULATION")

def get_csv_file():
    return SCENARIOS.get(CURRENT_SCENARIO, SCENARIOS["normal"])

def read_data():
    df = pd.read_csv(get_csv_file())
    return df


def get_last_status():
    df = read_data()
    last = df.iloc[-1].to_dict()

    return {
        "backend": "online",
        "timestamp": last["timestamp"],
        "aktueller_schritt": int(last["aktueller_schritt"]),
        "currentStep": int(last["aktueller_schritt"]),
        "phase": get_phase(int(last["aktueller_schritt"])),
        "alarm": str(last["alarm"]).lower() == "true",
        "alarmStatus": str(last["alarm"]).lower() == "true",
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
    }


def get_phase(step):
    phases = {
        0: "Idle",
        1: "Nachguss",
        2: "Maischen",
        3: "Läutern",
        4: "Kochen",
        5: "Kühlen",
        6: "Gären",
        7: "Fertig"
    }
    return phases.get(step, "Unknown")


def build_detector_payload(status):
    return {
        "connectionStatus": "CONNECTED",
        "source": "SIMULATION",
        "values": {
            "K1_Temperatur": status["k1_temperatur"],
            "K2_Temperatur": status["k2_temperatur"],
            "K3_Temperatur": status["k3_temperatur"],
            "MobilerSensor_Temperatur": 0.0,
            "Durchfluss_NachgussMaische": status["durchfluss"]
        }
    }


def alarm_to_dict(alarm, alarm_id):
    return {
        "id": alarm_id,
        "ruleId": alarm.ruleId,
        "code": alarm.code,
        "severity": alarm.severity,
        "state": alarm.state,
        "component": alarm.component,
        "variable": alarm.variable,
        "value": alarm.value,
        "threshold": alarm.threshold,
        "message": alarm.message,
        "status": alarm.status,
        "createdAt": alarm.createdAt.isoformat() if hasattr(alarm.createdAt, "isoformat") else str(alarm.createdAt),
        "clearedAt": None
    }


@app.route("/")
def home():
    return jsonify({
        "message": "Brauanlage Flask API läuft",
        "status": "online",
        "endpoints": [
            "/api/status",
            "/api/history",
            "/api/control",
            "/api/alarms/active",
            "/api/alarms/history"
        ]
    })


@app.route("/api/status", methods=["GET"])
def api_status():
    return jsonify(get_last_status())


@app.route("/api/history", methods=["GET"])
def history():
    df = read_data()
    return jsonify(df.to_dict(orient="records"))


@app.route("/api/alarms/active", methods=["GET"])
def active_alarms():
    status = get_last_status()
    payload = build_detector_payload(status)

    alarms = detector.evaluate(
        payload=payload,
        fsm_state=status["phase"],
        invalid_payload=False
    )

    result = []

    for i, alarm in enumerate(alarms):
        result.append(alarm_to_dict(alarm, f"ap5-active-{i}"))

    if status["alarm"] is True:
        result.append({
            "id": "csv-active-alarm",
            "ruleId": "CSV_001",
            "code": "CSV_ALARM_ACTIVE",
            "severity": "HIGH",
            "state": status["phase"],
            "component": "Brauanlage",
            "variable": "alarm",
            "value": True,
            "threshold": "false",
            "message": "CSV-Datensatz meldet eine aktive Anomalie.",
            "status": "ACTIVE",
            "createdAt": status["timestamp"],
            "clearedAt": None
        })

    return jsonify(result)


@app.route("/api/alarms/history", methods=["GET"])
def alarm_history():
    df = read_data()
    alarms = []

    previous_values = None

    for i, row in df.iterrows():
        status = {
            "timestamp": row["timestamp"],
            "phase": get_phase(int(row["aktueller_schritt"])),
            "k1_temperatur": float(row["k1_temperatur"]),
            "k2_temperatur": float(row["k2_temperatur"]),
            "k3_temperatur": float(row["k3_temperatur"]),
            "durchfluss": float(row["durchfluss"]),
            "alarm": str(row["alarm"]).lower() == "true"
        }

        payload = {
            "connectionStatus": "CONNECTED",
            "source": "SIMULATION",
            "values": {
                "K1_Temperatur": status["k1_temperatur"],
                "K2_Temperatur": status["k2_temperatur"],
                "K3_Temperatur": status["k3_temperatur"],
                "MobilerSensor_Temperatur": 0.0,
                "Durchfluss_NachgussMaische": status["durchfluss"]
            }
        }

        if previous_values is not None:
            payload["previous_values"] = previous_values

        detected = detector.evaluate(
            payload=payload,
            fsm_state=status["phase"],
            invalid_payload=False
        )

        for j, alarm in enumerate(detected):
            alarms.append(alarm_to_dict(alarm, f"ap5-history-{i}-{j}"))

        if status["alarm"]:
            alarms.append({
                "id": f"csv-alarm-{i}",
                "ruleId": "CSV_001",
                "code": "CSV_ALARM_ACTIVE",
                "severity": "HIGH",
                "state": status["phase"],
                "component": "Brauanlage",
                "variable": "alarm",
                "value": True,
                "threshold": "false",
                "message": "CSV-Datensatz enthält eine aktive Anomalie.",
                "status": "ACTIVE",
                "createdAt": status["timestamp"],
                "clearedAt": None
            })

        previous_values = payload["values"]

    return jsonify(alarms)


@app.route("/api/alarms/<alarm_id>/acknowledge", methods=["POST"])
def acknowledge_alarm(alarm_id):
    return jsonify({
        "message": f"Alarm {alarm_id} acknowledged"
    })


@app.route("/api/control", methods=["POST"])
def control():
    return jsonify({
        "message": "Control command received",
        "received": request.json
    })

@app.route("/api/simulation/scenarios", methods=["GET"])
def simulation_scenarios():
    return jsonify([
        {"id": "normal", "name": "Normalbetrieb"},
        {"id": "temperature_alarm", "name": "Temperaturfehler"},
        {"id": "sensor_disconnected", "name": "Sensor getrennt"},
        {"id": "flow_error", "name": "Durchflussfehler"},
        {"id": "emergency_stop", "name": "Not-Aus"}
    ])


@app.route("/api/simulation/scenario", methods=["POST"])
def set_simulation_scenario():
    global CURRENT_SCENARIO

    data = request.json or {}
    scenario = data.get("scenario")

    if scenario not in SCENARIOS:
        return jsonify({"error": "Unknown scenario"}), 400

    CURRENT_SCENARIO = scenario

    return jsonify({
        "message": "Scenario changed",
        "scenario": CURRENT_SCENARIO
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
