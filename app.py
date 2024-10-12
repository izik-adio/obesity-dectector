from flask import Flask, render_template, request, jsonify

app = Flask(__name__,static_folder="static",template_folder="templates")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extract all form data into a dictionary
        form_data = {
            'gender': request.form['gender'],
            'age': request.form['age'],
            'height': request.form['height'],
            'weight': request.form['weight'],
            'familyHistory': request.form['familyHistory'],
            'caloricFood': request.form['caloricFood'],
            'vegetableConsumption': request.form['vegetableConsumption'],
            'mainMeals': request.form['mainMeals'],
            'betweenMeals': request.form['betweenMeals'],
            'smoke': request.form['smoke'],
            'water': request.form['water'],
            'calorieMonitor': request.form['calorieMonitor'],
            'physicalActivity': request.form['physicalActivity'],
            'techUsage': request.form['techUsage'],
            'alcohol': request.form['alcohol'],
            'transportation': request.form['transportation']
        }
        
        # Return the form data as JSON for AJAX response
        return jsonify(form_data)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

