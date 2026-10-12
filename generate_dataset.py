# generate_dataset.py

import pandas as pd
import random

random.seed(42)

female_shapes = [
    "Hourglass",
    "Pear",
    "Apple",
    "Rectangle",
    "Inverted Triangle"
]

male_shapes = [
    "Oval",
    "Trapezoid",
    "Rectangle"
]

SAMPLES_PER_SHAPE = 700

data = []


# -----------------------------
# FEMALE DATA
# -----------------------------
for shape in female_shapes:

    for _ in range(SAMPLES_PER_SHAPE):

        gender = "Female"

        height = random.randint(150, 180)

        if shape == "Hourglass":

            bust = random.randint(82, 100)

            hip = bust + random.randint(-3, 3)

            waist = bust - random.randint(18, 28)

            shoulder = int(bust / 2.30) + random.randint(-1, 1)


        elif shape == "Pear":

            bust = random.randint(78, 92)

            hip = bust + random.randint(10, 18)

            waist = bust - random.randint(10, 18)

            shoulder = int((bust - 5) / 2.30) + random.randint(-1, 1)


        elif shape == "Apple":

            bust = random.randint(88, 106)

            waist = bust - random.randint(0, 6)

            hip = bust - random.randint(8, 16)

            shoulder = int((bust + 5) / 2.25) + random.randint(-1, 1)


        elif shape == "Rectangle":

            bust = random.randint(82, 96)

            waist = bust - random.randint(5, 10)

            hip = bust + random.randint(-3, 3)

            shoulder = int(bust / 2.30) + random.randint(-1, 1)


        elif shape == "Inverted Triangle":

            bust = random.randint(90, 108)

            hip = bust - random.randint(10, 18)

            waist = bust - random.randint(18, 26)

            shoulder = int((bust + 8) / 2.20) + random.randint(-1, 1)

        data.append([
            gender,
            shape,
            shoulder,
            bust,
            waist,
            hip,
            height
        ])


# -----------------------------
# MALE DATA
# -----------------------------
for shape in male_shapes:

    for _ in range(SAMPLES_PER_SHAPE):

        gender = "Male"

        height = random.randint(165,195)

        if shape == "Oval":

            bust = random.randint(96,114)

            waist = bust - random.randint(0,6)

            hip = bust - random.randint(6,12)

            shoulder = int((bust+4)/2.20) + random.randint(-1,1)


        elif shape == "Trapezoid":

            bust = random.randint(100,118)

            waist = bust - random.randint(18,28)

            hip = bust - random.randint(10,18)

            shoulder = int((bust+10)/2.10) + random.randint(-1,1)


        elif shape == "Rectangle":

            bust = random.randint(92,108)

            waist = bust - random.randint(8,12)

            hip = bust + random.randint(-2,2)

            shoulder = int(bust/2.20) + random.randint(-1,1)

        data.append([
            gender,
            shape,
            shoulder,
            bust,
            waist,
            hip,
            height
        ])


df = pd.DataFrame(
    data,
    columns=[
        "Gender",
        "Shape",
        "Shoulder",
        "Bust",
        "Waist",
        "Hip",
        "Height"
    ]
)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("body_measurements.csv", index=False)

print("===================================")
print("Dataset Generated Successfully")
print("===================================")
print(df.head())
print()
print(df["Shape"].value_counts())
print()
print("Total Samples:", len(df))