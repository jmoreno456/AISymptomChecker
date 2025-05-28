from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load trained model and list of symptoms
model = pickle.load(open("model.pkl", "rb"))
symptom_list = pickle.load(open("symptom_list.pkl", "rb"))


@app.route("/")
def home():
    return render_template("index.html", symptom_list=symptom_list)


@app.route("/predict", methods=["POST"])
def predict():
    selected_symptoms = request.form.getlist("selected_symptoms")
    additional_symptoms_raw = request.form.get("additional_symptoms", "")
    additional_symptoms = [
        s.strip().lower() for s in additional_symptoms_raw.split(",") if s.strip()
    ]

    # Combine all symptoms
    all_input_symptoms = [s.lower() for s in selected_symptoms] + additional_symptoms

    # Create binary input vector
    input_vector = [
        1 if symptom.lower() in all_input_symptoms else 0 for symptom in symptom_list
    ]

    # Predict probabilities
    probabilities = model.predict_proba([input_vector])[0]
    top_indices = np.argsort(probabilities)[::-1][:5]
    top_diseases = [
        (model.classes_[i], round(probabilities[i] * 100, 2)) for i in top_indices
    ]

    return render_template(
        "result.html", top_diseases=top_diseases, symptoms=all_input_symptoms
    )


if __name__ == "__main__":
    app.run(debug=True)