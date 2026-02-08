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
@app.route("/board/new", methods=["POST"])
def api_new_thread():
    data = request.json
    title = data.get("title")
    user_id = data.get("user_id")

    con = sqlite3.connect("db/threads.db")
    cur = con.cursor()
    cur.execute("INSERT INTO threads (title, user_id) VALUES (?, ?)", (title, user_id))
    con.commit()
    con.close()

    return jsonify({"success": True})
    @app.route("/board/post", methods=["POST"])
def api_post():
    data = request.json
    thread_id = data.get("thread_id")
    user_id = data.get("user_id")
    content = data.get("content")

    con = sqlite3.connect("db/threads.db")
    cur = con.cursor()
    cur.execute("INSERT INTO posts (thread_id, user_id, content) VALUES (?, ?, ?)",
                (thread_id, user_id, content))
    con.commit()
    con.close()

    return jsonify({"success": True})
    @app.route("/board/thread", methods=["POST"])
def api_get_thread():
    data = request.json
    thread_id = data.get("thread_id")

    con = sqlite3.connect("db/threads.db")
    cur = con.cursor()

    # スレ情報
    cur.execute("SELECT title FROM threads WHERE id=?", (thread_id,))
    thread = cur.fetchone()

    # 投稿一覧
    cur.execute("SELECT user_id, content FROM posts WHERE thread_id=?", (thread_id,))
    posts = cur.fetchall()

    con.close()

    return jsonify({
        "success": True,
        "title": thread[0],
        "posts": posts
    })
    
    if result:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})
       @app.route("/profile/get", methods=["POST"])
def api_profile_get():
    data = request.json
    user_id = data.get("user_id")

    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    cur.execute("SELECT username, bio FROM users WHERE id=?", (user_id,))
    result = cur.fetchone()
    con.close()

    if result:
        return jsonify({
            "success": True,
            "username": result[0],
            "bio": result[1]
        })
    else:
        return jsonify({"success": False})
        @app.route("/profile/update", methods=["POST"])
def api_profile_update():
    data = request.json
    user_id = data.get("user_id")
    bio = data.get("bio")

    con = sqlite3.connect("db/users.db")
    cur = con.cursor()
    cur.execute("UPDATE users SET bio=? WHERE id=?", (bio, user_id))
    con.commit()
    con.close()

    return jsonify({"success": True})
ADMIN_TOKEN = "Mitsuba38JGR"

@app.route("/admin/token", methods=["POST"])
def api_admin_token():
    data = request.json
    token = data.get("token")

    if token == ADMIN_TOKEN:
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})
