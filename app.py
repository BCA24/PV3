from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    advice = ""
    color = ""

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"]) / 100  
            
            
            bmi = round(weight / (height ** 2), 2)

