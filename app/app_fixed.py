"""
app_fixed.py - Version sécurisée de app.py
Copiez ce contenu dans app.py pour le 2e push de la démo
"""

from flask import Flask, request, render_template_string
from markupsafe import escape
import sqlite3
import subprocess
import os

app = Flask(__name__)

# ✅ SÉCURISÉ : SQL Injection - Requête paramétrée
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = ?"
    conn = sqlite3.connect("db.sqlite")
    cursor = conn.execute(query, (user,))
    result = cursor.fetchone()
    if result:
        return "Login OK"
    return "User not found"

# ✅ SÉCURISÉ : Command Injection - subprocess avec liste
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    try:
        result = subprocess.run(
            ["ping", "-c", "4", ip],
            capture_output=True,
            text=True,
            timeout=10,
            check=True
        )
        return f"<pre>{escape(result.stdout)}</pre>"
    except subprocess.CalledProcessError:
        return "Ping failed"
    except subprocess.TimeoutExpired:
        return "Ping timeout"

# ✅ SÉCURISÉ : XSS - Jinja2 avec échappement automatique
@app.route("/hello")
def hello():
    name = request.args.get("name", "Guest")
    template = "<h1>Hello {{ name }}</h1>"
    return render_template_string(template, name=name)

if __name__ == "__main__":
    # ✅ SÉCURISÉ : Debug désactivé en production
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    app.run(debug=debug_mode)
