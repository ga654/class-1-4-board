from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
# セッション（記憶）を使うための秘密の鍵（適当な英数字でOK）
app.secret_key = "class_1_4_secret_key_999"

homework_list = [
    {
        "id": 1,
        "subject": "数学",
        "content": "教科書 P.45 の練習問題 1〜5",
        "belongings": "コンパス、定規",
        "deadline": "2026-10-14",
    }
]

CLASS_PASSWORD = "1234"


@app.route("/", methods=["GET", "POST"])
def index():
    error = None

    # 1. ログイン（閲覧許可）の処理
    if request.method == "POST" and "login_password" in request.form:
        login_password = request.form.get("login_password")
        if login_password == CLASS_PASSWORD:
            session["is_logged_in"] = True
            return redirect(url_for("index"))
        else:
            error = "合言葉が違います！"

    # 2. 新しい宿題の投稿処理
    elif request.method == "POST":
        if not session.get("is_logged_in"):
            return redirect(url_for("index"))

        subject = request.form.get("subject")
        content = request.form.get("content")
        belongings = request.form.get("belongings")
        deadline = request.form.get("deadline")
        password = request.form.get("password")

        if password == CLASS_PASSWORD:
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
            error = "合言葉が違います！投稿できませんでした。"

    # まだ合言葉を入れていない人は、閲覧制限用の画面を表示する
    is_logged_in = session.get("is_logged_in", False)
    return render_template(
        "index.html",
        homework_list=homework_list,
        error=error,
        is_logged_in=is_logged_in,
    )


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("is_logged_in"):
        return redirect(url_for("index"))

    password = request.form.get("delete_password")
    if password == CLASS_PASSWORD:
        global homework_list
        homework_list = [
            post for post in homework_list if post["id"] != post_id
        ]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
