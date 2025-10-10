import os
from flask import Flask, render_template, request
import joblib
import numpy as np
import cv2
import mediapipe as mp
from outfit_mapping import get_random_outfits

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load models + scaler - FINAL CORRECTED BLOCK
try:
    # 🚨 CRITICAL FIX: Use the correct gendered filenames saved by train_model.py
    model_female = joblib.load("body_shape_model_female.pkl") 
    model_male = joblib.load("body_shape_model_male.pkl")     
    scaler = joblib.load("scaler.pkl")
    print("✅ All Models and Scaler loaded successfully. Application is ready.")
except FileNotFoundError as e:
    # This ensures the app doesn't crash immediately but reports the missing file
    print(f"🚨 ERROR: Model or Scaler file not found: {e}. Please run generate_dataset.py and train_model.py first.")
    model_female = None
    model_male = None
    scaler = None
except Exception as e:
    # Catch any other loading issues (e.g., corrupted file)
    print(f"🚨 UNEXPECTED ERROR during model loading: {e}")
    model_female = None
    model_male = None
    scaler = None

mp_pose = mp.solutions.pose

def extract_measurements(image_path, real_height_cm=None):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not readable")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape

    with mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False) as pose:
        res = pose.process(img_rgb)
        if not res.pose_landmarks:
            raise ValueError("No pose landmarks detected. Please upload a full-body image with clear view.")
        lm = res.pose_landmarks.landmark

    def xy(idx):
        return int(lm[idx].x * w), int(lm[idx].y * h)

    LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
    LEFT_HIP, RIGHT_HIP = 23, 24
    LEFT_ANKLE, RIGHT_ANKLE = 27, 28
    NOSE = 0

    coords = {}
    for idx, name in [(LEFT_SHOULDER, 'L_sh'), (RIGHT_SHOULDER, 'R_sh'),
                      (LEFT_HIP, 'L_hip'), (RIGHT_HIP, 'R_hip'),
                      (LEFT_ANKLE, 'L_ank'), (RIGHT_ANKLE, 'R_ank'),
                      (NOSE, 'nose')]:
        coords[name] = xy(idx)

    import math
    def dist(a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    ankle_y = max(coords['L_ank'][1], coords['R_ank'][1])
    pixel_height_person = abs(ankle_y - coords['nose'][1])
    if pixel_height_person == 0:
        pixel_height_person = h

    if real_height_cm is None:
        raise ValueError("Real height (cm) required to scale measurements.")

    scale = real_height_cm / pixel_height_person  # cm per pixel

    # Widths
    shoulder_width_cm = dist(coords['L_sh'], coords['R_sh']) * scale
    hip_width_cm = dist(coords['L_hip'], coords['R_hip']) * scale

    # Estimated Circumferences (Using rough, but consistent, scaling factors)
    bust_cm = shoulder_width_cm * 2.2
    hip_cm = hip_width_cm * 1.5 
    # Approximating waist position and width
    left_waist_x = int((coords['L_sh'][0] + coords['L_hip'][0]) / 2)
    right_waist_x = int((coords['R_sh'][0] + coords['R_hip'][0]) / 2)
    waist_width_cm = abs(right_waist_x - left_waist_x) * scale
    waist_cm = waist_width_cm * 2.5 # circumference scaling factor

    # Calculate Ratios - INPUT FEATURES FOR THE MODEL
    shoulder_hip_ratio = round(bust_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_hip_ratio = round(waist_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_bust_ratio = round(waist_cm / bust_cm, 2) if bust_cm > 0 else 1.0
    
    return {
        # Raw Measurements (for display)
        'Shoulder': round(shoulder_width_cm, 1),
        'Bust': round(bust_cm, 1),
        'Waist': round(waist_cm, 1),
        'Hip': round(hip_cm, 1),
        'Height': round(real_height_cm, 1),
        # Ratios (for model input)
        'SHR': shoulder_hip_ratio,
        'WHR': waist_hip_ratio,
        'WBR': waist_bust_ratio
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if model_female is None or model_male is None or scaler is None:
        return render_template("upload.html", error="System Error: Models not loaded. Please contact administrator.")

    if request.method == "POST":
        # --- Form Validation ---
        if 'image' not in request.files:
            return render_template("upload.html", error="No image file part.")
        file = request.files['image']
        if file.filename == '':
            return render_template("upload.html", error="No selected image.")

        try:
            user_height = float(request.form.get('height'))
        except:
            return render_template("upload.html", error="Please enter your height in cm (numbers only).")

        gender = request.form.get('gender')
        if not gender:
            return render_template("upload.html", error="Please select gender.")
            
        # --- File Save and Measurement Extraction ---
        import time
        filename = f"{int(time.time())}_{file.filename}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(path)
            # Pass user_height to extract measurements and scale
            measurements = extract_measurements(path, real_height_cm=user_height)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            # Display detailed Mediapipe or image error to user
            return render_template("upload.html", error=f"Processing Error: {str(e)}")
        
        # --- Prediction ---
        
        # ⬅️ PREVIOUS CODE: This version includes 'measurements['Height']' as a feature
        X_ratios = np.array([[measurements['SHR'], measurements['WHR'],
                              measurements['WBR'], measurements['Height']]])
                              
        X_scaled = scaler.transform(X_ratios) # Scaling the ratios

        # Choose model based on gender
        if gender == "Female":
            model = model_female
        else:
            model = model_male

        pred = model.predict(X_scaled)[0]
        probs = model.predict_proba(X_scaled)[0]
        
        try:
            idx = list(model.classes_).index(pred)
            confidence = round(probs[idx] * 100, 2)
        except ValueError:
            confidence = 0 # Fallback if prediction class is not in classes_

        # --- Recommendation and Result ---
        outfits = get_random_outfits(pred, gender, count=5)

        return render_template("result.html",
                               result=pred,
                               gender=gender,
                               outfits=outfits,
                               accuracy=confidence,
                               # Pass raw measurements for display, excluding the ratios
                               measurements={k: v for k, v in measurements.items() if k not in ['SHR', 'WHR', 'WBR']},
                               img_path=path.replace('\\', '/'))

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
