from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

DATABASE = "bmi.db"

# Database initialiseren
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bmi_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                weight REAL,
                height REAL,
                bmi REAL,
                classification TEXT,
                date_time TEXT
            )
        ''')
        conn.commit()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    bmi = None
    advice = ""
    color = ""

    if request.method == "POST":
        try:
            weight = float(request.form["weight"])
            height = float(request.form["height"]) / 100  # Omzetten naar meters
            
            # BMI berekenen
            bmi = round(weight / (height ** 2), 2)

            # Classificatie bepalen
            if bmi < 18.5:
                classification = "Ondergewicht"
                color = "red"
            elif 18.5 <= bmi < 25:
                classification = "Gezond gewicht"
                color = "green"
            elif 25 <= bmi < 30:
                classification = "Overgewicht"
                color = "orange"
            else:
                classification = "Obesitas"
                color = "red"

            advice = f"{classification} - Let op je gezondheid."

            # Huidige datum en tijd
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Gegevens opslaan in database
            with sqlite3.connect(DATABASE) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO bmi_records (weight, height, bmi, classification, date_time)
                    VALUES (?, ?, ?, ?, ?)
                ''', (weight, height * 100, bmi, classification, now))
                conn.commit()

        except ValueError:
            advice = "Ongeldige invoer. Voer alstublieft geldige cijfers in."

    return render_template("index.html", bmi=bmi, advice=advice, color=color)

@app.route("/history")
def history():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT weight, height, bmi, classification, date_time FROM bmi_records ORDER BY date_time DESC")
        records = cursor.fetchall()
    return render_template("history.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
