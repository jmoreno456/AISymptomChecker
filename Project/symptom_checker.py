## starter code
## nested dictionaries of symptoms
symptom_disease_dict = {
    "fever": {"flu", "common cold", "malaria"},
    "cough": {"common cold", "bronchitis", "covid-19"},
    "headache": {"migraine", "tension headache", "dehydraytion"},
    "fatigue": {"anemia", "depression", "thyroid issues"},
}


## exit allows clean exit for user
## try/except prevents bad input
def get_user_symptoms():
    """Prompts the user for comma-separated symptoms and returns a list"""
    try:
        user_input = (
            input("\nEnter symptoms separated by commas (or type 'exit' to quit):\n> ")
            .strip()
            .lower()
        )
        if user_input == "exit":
            return None
        if not user_input:
            raise ValueError("Empty input.")
        symptoms = [s.strip() for s in user_input.split(",") if s.strip()]
        if not symptoms:
            raise ValueError("No valid symptoms provided.")
        return symptoms
    except Exception as e:
        print(f"Input error: {e}")
        return []


def find_possible_conditions(symptoms):
    """Takes a list of symptoms and returns a dictionary of matched conditions and unknown symptoms"""
    possible_conditions = set()
    unknown_symptoms = []

    for symptom in symptoms:
        if symptom in symptom_disease_dict:
            possible_conditions.update(symptom_disease_dict[symptom])
        else:
            unknown_symptoms.append(symptom)

    return possible_conditions, unknown_symptoms


def display_results(conditions, unknowns):
    """Displays the matched conditions and unknown symptoms in a readable format"""
    if conditions:
        print("\nPossible conditions based on your symptoms:")
        for condition in sorted(conditions):
            print(f"- {condition}")
    else:
        print("\nNo known conditions matched your symptoms.")

    if unknowns:
        print("\nUnrecognized symptoms:")
        for symptom in unknowns:
            print(f"- {symptom}")


## while loop allows the users to check for symptoms
import os
import json
from datetime import datetime


def save_session(symptoms, conditions, unknowns):
    """Saves the session data (symptoms, conditions, unknowns) to a timestamped JSON file."""
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "symptoms_entered": symptoms,
        "matched_conditions": list(conditions),
        "unknown_symptoms": unknowns,
    }

    filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(log_dir, filename)

    with open(filepath, "w") as file:
        json.dump(log_data, file, indent=2)

    print(f"\nSession saved to {filepath}")


def main():
    """Main loop for running the symptom checker interactively."""
    print("Symptom Checker")

    while True:
        symptoms = get_user_symptoms()
        if symptoms is None:
            break
        elif not symptoms:
            continue

        conditions, unknowns = find_possible_conditions(symptoms)
        display_results(conditions, unknowns)
        save_session(symptoms, conditions, unknowns)


if __name__ == "__main__":
    main()