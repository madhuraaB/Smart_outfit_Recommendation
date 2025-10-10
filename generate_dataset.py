# generate_dataset.py
import pandas as pd
import random
import numpy as np

# Increased samples and strict ratio-based generation
female_shapes = ['Hourglass', 'Pear', 'Apple', 'Rectangle', 'Inverted Triangle']
male_shapes = ['Triangle', 'Inverted Triangle', 'Oval', 'Rectangle', 'Trapezoid']
data = []
NUM_SAMPLES_PER_SHAPE = 300 

# --- Female Data Generation ---
for shape in female_shapes:
    for _ in range(NUM_SAMPLES_PER_SHAPE):
        height = random.uniform(155, 180)
        
        # Enforcing strict ratios for clear class boundaries
        if shape == 'Hourglass':
            bust = random.uniform(95, 110)
            hip = random.uniform(bust * 0.95, bust * 1.05)
            waist = random.uniform(bust * 0.65, bust * 0.75)
            shoulder = random.uniform(bust * 0.85, bust * 0.95)
        
        elif shape == 'Pear':
            hip = random.uniform(100, 120)
            bust = random.uniform(hip * 0.8, hip * 0.9)
            waist = random.uniform(hip * 0.7, hip * 0.85)
            shoulder = random.uniform(bust * 0.9, bust * 1.0)

        elif shape == 'Apple':
            bust = random.uniform(105, 125)
            waist = random.uniform(bust * 0.85, bust * 0.95)
            hip = random.uniform(bust * 0.9, bust * 1.05)
            shoulder = random.uniform(bust * 0.9, bust * 1.0)
            
        elif shape == 'Rectangle':
            bust = random.uniform(90, 105)
            waist = random.uniform(bust * 0.8, bust * 0.95)
            hip = random.uniform(bust * 0.9, bust * 1.05)
            shoulder = random.uniform(bust * 0.95, bust * 1.05)

        elif shape == 'Inverted Triangle':
            bust = random.uniform(100, 120)
            hip = random.uniform(bust * 0.8, bust * 0.9)
            waist = random.uniform(bust * 0.7, bust * 0.8)
            shoulder = random.uniform(bust * 1.0, bust * 1.1)

        data.append([shoulder, bust, waist, hip, height, shape, 'Female'])

# --- Male Data Generation ---
for shape in male_shapes:
    for _ in range(NUM_SAMPLES_PER_SHAPE):
        height = random.uniform(170, 195)
        
        if shape == 'Trapezoid': 
            bust = random.uniform(100, 120)
            hip = random.uniform(bust * 0.9, bust * 1.0)
            waist = random.uniform(hip * 0.85, hip * 0.95)
            shoulder = random.uniform(bust * 1.0, bust * 1.1)
            
        elif shape == 'Inverted Triangle':
            bust = random.uniform(110, 130)
            waist = random.uniform(bust * 0.7, bust * 0.85)
            hip = random.uniform(waist * 0.95, waist * 1.05)
            shoulder = random.uniform(bust * 1.1, bust * 1.2)
            
        elif shape == 'Triangle':
            hip = random.uniform(105, 125)
            bust = random.uniform(hip * 0.8, hip * 0.9)
            waist = random.uniform(hip * 0.9, hip * 1.0)
            shoulder = random.uniform(bust * 0.9, bust * 1.0)
            
        elif shape == 'Oval':
            bust = random.uniform(115, 135)
            waist = random.uniform(bust * 0.9, bust * 1.0)
            hip = random.uniform(bust * 0.9, bust * 1.0)
            shoulder = random.uniform(bust * 0.9, bust * 1.0)
            
        elif shape == 'Rectangle':
            bust = random.uniform(95, 115)
            waist = random.uniform(bust * 0.85, bust * 0.95)
            hip = random.uniform(bust * 0.9, bust * 1.0)
            shoulder = random.uniform(bust * 0.95, bust * 1.05)

        data.append([shoulder, bust, waist, hip, height, shape, 'Male'])

df = pd.DataFrame(data, columns=['Shoulder','Bust','Waist','Hip','Height','BodyShape', 'Gender'])
df.to_csv('body_shapes_dataset_gendered.csv', index=False)
print("✅ Gendered Dataset generated: body_shapes_dataset_gendered.csv (Total: {} samples)".format(len(df)))