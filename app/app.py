from flask import Flask, request, render_template_string
import sqlite3
import os
import subprocess
import pickle

app = Flask(__name__)

#  SQL Injection - String formatting
@app.route("/login")
def login():
    user = request.args.get("user")
    query = "SELECT * FROM users WHERE username = '%s'" % user
    conn = sqlite3.connect("db.sqlite")
    conn.execute(query)
    return "Login OK"

#  SQL Injection - f-string
@app.route("/search")
def search():
    term = request.args.get("q")
    conn = sqlite3.connect("db.sqlite")
    conn.execute(f"SELECT * FROM products WHERE name = '{term}'")
    return "Search OK"

#  SQL Injection - Concaténation
@app.route("/delete")
def delete():
    user_id = request.args.get("id")
    conn = sqlite3.connect("db.sqlite")
    conn.execute("DELETE FROM users WHERE id = " + user_id)
    return "Deleted"

#  SQL Injection - Autre pattern
@app.route("/update")
def update():
    email = request.args.get("email")
    conn = sqlite3.connect("db.sqlite")
    query = "UPDATE users SET email = '" + email + "'"
    conn.execute(query)
    return "Updated"

# ❌ Command Injection - os.system avec concaténation
@app.route("/ping")
def ping():
    ip = request.args.get("ip")
    os.system("ping " + ip)
    return "Ping sent"

#  Command Injection - os.system avec f-string
@app.route("/nslookup")
def nslookup():
    domain = request.args.get("domain")
    os.system(f"nslookup {domain}")
    return "DNS lookup done"

#  Command Injection - subprocess avec shell=True et f-string
@app.route("/curl")
def curl():
    url = request.args.get("url")
    subprocess.run(f"curl {url}", shell=True)
    return "Request sent"

#  Command Injection - subprocess.call avec shell=True
@app.route("/wget")
def wget():
    file_url = request.args.get("file")
    subprocess.call("wget " + file_url, shell=True)
    return "Download started"

#  XSS - f-string avec HTML
@app.route("/hello")
def hello():
    name = request.args.get("name")
    return f"<h1>Hello {name}</h1>"

#  XSS - Concaténation HTML
@app.route("/welcome")
def welcome():
    username = request.args.get("user")
    return "<div>Welcome " + username + "</div>"

#  XSS - render_template_string avec concaténation
@app.route("/greet")
def greet():
    msg = request.args.get("msg")
    return render_template_string("<p>Message: " + msg + "</p>")
    #pc2

#  Désérialisation dangereuse - pickle.loads
@app.route("/load_data")
def load_data():
    data = request.args.get("data")
    obj = pickle.loads(data.encode())
    return f"Loaded: {obj}"

#  Désérialisation dangereuse - pickle.load
@app.route("/load_file")
def load_file():
    filename = request.args.get("file")
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    return f"Loaded: {obj}"

if __name__ == "__main__":
    app.run(debug=True)
