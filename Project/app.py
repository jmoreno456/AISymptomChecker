from flask import Flask, render_template, request
import pickle
import numpy as np
from rapidfuzz import process, fuzz

app = Flask(__name__)

# Load trained model and MultiLabelBinarizer
model = pickle.load(open("model.pkl", "rb"))
mlb = pickle.load(open("mlb.pkl", "rb"))

# Extract symptom list from mlb classes for consistent encoding
symptom_list = list(mlb.classes_)


def fuzzy_match_symptoms(user_symptoms, symptom_list, threshold=80):
    """
    For each user symptom, find the best fuzzy match in symptom_list above a similarity threshold.
    Return list of matched symptoms (or empty if none pass threshold).
    """
    matched = []
    for symptom in user_symptoms:
        if not symptom.strip():
            continue
        # Find best match with score
        best_match, score, _ = process.extractOne(
            symptom.lower(), symptom_list, scorer=fuzz.token_sort_ratio
        )
        if score >= threshold:
            matched.append(best_match)
        else:
            pass
    return matched


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

    # Combine all user input symptoms
    all_input_symptoms_raw = [
        s.lower() for s in selected_symptoms
    ] + additional_symptoms

    # Apply fuzzy matching to map user symptoms to known symptoms in symptom_list
    all_input_symptoms = fuzzy_match_symptoms(all_input_symptoms_raw, symptom_list)

    if not all_input_symptoms:
        # No valid symptoms matched, return with error message or prompt
        return render_template(
            "result.html",
            top_diseases=[],
            symptoms=[],
            error_message="No recognizable symptoms entered. Please try again.",
        )

    # Use MultiLabelBinarizer to encode input symptoms to model input vector
    input_vector = mlb.transform([all_input_symptoms])

    # Predict probabilities
    probabilities = model.predict_proba(input_vector)[0]
    top_indices = np.argsort(probabilities)[::-1][:5]
    top_diseases = [
        (model.classes_[i], round(probabilities[i] * 100, 2)) for i in top_indices
    ]

    return render_template(
        "result.html",
        top_diseases=top_diseases,
        symptoms=all_input_symptoms,
        error_message=None,
    )


if __name__ == "__main__":
    app.run(debug=True)
