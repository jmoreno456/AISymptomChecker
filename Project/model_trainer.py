import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

# Load the dataset
df = pd.read_csv(
    "/Users/jessemoreno/PythonProgramming/Project/data/Symptom2Disease.csv"
)

# Fill NaN with empty string for easier processing
df.fillna("", inplace=True)

# Combine all symptom columns into a list per row
symptom_cols = [col for col in df.columns if col.startswith("Symptom_")]
df["symptoms"] = df[symptom_cols].values.tolist()

# Convert list of symptoms per row into a set to remove duplicates and empty strings
df["symptoms"] = df["symptoms"].apply(
    lambda x: set([symptom.strip() for symptom in x if symptom.strip() != ""])
)

# Prepare X and y
X = df["symptoms"]
y = df["Disease"]

# Use MultiLabelBinarizer to convert symptoms list into binary features
mlb = MultiLabelBinarizer()
X_encoded = mlb.fit_transform(X)

# Save the MultiLabelBinarizer for later use (needed to encode user input)
with open("mlb.pkl", "wb") as f:
    pickle.dump(mlb, f)

# Split dataset (optional, for testing or validation)
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# Train Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model to 'model.pkl'
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Training complete. Model and encoder saved!")