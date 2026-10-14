from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

# 掲示板のデータを保存するリスト
homework_list = [
    {
        "id": 1,
        "subject": "数学",
        "content": "教科書 P.45 の練習問題 1〜5",
        "belongings": "コンパス、定規",
        "deadline": "2026-10-14",
    }
]

# クラス共通の合言葉
CLASS_PASSWORD = "1234"


# メイン画面（表示と投稿）
@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
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

    return render_template(
        "index.html", homework_list=homework_list, error=error
    )


# ❌ 削除用の処理（ここが足りなかったか、位置がズレていました）
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    password = request.form.get("delete_password")

    if password == CLASS_PASSWORD:
        global homework_list
        homework_list = [
            post for post in homework_list if post["id"] != post_id
        ]

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
