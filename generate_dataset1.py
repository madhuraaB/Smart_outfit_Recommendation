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
            shoulder = random.randint(37, 42)

            bust = random.randint(82, 98)
            hip = bust + random.randint(-3, 3)
            waist = bust - random.randint(18, 26)
      
             
        elif shape == 'Apple':
            shoulder = random.randint(40, 46)

            bust = random.randint(90, 104)
            waist = bust - random.randint(2, 8)
            hip = bust - random.randint(8, 16)
        
        if shape == 'Hourglass':
            shoulder = random.randint(37, 42)

            bust = random.randint(82, 98)
            hip = bust + random.randint(-3, 3)
            waist = bust - random.randint(18, 26)


        elif shape == 'Apple':
            shoulder = random.randint(40, 46)

            bust = random.randint(90, 104)
            waist = bust - random.randint(2, 8)
            hip = bust - random.randint(8, 16)


        elif shape == 'Inverted Triangle':
            shoulder = random.randint(43, 49)

            bust = random.randint(92, 106)
            hip = bust - random.randint(10, 18)
            waist = bust - random.randint(18, 26)
        
        data.append([gender, shape, shoulder, bust, waist, hip, height])

# --- Male Data Generation (Simplified, often categorized by shoulder/waist) ---
for shape in male_body_shapes:
     for _ in range(SAMPLES_PER_SHAPE):
        gender = 'Male'
        height = random.randint(165, 195)

        if shape == 'Oval':
            shoulder = random.randint(44, 50)

            bust = random.randint(96, 110)
            waist = bust - random.randint(0, 6)
            hip = bust - random.randint(6, 12)

        elif shape == 'Trapezoid':
            shoulder = random.randint(50, 56)

            bust = random.randint(100, 114)
            waist = bust - random.randint(18, 28)
            hip = bust - random.randint(10, 18)

        elif shape == 'Rectangle':
            shoulder = random.randint(42, 48)

            bust = random.randint(90, 104)
            waist = bust - random.randint(8, 12)
            hip = bust + random.randint(-2, 2)
        data.append([gender, shape, shoulder, bust, waist, hip, height])


df = pd.DataFrame(data, columns=['Gender', 'Shape', 'Shoulder', 'Bust', 'Waist', 'Hip', 'Height'])
df.to_csv('body_measurements.csv', index=False)
print(f"✅ Generated {len(df)} samples ({SAMPLES_PER_SHAPE} per shape) and saved to body_measurements.csv.")
