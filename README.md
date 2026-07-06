# 🍺 Digitaler Zwilling einer Brauanlage – Flask Backend

## Projektübersicht

Dieses Repository enthält das Backend des Projekts **„Digitaler Zwilling einer Brauanlage“**.

Das Backend wurde im Rahmen des Moduls **Modellbasierter Systementwurf und technisches Projektmanagement (MBSE)** entwickelt.

Es dient als Kommunikationsschicht zwischen den Prozessdaten der Brauanlage und dem webbasierten Dashboard.

Während der Entwicklungsphase werden die Prozessdaten über eine CSV-basierte Simulation bereitgestellt. Im späteren Produktivbetrieb kann dieselbe Architektur ohne Änderungen auf reale OPC-UA-Daten umgestellt werden.

---

# Projektziele

Ziel des Projekts ist die Entwicklung eines Digitalen Zwillings einer Siemens S7-1500 Brauanlage.

Das Backend übernimmt dabei folgende Aufgaben:

- Bereitstellung aktueller Prozessdaten
- Bereitstellung historischer Messwerte
- Alarmverwaltung
- Simulationssteuerung
- REST-Schnittstelle für das Dashboard
- Vorbereitung der OPC-UA-Integration

---

# Systemarchitektur

```
                Siemens S7-1500
                      │
                  OPC-UA
                      │
            (zukünftiger Betrieb)
                      │
               Flask Backend
          -----------------------
          REST API (JSON)
          Alarm Detection
          CSV Simulation
          -----------------------
                      │
                 HTTP / JSON
                      │
             Lovable Dashboard
```

---

# Projektstruktur

```
brauanlage-api
│
├── app.py
├── requirements.txt
├── simulation/
│   ├── data_normal.csv
│   ├── data_alarm_temperature.csv
│   ├── data_sensor_disconnected.csv
│   ├── data_flow_error.csv
│   └── data_emergency_stop.csv
│
├── anomaly_detection/
│   ├── detector.py
│   └── ...
│
├── opcua_mapper.py
│
└── README.md
```

---

# Verwendete Technologien

| Technologie | Zweck |
|-------------|-------|
| Python | Backend |
| Flask | REST API |
| Flask-CORS | CORS-Unterstützung |
| Pandas | CSV-Verarbeitung |
| JSON | Datenaustausch |
| Render | Deployment |
| GitHub | Versionsverwaltung |
| Lovable | Dashboard |

---

# REST API

## Status

```
GET /api/status
```

Liefert den aktuellen Anlagenzustand.

---

## Historie

```
GET /api/history
```

Liefert alle Messwerte.

---

## Aktive Alarme

```
GET /api/alarms/active
```

Liefert alle aktiven Alarme.

---

## Alarmhistorie

```
GET /api/alarms/history
```

Historische Alarmmeldungen.

---

## Steuerung

```
POST /api/control
```

Empfängt Steuerbefehle.

---

## Simulation

### Szenarien anzeigen

```
GET /api/simulation/scenarios
```

---

### Szenario wechseln

```
POST /api/simulation/scenario
```

Body:

```json
{
  "scenario":"temperature_alarm"
}
```

---

### Simulation zurücksetzen

```
POST /api/simulation/reset
```

---

### Simulationsstatus

```
GET /api/simulation/status
```

---

## Systeminformationen

```
GET /api/info
```

---

## Health Check

```
GET /api/health
```

---

## Version

```
GET /api/version
```

---

# Simulationsszenarien

| Szenario | Beschreibung |
|-----------|--------------|
| normal | Normalbetrieb |
| temperature_alarm | Temperatur überschritten |
| sensor_disconnected | Sensorfehler |
| flow_error | Durchflussfehler |
| emergency_stop | Not-Aus |

---

# Beispiel einer API-Antwort

```json
{
    "backend":"online",
    "phase":"Maischen",
    "k1Temperature":63.2,
    "k2Temperature":65.8,
    "k3Temperature":24.1,
    "flowRate":1.4,
    "alarm":false
}
```

---

# Lokale Installation

Repository klonen

```bash
git clone https://github.com/LucreceS237/brauanlage-api.git
```

Projekt öffnen

```bash
cd brauanlage-api
```

Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Backend starten

```bash
python app.py
```

Das Backend läuft anschließend unter

```
http://localhost:5000
```

---

# Deployment

Das Backend wurde auf **Render** veröffentlicht.

Die Anwendung kann sowohl lokal als auch in der Cloud betrieben werden.

---

# Projektmitglieder

| Rolle | Aufgabe |
|--------|----------|
| Engineer A | OPC-UA Analyse |
| Engineer B | Datenerfassung |
| Engineer C | Zustandsautomat |
| Engineer E | Flask Backend, REST API, Dashboard, Simulation, Deployment |

---

# Eigener Beitrag (Engineer E)

Im Rahmen dieses Projekts wurden folgende Komponenten entwickelt:

- Flask Backend
- REST API
- CSV-Simulation
- Alarm API
- Dashboard-Anbindung
- Deployment auf Render
- API-Dokumentation
- Integration der Simulationsszenarien

---

# Ausblick

Im nächsten Entwicklungsschritt wird die CSV-Simulation vollständig durch die OPC-UA-Kommunikation ersetzt.

Dadurch werden die Prozessdaten direkt von der Siemens S7-1500 gelesen und in Echtzeit im Dashboard visualisiert.

---

# Lizenz

Dieses Repository wurde ausschließlich im Rahmen eines Hochschulprojekts entwickelt.

© Hochschule Ruhr West – MBSE Projekt 2026
