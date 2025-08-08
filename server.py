from flask import Flask, request, jsonify, send_from_directory, render_template
import json
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

CONFIG_PATH = "config.json"

def cargar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_config(data):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/config")
def get_config():
    try:
        config = cargar_config()
        return jsonify(config)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/update_config", methods=["POST"])
def update_config():
    try:
        new_config = request.get_json()
        if new_config.get("password") != "admin":
            return jsonify({"error": "Unauthorized"}), 403

        guardar_config({
            "welcome_message": new_config.get("welcome_message"),
            "dice_faces": new_config.get("dice_faces")
        })
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)