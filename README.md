# Brauanlage API

Flask REST API for the Digital Twin of the HRW brewery system.

## Endpoints

### GET /
Returns API status.

### GET /api/status
Returns the latest process values from `data.csv`.

### GET /api/history
Returns historical process values from `data.csv`.

### POST /api/control
Receives control commands for pump, heater or stirrer.

## Architecture

CSV data → Flask API → REST endpoints → Lovable/Vercel Dashboard

## Run locally

```bash
pip install -r requirements.txt
python app.py
