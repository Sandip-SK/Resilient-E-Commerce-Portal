import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Fetch database credentials from Environment Variables (12-Factor App methodology)
DB_HOST = os.environ.get("DB_HOST", "postgres-headless")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASSWORD", "sre-super-secret")
DB_NAME = os.environ.get("DB_NAME", "postgres")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME,
            connect_timeout=3
        )
        return conn
    except Exception as e:
        return None

@app.route('/')
def index():
    return jsonify({"message": "E-Commerce API is Running"}), 200

# Liveness Probe: Tells Kubernetes if the container process is running.
@app.route('/health/live')
def liveness():
    return jsonify({"status": "alive"}), 200

# Readiness Probe: Tells Kubernetes if the app can connect to the database.
@app.route('/health/ready')
def readiness():
    conn = get_db_connection()
    if conn:
        conn.close()
        return jsonify({"status": "ready", "database": "connected"}), 200
    else:
        # If DB is down, return a 503. Kubernetes will temporarily stop sending traffic here.
        return jsonify({"status": "not ready", "database": "disconnected"}), 503

if __name__ == '__main__':
    # Bind to 0.0.0.0 so the container can receive external traffic
    app.run(host='0.0.0.0', port=5000)