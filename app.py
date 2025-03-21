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

           
            if bmi < 18.5:
                advice = "Ondergewicht - Probeer meer voedzame maaltijden te eten."
                color = "red"
            elif 18.5 <= bmi < 25:
                advice = "Gezond gewicht - Goed bezig!"
                color = "green"
            elif 25 <= bmi < 30:
                advice = "Overgewicht - Probeer een gebalanceerd dieet en beweging."
                color = "orange"
            else:
                advice = "Obesitas - Overweeg een gezondere levensstijl en raadpleeg een professional."
                color = "red"


        except ValueError:
            advice = "Ongeldige invoer. Voer alstublieft geldige cijfers in."

    return render_template("index.html", bmi=bmi, advice=advice, color=color)


if __name__ == "__main__":
    app.run(debug=True)
