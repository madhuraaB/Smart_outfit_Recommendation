# train_models.py

import os
import warnings
import joblib
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

warnings.filterwarnings("ignore", category=FutureWarning)

# Use the directory containing this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "body_measurements.csv")

# Required dataset columns
required_columns = [
    "Bust", "Waist", "Hip", "Shoulder",
    "Height", "Gender", "Shape"
]

# Load dataset
try:
    df = pd.read_csv(DATA_PATH)
    print(f"Dataset loaded: {len(df)} samples.")
except FileNotFoundError:
    raise FileNotFoundError(
        "body_measurements.csv not found. "
        "Run generate_dataset.py first."
    )

# Validate dataset
missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    raise ValueError(f"Missing dataset columns: {missing_columns}")

if df.empty:
    raise ValueError("The dataset is empty.")

df = df.dropna(subset=required_columns).copy()

# Prevent division by zero
for col in ["Bust", "Hip"]:
    df[col] = df[col].replace(0, 1)

# Feature engineering
df["Bust_Hip_Ratio"] = df["Bust"] / df["Hip"]
df["Waist_Hip_Ratio"] = df["Waist"] / df["Hip"]
df["Waist_Bust_Ratio"] = df["Waist"] / df["Bust"]
df["Shoulder_Hip_Ratio"] = df["Shoulder"] / df["Hip"]
df["Shoulder_Bust_Ratio"] = df["Shoulder"] / df["Bust"]

# Keep feature order consistent with app.py
features = [
    "Bust_Hip_Ratio",
    "Waist_Hip_Ratio",
    "Waist_Bust_Ratio",
    "Shoulder_Hip_Ratio",
    "Shoulder_Bust_Ratio",
    "Height"
]

target = "Shape"

# Separate datasets by gender
df_female = df[
    df["Gender"].astype(str).str.strip().str.lower() == "female"
].copy()

df_male = df[
    df["Gender"].astype(str).str.strip().str.lower() == "male"
].copy()

if df_female.empty or df_male.empty:
    raise ValueError(
        "Dataset must contain both Female and Male samples."
    )

# Balance classes within each gender
def balance_classes(data):
    max_samples = data[target].value_counts().max()

    return (
        data.groupby(target, group_keys=False)
        .apply(
            lambda group: resample(
                group,
                replace=True,
                n_samples=max_samples,
                random_state=42
            )
        )
        .reset_index(drop=True)
    )

df_female = balance_classes(df_female)
df_male = balance_classes(df_male)

# Train scaler on the six features
X_all = df[features]
scaler = StandardScaler()
scaler.fit(X_all)

joblib.dump(scaler, os.path.join(BASE_DIR, "scaler.pkl"))
print("Scaler saved with", len(features), "features.")

# Train female model
X_female = scaler.transform(df_female[features])
y_female = df_female[target]

model_female = RandomForestClassifier(
    n_estimators=500,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    class_weight="balanced_subsample"
)

model_female.fit(X_female, y_female)

joblib.dump(
    model_female,
    os.path.join(BASE_DIR, "body_shape_model_female.pkl")
)
print("Female model saved.")

# Train male model
X_male = scaler.transform(df_male[features])
y_male = df_male[target]

model_male = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42,
    class_weight="balanced"
)

model_male.fit(X_male, y_male)

joblib.dump(
    model_male,
    os.path.join(BASE_DIR, "body_shape_model_male.pkl")
)
print("Male model saved.")

print("\nTraining completed successfully!")
print("Feature count:", len(features))
print("Scaler expects:", scaler.n_features_in_, "features")
print("Female model expects:", model_female.n_features_in_, "features")
print("Male model expects:", model_male.n_features_in_, "features")
