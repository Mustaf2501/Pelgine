from flask import Flask, redirect, url_for,render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("frontpage.html")


@app.route("/test")
def test():
    return render_template("extendtest.html")


if __name__ == "__main__":
    app.run(debug=True)