from flask import Flask, request, render_template
import requests
app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')
@app.route('/calc', methods=["POST"])
def calc():
    if not request.form.get("input"):
        return render_template('index.html', result = "Không để trống!")
    else:
        resuls=0
        blacklists = ["system","os","popen","commands","subprocess","pty","\\","chr","exec","sys","init","class","base","subclasses","builtins","base64","modules"]
        cal = request.form.get("input")
        for i in blacklists:
            if i in cal.lower():
                return render_template('index.html', result = i)
        resuls = eval(cal)
        return render_template('index.html', result = resuls)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9997)
