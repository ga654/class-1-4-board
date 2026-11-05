from flask import Flask

app = Flask(__name__)

@app.route('/')
def maintenance():
    return "メンテ中🙇（工事中🚧）"

if __name__ == '__main__':
    app.run()