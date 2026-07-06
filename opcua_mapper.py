def get_opcua_value(payload, topic, default=0):
    try:
        value = payload["values"][topic]["payload"]["value"]
        return default if value is None else value
    except Exception:
        return default


def map_opcua_to_status(payload, get_phase):
    k1 = get_opcua_value(payload, "brauanlage/k1/temperatur", 0)
    k2 = get_opcua_value(payload, "brauanlage/k2/temperatur", 0)
    k3 = get_opcua_value(payload, "brauanlage/k3/temperatur", 0)
    k4 = get_opcua_value(payload, "brauanlage/k4/mobiler_sensor/temperatur", 0)

    k2_level = get_opcua_value(payload, "brauanlage/k2/fuellstand", 0)
    k3_level = get_opcua_value(payload, "brauanlage/k3/fuellstand", 0)

    flow = get_opcua_value(payload, "brauanlage/durchfluss/nachguss_maische", 0)
    step = get_opcua_value(payload, "brauanlage/status/aktueller_schritt", 0)

    return {
        "backend": "online",
        "source": "OPC-UA JSON",
        "timestamp": payload.get("timestamp"),
        "aktueller_schritt": int(step),
        "currentStep": int(step),
        "phase": get_phase(int(step)),
        "alarm": False,
        "alarmStatus": False,
        "durchfluss": float(flow),
        "flowRate": float(flow),
        "k1_temperatur": float(k1),
        "k1Temperature": float(k1),
        "k2_temperatur": float(k2),
        "k2Temperature": float(k2),
        "k3_temperatur": float(k3),
        "k3Temperature": float(k3),
        "k4_temperatur": float(k4),
        "k4Temperature": float(k4),
        "k2_fuellstand": float(k2_level),
        "k2Level": float(k2_level),
        "k3_fuellstand": float(k3_level),
        "k3Level": float(k3_level),
    }
