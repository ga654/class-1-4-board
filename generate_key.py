from pywebpush import webpush

# VAPIDキーを生成
vapid_keys = webpush.generate_vapid_key()

print("--- 以下の2つをコピーしてください ---")
print("Public Key:", vapid_keys[0])  # 公開鍵
print("Private Key:", vapid_keys[1])  # 秘密鍵