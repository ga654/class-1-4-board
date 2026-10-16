import json
import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from pywebpush import WebPushException, webpush

app = Flask(__name__)
app.secret_key = "class_1_4_secret_key_999"

# ========================================================
# 🔗 Supabase ＆ プッシュ通知（VAPID）の設定
# ========================================================
SUPABASE_URL = "https://lhdalwtppyufudtjkxtk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxoZGFsd3RwcHl1ZnVkdGpreHRrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTIxNTA2NzMsImV4cCI6MjEwNzcyNjY3M30.I5ePEyIV3o6tUNyf7zq78SC1MdMYMK4nBKm2057Onjg"

# 🔑 【ここにさっき取得した鍵を貼り付けてください】
VAPID_PUBLIC_KEY = "BIaxU3i84TQorBGdAXL0IWaCXVjNAgaDM5p8rHdWGG19ZLhn3WOmaI2yMHP7pfR-ehpsD6R0oi0bUXDroyGuNak"
VAPID_PRIVATE_KEY = "zGVHtLa6eKh3k0uJfE7x0vcL_efXh27cdAP7tOhfCWg"
VAPID_CLAIMS = {"sub": "mailto:admin@example.com"}

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}


def get_data_from_supabase(table_name):
    try:
        response = requests.get(
            f"{SUPABASE_URL}/rest/v1/{table_name}?select=*",
            headers=HEADERS,
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching data: {e}")
    return []


def send_push_notification(title, body):
    subscriptions = get_data_from_supabase("subscriptions")
    for sub in subscriptions:
        subscription_info = {
            "endpoint": sub.get("endpoint"),
            "keys": {"p256dh": sub.get("p256dh"), "auth": sub.get("auth")},
        }
        try:
            webpush(
                subscription_info=subscription_info,
                data=json.dumps({"title": title, "body": body}),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS,
            )
        except Exception as e:
            print(f"Push notification error: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    success = None

    password_data = get_data_from_supabase("passwords")
    VIEW_PASSWORD = "1234"
    WRITE_PASSWORD = "abcd"
    pwd_id = None
    if password_data and len(password_data) > 0:
        VIEW_PASSWORD = str(password_data[0].get("view_password", "1234")).strip()
        WRITE_PASSWORD = str(password_data[0].get("write_password", "abcd")).strip()
        pwd_id = password_data[0].get("id")

    if request.method == "POST":
        if "login_password" in request.form:
            login_password = request.form.get("login_password").strip()
            if login_password == VIEW_PASSWORD:
                session["is_logged_in"] = True
                return redirect(url_for("index"))
            else:
                error = "合言葉が違います！ / Incorrect Password"

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
                    "subject": subject,
                    "content": content,
                    "belongings": belongings,
                    "deadline": deadline,
                }
                try:
                    requests.post(
                        f"{SUPABASE_URL}/rest/v1/homework",
                        json=payload,
                        headers=HEADERS,
                        timeout=5,
                    )
                    send_push_notification(
                        "新しい宿題が追加されました！",
                        f"教科: {subject}\n内容: {content}",
                    )
                except Exception as e:
                    print(f"Error posting: {e}")
                return redirect(url_for("index"))
            else:
                error = "書き込み用の合言葉が違います！ / Incorrect Write Password"

        elif "new_view_password" in request.form:
            if not session.get("is_logged_in"):
                return redirect(url_for("index"))

            current_write_pass = request.form.get("current_write_password").strip()
            new_view = request.form.get("new_view_password").strip()
            new_write = request.form.get("new_write_password").strip()

            if current_write_pass == WRITE_PASSWORD:
                payload = {"view_password": new_view, "write_password": new_write}
                try:
                    requests.patch(
                        f"{SUPABASE_URL}/rest/v1/passwords?id=eq.{pwd_id}",
                        json=payload,
                        headers=HEADERS,
                        timeout=5,
                    )
                    success = "パスワードを更新しました！ / Passwords updated!"
                except Exception as e:
                    error = "通信エラーが発生しました / Connection Error"
                    print(f"Error updating password: {e}")
            else:
                error = "現在の書き込み合言葉が違います！ / Incorrect Current Password"

    homework_list = get_data_from_supabase("homework")
    if not isinstance(homework_list, list):
        homework_list = []
    homework_list = sorted(
        homework_list, key=lambda x: x.get("id", 0), reverse=True
    )

    is_logged_in = session.get("is_logged_in", False)
    return render_template(
        "index.html",
        homework_list=homework_list,
        error=error,
        success=success,
        is_logged_in=is_logged_in,
        vapid_public_key=VAPID_PUBLIC_KEY,
    )


@app.route("/save-subscription", methods=["POST"])
def save_subscription():
    sub_data = request.get_json()
    endpoint = sub_data.get("endpoint")
    keys = sub_data.get("keys", {})
    p256dh = keys.get("p256dh")
    auth = keys.get("auth")

    payload = {"endpoint": endpoint, "p256dh": p256dh, "auth": auth}
    try:
        requests.post(
            f"{SUPABASE_URL}/rest/v1/subscriptions",
            json=payload,
            headers=HEADERS,
            timeout=5,
        )
        return jsonify({"success": True})
    except Exception as e:
        print(f"Error saving subscription: {e}")
        return jsonify({"success": False}), 500


@app.route("/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    if not session.get("is_logged_in"):
        return redirect(url_for("index"))

    password_data = get_data_from_supabase("passwords")
    WRITE_PASSWORD = (
        str(password_data[0].get("write_password", "abcd")).strip()
        if password_data
        else "abcd"
    )

    password = request.form.get("delete_password").strip()
    if password == WRITE_PASSWORD:
        try:
            requests.delete(
                f"{SUPABASE_URL}/rest/v1/homework?id=eq.{post_id}",
                headers=HEADERS,
                timeout=5,
            )
        except Exception as e:
            print(f"Error deleting: {e}")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)