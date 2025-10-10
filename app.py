import os
from flask import Flask, render_template, request
import joblib
import numpy as np
import cv2
import mediapipe as mp
from outfit_mapping import get_random_outfits

UPLOAD_FOLDER = 'static/uploads'
# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Load models + scaler - CRITICAL FIX FOR STARTUP CRASH
try:
    # 🚨 FIX 1: Use the correct gendered filenames saved by train_model.py
    model_female = joblib.load("body_shape_model_female.pkl") 
    model_male = joblib.load("body_shape_model_male.pkl")     
    scaler = joblib.load("scaler.pkl")
    print("✅ All Models and Scaler loaded successfully. Application is ready.")
except FileNotFoundError as e:
    # FIX 2: Graceful error handling prevents the script from stopping before mp is defined
    print(f"🚨 ERROR: Model or Scaler file not found: {e}. Please run generate_dataset.py and train_model.py first.")
    model_female = None
    model_male = None
    scaler = None
except Exception as e:
    print(f"🚨 UNEXPECTED ERROR during model loading: {e}")
    model_female = None
    model_male = None
    scaler = None

# Initialize MediaPipe outside the function for performance
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

    def dist(a, b, scale):
        # Calculate Euclidean distance between two landmark points (x,y) and scale it to cm
        return math.hypot(lm[a].x * w - lm[b].x * w, lm[a].y * h - lm[b].y * h) * scale

    import math
    
    LEFT_SHOULDER, RIGHT_SHOULDER = 11, 12
    LEFT_HIP, RIGHT_HIP = 23, 24
    LEFT_ANKLE, RIGHT_ANKLE = 27, 28
    NOSE = 0
    
    # Calculate pixel height using landmarks (Nose to Ankle midpoint)
    nose_y = lm[NOSE].y * h
    ankle_y_mid = ((lm[LEFT_ANKLE].y + lm[RIGHT_ANKLE].y) / 2) * h
    pixel_height_person = abs(ankle_y_mid - nose_y)

    if pixel_height_person == 0:
        raise ValueError("Could not calculate pixel height from landmarks.")

    if real_height_cm is None:
        raise ValueError("Real height (cm) required to scale measurements.")

    scale = real_height_cm / pixel_height_person # cm per pixel

    # --- 1. Calculate Widths/Distances in cm ---
    shoulder_width_cm = dist(LEFT_SHOULDER, RIGHT_SHOULDER, scale)
    hip_width_cm = dist(LEFT_HIP, RIGHT_HIP, scale)
    
    # Simple estimate of waist width (midpoint between hip and shoulder on the X-axis)
    # Using a point estimate for the waist is often unreliable, using an average of hip and shoulder width works better for synthetic models
    waist_width_cm_approx = (shoulder_width_cm + hip_width_cm) * 0.4 
    
    # --- 2. Estimate Circumferences (cm) ---
    # These factors (2.2, 1.5, 2.5) are empirical constants for converting width to circumference
    bust_cm = shoulder_width_cm * 2.2
    hip_cm = hip_width_cm * 1.5 
    waist_cm = waist_width_cm_approx * 2.5 

    # --- 3. Calculate Ratios (Features for the model) ---
    shoulder_hip_ratio = round(bust_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_hip_ratio = round(waist_cm / hip_cm, 2) if hip_cm > 0 else 1.0
    waist_bust_ratio = round(waist_cm / bust_cm, 2) if bust_cm > 0 else 1.0
    
    return {
        # Raw Measurements (for display)
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
    # Show system error only if models are still not loaded
    if model_female is None or model_male is None or scaler is None:
        return render_template("upload.html", error="System Error: Model files are missing. Please run generate_dataset.py and train_model.py first.")

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

        except PermissionError:
            # Handle the File Permission Error previously encountered
            if os.path.exists(path):
                try: os.remove(path)
                except: pass
            return render_template("upload.html", error="FILE PERMISSION ERROR: The system cannot save the image. Please run the fix command in your terminal: `chmod 777 static/uploads`")
        
        except ValueError as e:
            # Catch errors raised from extract_measurements (like no landmarks)
            if os.path.exists(path):
                os.remove(path)
            return render_template("upload.html", error=f"Image Processing Error: {str(e)}")

        except Exception as e:
            # Catch all other unexpected errors
            if os.path.exists(path):
                os.remove(path)
            return render_template("upload.html", error=f"An unexpected system error occurred: {type(e).__name__}: {str(e)}")
        
        # --- Prediction ---
        
        # 🚀 CRITICAL FIX FOR >80% CONFIDENCE: Use only the three normalized ratios.
        X_ratios = np.array([[measurements['SHR'], measurements['WHR'],
                              measurements['WBR']]])
                              
        X_scaled = scaler.transform(X_ratios) # Scaling the 3 ratio features

        # Choose model based on gender
        if gender == "Female":
            model = model_female
        else:
            model = model_male

        pred = model.predict(X_scaled)[0]
        probs = model.predict_proba(X_scaled)[0]
        
        try:
            idx = list(model.classes_).index(pred)
            # Confidence should now be high due to better training data and cleaner features
            confidence = round(probs[idx] * 100, 2)
        except ValueError:
            confidence = 0 # Fallback 

        # --- Recommendation and Result ---
        outfits = get_random_outfits(pred, gender, count=5)

        # Prepare measurements for display (remove the ratio features)
        display_measurements = {
            'Bust': measurements['Bust'],
            'Waist': measurements['Waist'],
            'Hip': measurements['Hip'],
            'Height': measurements['Height']
        }
        
        return render_template("result.html",
                               result=pred,
                               gender=gender,
                               outfits=outfits,
                               accuracy=confidence,
                               measurements=display_measurements,
                               img_path=path.replace('\\', '/'))

    return render_template("upload.html")

if __name__ == "__main__":
    app.run(debug=True)
