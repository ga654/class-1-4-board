from flask import Flask

app = Flask(__name__)

@app.route('/')
def maintenance():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>メンテ中</title>
        <style>
            body {
                /* ヒラギノ丸ゴをはじめとした丸ゴシック系フォントを指定 */
                font-family: "Hiragino Maru Gothic ProN", "ヒラギノ丸ゴ ProN W4", "BIZ UDPGothic", "Meiryo", sans-serif;
                background-color: #f8fafc;
                color: #334155;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                padding: 40px;
                background: white;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            }
            h1 {
                font-size: 1.8rem;
                margin: 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>メンテ中🙇（工事中🚧）</h1>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()