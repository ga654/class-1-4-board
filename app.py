import os
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "class_1_4_secret_key_999"

# 掲示板データ
homework_list = [
    {
        "id": 1,
        "subject": "数学",
        "content": "教科書 P.45 の練習問題 1〜5",
        "belongings": "コンパス、定規",
        "deadline": "2026-10-14",
    }
]

PASSWORD_FILE = "passwords.txt"


# 🔐 パスワードをファイルから読み込む関数（バグを修正しました！）
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r", encoding="utf-8") as f:
            data = f.read().strip().split(",")
            if len(data) == 2:
                return data[0], data[1]  # ⭕️ 正しく閲覧用と書き込み用を分けて返します
    return "1234", "abcd"  # ファイルがない場合の初期値


# 💾 新しいパスワードをファイルに保存する関数
def save_passwords(view_pass, write_pass):
    with open(PASSWORD_FILE, "w", encoding="utf-8") as f:
        f.write(f"{view_pass},{write_pass}")


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    success = None
    VIEW_PASSWORD, WRITE_PASSWORD = load_passwords()

    if request.method == "POST":
        # ① 最初の画面：閲覧許可（ログイン）チェック
        if "login_password" in request.form:
            login_password = request.form.get("login_password")
            if login_password == VIEW_PASSWORD:
                session["is_logged_in"] = True
                return redirect(url_for("index"))
            else:
                error = "合言葉が違います！ / Incorrect Password"

        # ② 掲示板：新しい宿題の投稿処理
        elif "subject" in request.form:
            if not session.get("is_logged_in"):
                return redirect(url_for("index"))

            subject = request.form.get("subject")
            content = request.form.get("content")
            belongings = request.form.get("belongings")
            deadline = request.form.get("deadline")
            password = request.form.get("password")

            if password == WRITE_PASSWORD:
                new_post = {
                    "id": len(homework_list) + 1,
                    "subject": subject,
                    "content": content,
                    "belongings": belongings,
                    "deadline": deadline,
                }
                homework_list.insert(0, new_post)
                return redirect(url_for("index"))
            else:
                error = (
                    "書き込み用の合言葉が違います！ / Incorrect Write Password"
                )

        # ③ 管理者画面：Web上でのパスワード変更処理
        elif "new_view_password" in request.form:
            if not session.get("is_logged_in"):
                return redirect(url_for("index"))

            current_write_pass = request.form.get("current_write_password")
            new_view = request.form.get("new_view_password")
            new_write = request.form.get("new_write_password")

            if current_write_pass == WRITE_PASSWORD:
                save_passwords(new_view, new_write)
                success = "パスワードを更新しました！ / Passwords updated!"
            else:
                error = (
                    "現在の書き込み合言葉が違います！ / Incorrect Current Password"
                )

    is_logged_in = session.get("is_logged_in", False)
    return render_template(
        "index.html",
        homework_list=homework_list,
        error=error,
        success=success,
        is_logged_in=is_logged_in,
    )


# ❌ 投稿の削除（消去）用処理
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("is_logged_in"):
        return redirect(url_for("index"))

    _, WRITE_PASSWORD = load_passwords()
    password = request.form.get("delete_password")
    if password == WRITE_PASSWORD:
        global homework_list
        homework_list = [
            post for post in homework_list if post["id"] != post_id
        ]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
