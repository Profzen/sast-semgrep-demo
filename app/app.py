from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# ❌ SQL Injection
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = '%s'" % user
    conn = sqlite3.connect("db.sqlite")
    conn.execute(query)
    return "Login OK"

# ❌ Command Injection
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system("ping " + ip)
    return "Ping sent"

# ❌ XSS
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"

if __name__ == "__main__":
    app.run(debug=True)


