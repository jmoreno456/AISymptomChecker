import pandas as pd
import pickle

# Load your dataset
df = pd.read_csv(
    "/Users/jessemoreno/PythonProgramming/Project/data/Symptom2Disease.csv"
)

# Get all symptom columns (e.g., Symptom_1 to Symptom_17)
symptom_columns = [col for col in df.columns if col.startswith("Symptom")]

# Flatten all symptom values and remove NaN
symptoms = pd.unique(df[symptom_columns].values.ravel())
symptom_list = sorted([s.strip() for s in symptoms if pd.notna(s)])

# Save to pickle
with open("symptom_list.pkl", "wb") as f:
    pickle.dump(symptom_list, f)

print("✅ symptom_list.pkl saved!")
