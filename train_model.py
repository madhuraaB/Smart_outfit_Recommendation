# train_models.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

try:
    df = pd.read_csv('body_measurements.csv')
    print(f"Dataset loaded: {len(df)} samples.")
except FileNotFoundError:
    print("🚨 ERROR: body_shapes_dataset_gendered.csv not found. Please run generate_dataset.py first.")
    exit()
df['Hip'] = df['Hip'].replace(0, 1)
df['Bust'] = df['Bust'].replace(0, 1)
# -------- Feature Engineering --------
# Ratios
df['Bust_Hip_Ratio'] = df['Bust'] / df['Hip']
df['Waist_Hip_Ratio'] = df['Waist'] / df['Hip']
df['Waist_Bust_Ratio'] = df['Waist'] / df['Bust']
df['Shoulder_Hip_Ratio'] = df['Shoulder'] / df['Hip']
df['Shoulder_Bust_Ratio'] = df['Shoulder'] / df['Bust']

# Features for high-confidence training are the Ratios and Height
features = [
    'Bust_Hip_Ratio',
    'Waist_Hip_Ratio',
    'Waist_Bust_Ratio',
    'Shoulder_Hip_Ratio',
    'Shoulder_Bust_Ratio',
    'Height'
]
target = 'Shape'

df_female = df[df['Gender'] == 'Female'].copy()
df_male = df[df['Gender'] == 'Male'].copy()
from sklearn.utils import resample

# Balance female data
df_female = df_female.groupby('Shape', group_keys=False).apply(
    lambda x: resample(x, replace=True, 
                       n_samples=df_female['Shape'].value_counts().max(), 
                       random_state=42)
)

# Balance male data
df_male = df_male.groupby('Shape', group_keys=False).apply(
    lambda x: resample(x, replace=True, 
                       n_samples=df_male['Shape'].value_counts().max(), 
                       random_state=42)
)


# --- 1. Scaling ---
X_all = df[features]
scaler = StandardScaler()
scaler.fit(X_all)
joblib.dump(scaler, 'scaler.pkl')
print("✅ Scaler saved: scaler.pkl (Trained on Ratios)")

X_female = scaler.transform(df_female[features])
y_female = df_female[target]
X_male = scaler.transform(df_male[features])
y_male = df_male[target]

# --- 2. Model Training (RandomForestClassifier with high estimators) ---

print("\n--- Training Female Model (Ratio-Based) ---")
model_female =RandomForestClassifier(
    n_estimators=500,
    max_depth=12,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    class_weight='balanced_subsample'
)
model_female.fit(X_female, y_female)
joblib.dump(model_female, 'body_shape_model_female.pkl')
print("✅ Female Model saved: body_shape_model_female.pkl")

print("\n--- Training Male Model (Ratio-Based) ---")
model_male = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42, class_weight='balanced')
model_male.fit(X_male, y_male)
joblib.dump(model_male, 'body_shape_model_male.pkl')
print("✅ Male Model saved: body_shape_model_male.pkl")