"""
ZJClaw WebUI - Commercial Management AI Assistant Web Interface
"""

import os
import sys
from pathlib import Path

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import httpx

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "zjclaw-webui-secret-key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = Path(__file__).parent / "flask_session"

Session(app)

ZJCLAW_API_URL = os.environ.get("ZJCLAW_API_URL", "http://localhost:18790")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    try:
        response = httpx.post(
            f"{ZJCLAW_API_URL}/chat",
            json={"message": message, "session_id": session.get("session_id", "webui:user")},
            timeout=120.0
        )
        response.raise_for_status()
        return jsonify(response.json())
    except httpx.ConnectError:
        return jsonify({
            "error": "ZJClaw gateway is not running. Please start 'zjclaw gateway' first."
        }), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/status", methods=["GET"])
def status():
    try:
        response = httpx.get(f"{ZJCLAW_API_URL}/status", timeout=5.0)
        return jsonify(response.json())
    except httpx.ConnectError:
        return jsonify({"status": "offline", "message": "ZJClaw gateway is not running"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def create_app():
    Path(app.config["SESSION_FILE_DIR"]).mkdir(parents=True, exist_ok=True)
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
