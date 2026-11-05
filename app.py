from flask import Flask

app = Flask(__name__)

@app.route('/')
def maintenance():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>1-4組 黒板掲示板</title>
        <!-- Google Fontsから Zen Kurenaido を読み込み -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Zen+Kurenaido&display=swap" rel="stylesheet">
        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }
            body {
                background-color: #1a1a1a;
                font-family: 'Zen Kurenaido', sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            /* 木枠フレーム付きの黒板 */
            .blackboard {
                background-color: #1d3c28;
                background-image: 
                    radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 80%),
                    repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0, 0, 0, 0.03) 2px, rgba(0, 0, 0, 0.03) 4px);
                border: 12px solid #5c3a21;
                border-radius: 8px;
                box-shadow: 
                    inset 0 0 20px rgba(0, 0, 0, 0.8),
                    0 10px 30px rgba(0, 0, 0, 0.5);
                max-width: 520px;
                width: 100%;
                padding: 40px 30px;
                color: #f0f4f1;
                position: relative;
            }

            /* チョーク文字の効果（白いボカシ） */
            .chalk-text {
                color: rgba(255, 255, 255, 0.9);
                text-shadow: 
                    0 0 2px rgba(255, 255, 255, 0.6),
                    1px 1px 1px rgba(0, 0, 0, 0.5);
                letter-spacing: 0.08em;
            }

            /* 日直コーナー風の見出し */
            .header-box {
                border: 2px dashed rgba(255, 255, 255, 0.4);
                padding: 8px 16px;
                display: inline-block;
                margin-bottom: 24px;
                transform: rotate(-1deg);
            }

            h1 {
                font-size: 1.8rem;
                margin-bottom: 16px;
            }

            p {
                font-size: 1.1rem;
                line-height: 1.8;
                color: rgba(255, 255, 255, 0.85);
            }

            /* 黄色チョークのアクセント */
            .yellow-chalk {
                color: #fef08a;
                text-shadow: 0 0 2px rgba(254, 240, 138, 0.6);
            }

            /* 黒板消し＆チョークの粉受け（下部の台） */
            .chalk-tray {
                position: absolute;
                bottom: -18px;
                left: 10%;
                right: 10%;
                height: 8px;
                background: #3d2314;
                border-radius: 2px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.4);
            }
        </style>
    </head>
    <body>
        <div class="blackboard">
            <div class="header-box chalk-text">
                📌 本日の連絡事項
            </div>
            <h1 class="chalk-text yellow-chalk">【1-4組 掲示板】改修工事中！</h1>
            <p class="chalk-text">
                ただいま新しいクラス掲示板を作成しています。<br>
                完成まで黒板の前で少々お待ちください 🧹✨
            </p>
            <div class="chalk-tray"></div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run()