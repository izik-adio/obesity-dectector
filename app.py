from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import xgboost as xgb
import joblib

app = Flask(__name__,static_folder="static",template_folder="templates")

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Extract all form data into a dictionary
        form_data = {
            'Gender': request.form['gender'],
            'Age': float(request.form['age']),
            'Height': float(request.form['height']) / 100,
            'Weight': float(request.form['weight']),
            'family_history_with_overweight': request.form['familyHistory'],
            'FAVC': request.form['caloricFood'],  # Frequent consumption of high-calorie food
            'FCVC': request.form['vegetableConsumption'],  # Frequency of vegetable consumption
            'NCP': request.form['mainMeals'],  # Number of main meals
            'CAEC': request.form['betweenMeals'],  # Consumption of food between meals
            'SMOKE': request.form['smoke'], #smoke
            'CH2O': request.form['water'],  # Daily water intake
            'SCC': request.form['calorieMonitor'],  # Monitoring of calorie consumption
            'FAF': request.form['physicalActivity'],  # Physical activity frequency
            'TUE': request.form['techUsage'],  # Time using technology devices
            'CALC': request.form['alcohol'],  # Alcohol consumption
            'MTRANS': request.form['transportation'],  # Transportation method
        }
        result = predict(form_data)

        return jsonify(result)

    return render_template("index.html")

def predict(data):
    df = pd.DataFrame(data, index=[0])
    df["BMI"] = df["Weight"] / (df["Height"] ** 2)
    cat_cols = ['Gender', 'family_history_with_overweight', 'FAVC', 'FCVC', 'NCP', 'CAEC', 'SMOKE', 'CH2O', 'SCC', 'FAF', 'TUE', 'CALC', 'MTRANS']
    num_cols =  ['Age', 'Height', 'Weight', 'BMI']

    # initialize the required models
    xgb_model = xgb.Booster()
    xgb_model.load_model("./modules/xgb_model.json")
    label_encoder = joblib.load("./modules/label_encoder.pkl")
    one_hot = joblib.load("./modules/one_hot_encoder.pkl")
    scaler = joblib.load("./modules/scaler.pkl")

    # transform data
    df[num_cols] = scaler.transform(df[num_cols])
    inputs_encoded = one_hot.transform(df[cat_cols])
    inputs_encoded = pd.DataFrame.sparse.from_spmatrix(inputs_encoded, index=df.index)
    df = pd.concat((df[num_cols], inputs_encoded), axis=1)
    df = df.astype(pd.SparseDtype("float", 0))

    # predict
    df = xgb.DMatrix(df)
    prediction = xgb_model.predict(df)
    prediction = np.array([np.argmax(prediction)])

    prediction = label_encoder.inverse_transform(prediction)[0]

    recommendations = {
        "Insufficient_Weight": {
            "obesityCategory": "Underweight",
            "advice": "You are classified as underweight. This could be due to nutritional deficiencies or metabolic issues. It's essential to adopt a balanced diet rich in healthy fats, proteins, and carbohydrates. Consider consulting a healthcare provider to identify any underlying causes, and gradually aim to increase your calorie intake by adding nutrient-dense foods such as nuts, avocados, and lean proteins.",
            "reference": "For more information, visit the World Health Organization (WHO) guidelines on maintaining a healthy diet: https://www.who.int/news-room/fact-sheets/detail/healthy-diet"
        },
        "Normal_Weight": {
            "obesityCategory": "Normal Weight",
            "advice": "You are within the normal weight range. To maintain your health, it's important to keep eating a balanced diet with a focus on whole grains, fruits, vegetables, and lean proteins. Regular physical activity, such as 150 minutes of moderate-intensity exercise weekly, will help sustain your fitness. Keep monitoring your weight and continue making healthy lifestyle choices.",
            "reference": "Learn more about healthy living at: https://www.who.int/news-room/fact-sheets/detail/physical-activity"
        },
        "Overweight_Level_I": {
            "obesityCategory": "Overweight Level 1",
            "advice": "You fall into the first level of overweight. It's advisable to begin reducing calorie-dense, nutrient-poor foods such as sugary drinks and processed snacks. Engage in at least 30 minutes of physical activity most days of the week. These changes can help prevent further weight gain and reduce the risk of diseases like diabetes and cardiovascular conditions.",
            "reference": "Check WHO guidelines on weight management: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight"
        },
        "Overweight_Level_II": {
            "obesityCategory": "Overweight Level 2",
            "advice": "You are in the second level of overweight. At this stage, there is an increased risk of health issues, such as type 2 diabetes, heart disease, and musculoskeletal problems. Reducing refined sugars and fats, increasing fiber intake from fruits and vegetables, and incorporating more physical activity (e.g., walking or cycling) into your daily routine is crucial. Consider professional guidance to tailor a sustainable weight loss plan.",
            "reference": "Explore the WHO’s healthy diet advice: https://www.who.int/news-room/fact-sheets/detail/healthy-diet"
        },
        "Obesity_Type_I": {
            "obesityCategory": "Obesity Type 1",
            "advice": "You are classified as Obesity Type I. It's important to seek guidance from healthcare professionals to address your condition and reduce risks of further health complications, such as hypertension and respiratory problems. Start with manageable changes in diet and exercise, like reducing portion sizes and engaging in at least 150 minutes of moderate physical activity weekly.",
            "reference": "For more detailed advice, visit WHO’s recommendations on physical activity: https://www.who.int/news-room/fact-sheets/detail/physical-activity"
        },
        "Obesity_Type_II": {
            "obesityCategory": "Obesity Type 2",
            "advice": "Obesity Type II is associated with significant health risks. You are advised to adopt an aggressive approach towards lifestyle modification, possibly involving both dietary changes and structured physical activity. Seek medical support for developing a customized weight management plan, and explore group-based programs for added motivation and accountability. This can reduce your risk of serious complications like heart disease and certain cancers.",
            "reference": "For more information, refer to WHO guidelines on preventing noncommunicable diseases: https://www.who.int/news-room/fact-sheets/detail/noncommunicable-diseases"
        },
        "Obesity_Type_III": {
            "obesityCategory": "Obesity Type 3",
            "advice": "You fall into the most severe category of obesity, known as Obesity Type III. At this level, it's crucial to take immediate action to reduce your risk of life-threatening conditions such as stroke, liver disease, and cancer. Consult with a healthcare provider to explore a combination of medical, dietary, and possibly surgical interventions. Achieving even a modest weight reduction can significantly improve health outcomes.",
            "reference": "Learn about managing severe obesity at WHO: https://www.who.int/news-room/fact-sheets/detail/obesity-and-overweight"
        }
    }


    return recommendations[prediction]

if __name__ == "__main__":
    app.run(debug=True)