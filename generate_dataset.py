# generate_dataset.py
import pandas as pd
import random

body_shapes = ['Hourglass', 'Pear', 'Apple', 'Rectangle', 'Inverted Triangle']
# Adding male shapes for robustness, although only 3 are typically used for men (Oval, Trapezoid, Rectangle)
male_body_shapes = ['Oval', 'Trapezoid', 'Rectangle']

data = []

# 🚀 CRITICAL FIX: Generate 500 samples per shape for robust training
SAMPLES_PER_SHAPE = 500

# --- Female Data Generation ---
for shape in body_shapes:
    for _ in range(SAMPLES_PER_SHAPE):
        gender = 'Female'
        height = random.randint(150, 185) # Base height
        
        # Ranges based on common body shape definitions (cm)
        if shape == 'Hourglass':
            # Bust ~ Hip, Waist significantly smaller
            shoulder = random.randint(38, 44)
            bust = random.randint(90, 105)
            hip = random.randint(90, 105)
            waist = random.randint(60, 75)
        elif shape == 'Pear':
            # Hip > Bust/Shoulder
            shoulder = random.randint(36, 42)
            bust = random.randint(80, 95)
            waist = random.randint(65, 75)
            hip = random.randint(95, 110)
        elif shape == 'Apple':
            # Waist/Bust is largest circumference
            shoulder = random.randint(40, 48)
            bust = random.randint(95, 115)
            waist = random.randint(75, 90)
            hip = random.randint(90, 105)
        elif shape == 'Rectangle':
            # Bust ~ Waist ~ Hip
            shoulder = random.randint(36, 42)
            bust = random.randint(85, 95)
            waist = random.randint(70, 80)
            hip = random.randint(85, 95)
        elif shape == 'Inverted Triangle':
            # Shoulder/Bust > Hip
            shoulder = random.randint(42, 50)
            bust = random.randint(95, 110)
            waist = random.randint(70, 80)
            hip = random.randint(85, 95)
        
        data.append([gender, shape, shoulder, bust, waist, hip, height])

# --- Male Data Generation (Simplified, often categorized by shoulder/waist) ---
for shape in male_body_shapes:
     for _ in range(SAMPLES_PER_SHAPE):
        gender = 'Male'
        height = random.randint(165, 195)

        if shape == 'Oval': # Apple equivalent: central weight
            shoulder = random.randint(45, 55)
            bust = random.randint(100, 120)
            waist = random.randint(90, 105)
            hip = random.randint(95, 115)
        elif shape == 'Trapezoid': # Hourglass/Inverted Triangle equivalent: Broad shoulders, narrow waist/hip
            shoulder = random.randint(48, 58)
            bust = random.randint(105, 125)
            waist = random.randint(80, 95)
            hip = random.randint(90, 105)
        elif shape == 'Rectangle': # Similar to female Rectangle
            shoulder = random.randint(40, 50)
            bust = random.randint(90, 110)
            waist = random.randint(80, 90)
            hip = random.randint(85, 95)

        data.append([gender, shape, shoulder, bust, waist, hip, height])


df = pd.DataFrame(data, columns=['Gender', 'Shape', 'Shoulder', 'Bust', 'Waist', 'Hip', 'Height'])
df.to_csv('body_measurements.csv', index=False)
print(f"✅ Generated {len(df)} samples ({SAMPLES_PER_SHAPE} per shape) and saved to body_measurements.csv.")
