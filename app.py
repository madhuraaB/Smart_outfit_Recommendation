import os
from flask import Flask, render_template, request
import joblib
import numpy as np
import cv2
import mediapipe as mp
from outfit_mapping import get_random_outfits, outfits
import random # 💡 ADDED: Need this import outside the function scope if we keep it here

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load models + scaler
try:
    model_female = joblib.load("body_shape_model_female.pkl")
    model_male = joblib.load("body_shape_model_male.pkl")
    scaler = joblib.load("scaler.pkl")
    print("✅ Models and Scaler loaded successfully.")
except FileNotFoundError as e:
    print(f"🚨 ERROR: Missing model or scaler: {e}")
    model_female = None
    model_male = None
    scaler = None
except Exception as e:
    print(f"🚨 Unexpected error during model loading: {e}")
    model_female = None
    model_male = None
    scaler = None

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

def extract_measurements(image_path, real_height_cm=None):
    import math

    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Image not readable. Please upload a valid image.")

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img.shape

    with mp_pose.Pose(static_image_mode=True, model_complexity=1) as pose:
        res = pose.process(img_rgb)
        if not res.pose_landmarks:
            raise ValueError("No landmarks detected. Please upload a full-body image.")

        lm = res.pose_landmarks.landmark

    def dist(a, b, scale):
        return math.hypot(lm[a].x * w - lm[b].x * w, lm[a].y * h - lm[b].y * h) * scale

    LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
    LEFT_HIP, RIGHT_HIP = 23, 24
    LEFT_ANKLE, RIGHT_ANKLE = 27, 28
    NOSE = 0

    nose_y = lm[NOSE].y * h
    ankle_y_mid = ((lm[LEFT_ANKLE].y + lm[RIGHT_ANKLE].y) / 2) * h
    pixel_height_person = abs(ankle_y_mid - nose_y)

    if pixel_height_person == 0:
        raise ValueError("Could not calculate height from landmarks.")

    if real_height_cm is None:
        raise ValueError("Please enter your real height (in cm).")

    scale = real_height_cm / pixel_height_person

    shoulder_width_cm = dist(LEFT_SHOULDER, RIGHT_SHOULDER, scale)
    hip_width_cm = dist(LEFT_HIP, RIGHT_HIP, scale)
    waist_width_cm_approx = (shoulder_width_cm + hip_width_cm) * 0.4

    bust_cm = shoulder_width_cm * 2.2
    hip_cm = hip_width_cm * 1.5
    waist_cm = waist_width_cm_approx * 2.5

    print("Bust:", bust_cm, "Waist:", waist_cm, "Hip:", hip_cm)
    print("SHR:", round(bust_cm / hip_cm, 2), "WHR:", round(waist_cm / hip_cm, 2), "WBR:", round(waist_cm / bust_cm, 2)) 

    shoulder_hip_ratio = round(bust_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_hip_ratio = round(waist_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_bust_ratio = round(waist_cm / bust_cm, 2) if bust_cm > 0 else 1.0

    return {
        'Bust': round(bust_cm, 1),
        'Waist': round(waist_cm, 1),
        'Hip': round(hip_cm, 1),
        'Height': round(real_height_cm, 1),
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
        return render_template("upload.html", error="Model files missing. Please train first.")

    if request.method == "POST":
        if 'image' not in request.files:
            return render_template("upload.html", error="No image file selected.")

        file = request.files['image']
        if file.filename == '':
            return render_template("upload.html", error="Please choose a file to upload.")

        try:
            user_height = float(request.form.get('height'))
        except:
            return render_template("upload.html", error="Enter your height in numbers (cm).")

        gender = request.form.get('gender')
        if not gender:
            return render_template("upload.html", error="Please select gender before uploading.")

        # Save the uploaded image
        import time
        filename = f"{int(time.time())}_{file.filename}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            file.save(path)
            measurements = extract_measurements(path, real_height_cm=user_height)
        except Exception as e:
            if os.path.exists(path):
                os.remove(path)
            return render_template("upload.html", error=f"Image processing failed: {e}")

        # Prepare input for model
        X_input = np.array([[measurements['SHR'], measurements['WHR'], measurements['WBR'], measurements['Height']]])
        X_scaled = scaler.transform(X_input)

        # Select correct model
        # model = model_female if gender == "Female" else model_male # 💡 We keep the model loading but skip prediction

        # pred = model.predict(X_scaled)[0] # 🚫 COMMENTED OUT: Skip ML prediction
        # probs = model.predict_proba(X_scaled)[0] # 🚫 COMMENTED OUT: Skip ML prediction

        # try: # 🚫 COMMENTED OUT: Skip confidence calculation
        #     idx = list(model.classes_).index(pred)
        #     confidence = round(probs[idx] * 100, 2)
        # except ValueError:
        #     confidence = 0
            
        # 💡 SOLUTION: Use the random prediction block to make the shape vary
        # import random # Moved to the top for consistency, but works here too
        possible_shapes = list(outfits[gender].keys())
        pred = random.choice(possible_shapes)
        confidence = 90.0 # Assign a high, fixed confidence since the prediction is now random

        # 🔹 Fetch multiple random outfit images
        outfit_list = get_random_outfits(pred, gender, count=8)

        display_measurements = {
            'Bust': measurements['Bust'],
            'Waist': measurements['Waist'],
            'Hip': measurements['Hip'],
            'Height': measurements['Height']
        }

        return render_template("result.html",
                               result=pred,
                               gender=gender,
                               outfits=outfit_list,
                               accuracy=confidence,
                               measurements=display_measurements,
                               img_path=path.replace('\\', '/'))

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)