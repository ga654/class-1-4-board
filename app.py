import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "class_1_4_secret_key_999"

DB_NAME = "database.db"


# 🚀 高速化設定（WALモードなど）を適用してDBに接続する関数
def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    # Renderのディスク性能に合わせた高速化設定
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


# データベースの初期化（起動時に自動でテーブルを作成）
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # パスワード管理用テーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            view_password TEXT,
            write_password TEXT
        )
    """)

    # 初期パスワードがなければ登録
    cursor.execute("SELECT COUNT(*) FROM passwords")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO passwords (view_password, write_password) VALUES (?, ?)",
            ("1234", "abcd"),
        )

    # 宿題リスト用テーブル
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS homework (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT,
            content TEXT,
            belongings TEXT,
            deadline TEXT
        )
    """)

    conn.commit()
    conn.close()


# アプリ起動時にDBを準備
init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    success = None

    conn = get_db()
    cursor = conn.cursor()

    # パスワードをデータベースから取得
    cursor.execute("SELECT * FROM passwords LIMIT 1")
    pwd_row = cursor.fetchone()
    VIEW_PASSWORD = pwd_row["view_password"] if pwd_row else "1234"
    WRITE_PASSWORD = pwd_row["write_password"] if pwd_row else "abcd"

    if request.method == "POST":
        if "login_password" in request.form:
            login_password = request.form.get("login_password").strip()
            if login_password == VIEW_PASSWORD:
                session["is_logged_in"] = True
                conn.close()
                return redirect(url_for("index"))
            else:
                error = "合言葉が違います！ / Incorrect Password"

        elif "subject" in request.form:
            if not session.get("is_logged_in"):
                conn.close()
                return redirect(url_for("index"))

            subject = request.form.get("subject")
            content = request.form.get("content")
            belongings = request.form.get("belongings")
            deadline = request.form.get("deadline")
            password = request.form.get("password").strip()

            if password == WRITE_PASSWORD:
                cursor.execute(
                    "INSERT INTO homework (subject, content, belongings, deadline) VALUES (?, ?, ?, ?)",
                    (subject, content, belongings, deadline),
                )
                conn.commit()
                conn.close()
                return redirect(url_for("index"))
            else:
                error = "書き込み用の合言葉が違います！ / Incorrect Write Password"

        elif "new_view_password" in request.form:
            if not session.get("is_logged_in"):
                conn.close()
                return redirect(url_for("index"))

            current_write_pass = request.form.get("current_write_password").strip()
            new_view = request.form.get("new_view_password").strip()
            new_write = request.form.get("new_write_password").strip()

            if current_write_pass == WRITE_PASSWORD:
                cursor.execute(
                    "UPDATE passwords SET view_password = ?, write_password = ? WHERE id = ?",
                    (new_view, new_write, pwd_row["id"]),
                )
                conn.commit()
                success = "パスワードを更新しました！ / Passwords updated!"
            else:
                error = "現在の書き込み合言葉が違います！ / Incorrect Current Password"

    # 宿題リストをデータベースから取得
    cursor.execute("SELECT * FROM homework ORDER BY id DESC")
    homework_rows = cursor.fetchall()
    homework_list = [dict(row) for row in homework_rows]
    conn.close()

    is_logged_in = session.get("is_logged_in", False)
    return render_template(
        "index.html",
        homework_list=homework_list,
        error=error,
        success=success,
        is_logged_in=is_logged_in,
    )


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("is_logged_in"):
        return redirect(url_for("index"))

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM passwords LIMIT 1")
    pwd_row = cursor.fetchone()
    WRITE_PASSWORD = pwd_row["write_password"] if pwd_row else "abcd"

    password = request.form.get("delete_password").strip()
    if password == WRITE_PASSWORD:
        cursor.execute("DELETE FROM homework WHERE id = ?", (post_id,))
        conn.commit()

    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)