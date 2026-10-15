import requests
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
# セッション用のシークレット鍵
app.secret_key = "class_1_4_secret_key_999"

# ========================================================
# 🔗 【重要】ここに最新のGASのウェブアプリURLを貼り付けてください！
# ========================================================
GAS_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwNB_sbSf17flMiXR4FX0eOM1V6FH_w3VkKUrY0BNLUMT9JrZ6RouXD5GoQJlk23inM/exec"


# 📊 スプレッドシートからデータを取得する関数
def get_data_from_sheet(sheet_name):
    try:
        response = requests.get(f"{GAS_WEB_APP_URL}?sheet={sheet_name}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
    return []


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    success = None

    # 初期パスワードの準備（通信に失敗したときの保険）
    VIEW_PASSWORD = "1234"
    WRITE_PASSWORD = "abcd"

    # 🔐 スプレッドシートから最新のパスワードを取得して、安全に解析する
    password_data = get_data_from_sheet("passwords")
    if password_data and isinstance(password_data, list) and len(password_data) > 0:
        # 1件目のデータ（2行目の内容）を安全に文字として取り出す
        first_row = password_data[0]
        if isinstance(first_row, dict):
            VIEW_PASSWORD = str(first_row.get("view_password", "1234")).strip()
            WRITE_PASSWORD = str(first_row.get("write_password", "abcd")).strip()

    if request.method == "POST":
        # ① 最初の画面：閲覧許可（ログイン）チェック
        if "login_password" in request.form:
            login_password = request.form.get("login_password").strip()
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
            password = request.form.get("password").strip()

            if password == WRITE_PASSWORD:
                payload = {
                    "action": "add",
                    "sheet": "homework",
                    "subject": subject,
                    "content": content,
                    "belongings": belongings,
                    "deadline": deadline,
                }
                requests.post(GAS_WEB_APP_URL, json=payload)
                return redirect(url_for("index"))
            else:
                error = (
                    "書き込み用の合言葉が違います！ / Incorrect Write Password"
                )

        # ③ 管理者画面：Web上でのパスワード変更処理
        elif "new_view_password" in request.form:
            if not session.get("is_logged_in"):
                return redirect(url_for("index"))

            current_write_pass = request.form.get("current_write_password").strip()
            new_view = request.form.get("new_view_password").strip()
            new_write = request.form.get("new_write_password").strip()

            if current_write_pass == WRITE_PASSWORD:
                payload = {
                    "action": "update_password",
                    "sheet": "passwords",
                    "new_view": new_view,
                    "new_write": new_write,
                }
                requests.post(GAS_WEB_APP_URL, json=payload)
                success = "パスワードを更新しました！ / Passwords updated!"
            else:
                error = (
                    "現在の書き込み合言葉が違います！ / Incorrect Current Password"
                )

    # スプレッドシートから最新の宿題一覧を取得
    homework_list = get_data_from_sheet("homework")
    if not isinstance(homework_list, list):
        homework_list = []

    is_logged_in = session.get("is_logged_in", False)
    return render_template(
        "index.html",
        homework_list=homework_list,
        error=error,
        success=success,
        is_logged_in=is_logged_in,
    )


# ❌ 投稿の削除用処理
@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("is_logged_in"):
        return redirect(url_for("index"))

    VIEW_PASSWORD = "1234"
    WRITE_PASSWORD = "abcd"
    
    password_data = get_data_from_sheet("passwords")
    if password_data and isinstance(password_data, list) and len(password_data) > 0:
        first_row = password_data[0]
        if isinstance(first_row, dict):
            WRITE_PASSWORD = str(first_row.get("write_password", "abcd")).strip()

    password = request.form.get("delete_password").strip()
    if password == WRITE_PASSWORD:
        payload = {"action": "delete", "sheet": "homework", "id": post_id}
        requests.post(GAS_WEB_APP_URL, json=payload)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
