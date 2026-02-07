from flask import Flask

app = Flask(__name__)

from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = "db/users.db"

@app.route("/register", methods=["POST"])
def api_register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        con.close()
        return jsonify({"success": True})
    except:
        con.close()
        return jsonify({"success": False, "error": "ユーザー名が既に使われています"})
        @app.route("/login", methods=["POST"])
def api_login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    result = cur.fetchone()
    con.close()

    if result:
        user_id = result[0]
        return jsonify({"success": True, "user_id": user_id})
    else:
        return jsonify({"success": False})
        @app.route("/verify", methods=["POST"])
def api_verify():
    data = request.json
    user_id = data.get("user_id")

    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
    result = cur.fetchone()
    con.close()

    if result:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})
        
