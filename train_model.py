# train_models.py
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import joblib
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

try:
    df = pd.read_csv('body_shapes_dataset_gendered.csv')
    print(f"Dataset loaded: {len(df)} samples.")
except FileNotFoundError:
    print("🚨 ERROR: body_shapes_dataset_gendered.csv not found. Please run generate_dataset.py first.")
    exit()

# --- Feature Engineering: Create Ratios (CRITICAL STEP) ---
df['SHR'] = df['Bust'] / df['Hip']      # Shoulder-Hip Ratio (Bust proxy)
df['WHR'] = df['Waist'] / df['Hip']      # Waist-Hip Ratio
df['WBR'] = df['Waist'] / df['Bust']     # Waist-Bust Ratio

# Features for high-confidence training are the Ratios and Height
features = ['SHR', 'WHR', 'WBR', 'Height']
target = 'BodyShape'

df_female = df[df['Gender'] == 'Female'].copy()
df_male = df[df['Gender'] == 'Male'].copy()

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
# Using n_estimators=300 increases model robustness and confidence.

print("\n--- Training Female Model (Ratio-Based) ---")
model_female = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42, class_weight='balanced')
model_female.fit(X_female, y_female)
joblib.dump(model_female, 'body_shape_model_female.pkl')
print("✅ Female Model saved: body_shape_model_female.pkl")

print("\n--- Training Male Model (Ratio-Based) ---")
model_male = RandomForestClassifier(n_estimators=300, max_depth=10, random_state=42, class_weight='balanced')
model_male.fit(X_male, y_male)
joblib.dump(model_male, 'body_shape_model_male.pkl')
print("✅ Male Model saved: body_shape_model_male.pkl")