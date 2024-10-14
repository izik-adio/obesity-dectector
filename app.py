from flask import Flask, render_template, request, jsonify
from prediction import advice

app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Extract all form data into a dictionary
        form_data = {
            "Gender": request.form["gender"],
            "Age": float(request.form["age"]),
            "Height": float(request.form["height"]) / 100,
            "Weight": float(request.form["weight"]),
            "family_history_with_overweight": request.form["familyHistory"],
            "FAVC": request.form[
                "caloricFood"
            ],  # Frequent consumption of high-calorie food
            "FCVC": request.form[
                "vegetableConsumption"
            ],  # Frequency of vegetable consumption
            "NCP": request.form["mainMeals"],  # Number of main meals
            "CAEC": request.form["betweenMeals"],  # Consumption of food between meals
            "SMOKE": request.form["smoke"],  # smoke
            "CH2O": request.form["water"],  # Daily water intake
            "SCC": request.form["calorieMonitor"],  # Monitoring of calorie consumption
            "FAF": request.form["physicalActivity"],  # Physical activity frequency
            "TUE": request.form["techUsage"],  # Time using technology devices
            "CALC": request.form["alcohol"],  # Alcohol consumption
            "MTRANS": request.form["transportation"],  # Transportation method
        }

        result = jsonify(advice(form_data))

        return result

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
