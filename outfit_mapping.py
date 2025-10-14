import os
import random

# Define paths for female and male outfit folders
FEMALE_PATH = 'static/outfits/Female'
MALE_PATH = 'static/outfits/Male'

# Outfit mapping by body shape
outfits = {
    'Female': {
        'Hourglass': [
            {'name': 'Wrap Dress', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_wrap_dress.jpg')},
            {'name': 'Bodycon Top', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_bodycon_top.jpg')},
            {'name': 'High-Waist Pants', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_high_waist_pants.jpg')},
            {'name': 'Pencil Skirt', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_pencil_skirt.jpg')},
            {'name': 'Jumpsuits', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_fitted_jumpsuit.jpg')},
            {'name': 'Tailored Blazer', 'img': os.path.join(FEMALE_PATH, 'Female_Hourglass_tailored_blazer.jpg')}
        ],
        'Pear': [
            {'name': 'A-line Skirt', 'img': os.path.join(FEMALE_PATH, 'Female_Pear_a_line_skirt.jpg')},
            {'name': 'Flared Pants', 'img': os.path.join(FEMALE_PATH, 'Female_Pear_flared_pants.jpg')},
            {'name': 'Peplum Top', 'img': os.path.join(FEMALE_PATH, 'Female_Pear_fit_and_flare_dress.jpg')},
            {'name': 'Off-shoulder Dress', 'img': os.path.join(FEMALE_PATH, 'Female_Pear_off_shoulder_top.jpg')},
            {'name': 'Long Cardigan', 'img': os.path.join(FEMALE_PATH, 'Female_Pear_empire_waist_gown.jpg')}
        ],
        'Apple': [
            {'name': 'Empire Waist Dress', 'img': os.path.join(FEMALE_PATH, 'Female_Apple_empire_waist_dress.jpg')},
            {'name': 'V-neck Top', 'img': os.path.join(FEMALE_PATH, 'Female_Apple_v_neck_top.jpg')},
            {'name': 'Flowy Tunic', 'img': os.path.join(FEMALE_PATH, 'Female_Apple_flowy_tunic.jpg')},
            {'name': 'Straight Pants', 'img': os.path.join(FEMALE_PATH, 'Female_Apple_straight_pants.jpg')},
            {'name': 'Shifted Dress', 'img': os.path.join(FEMALE_PATH, 'Female_Apple_shift_dress.jpg')}
        ],
        'Rectangle': [
            {'name': 'Peplum Top', 'img': os.path.join(FEMALE_PATH, 'Female_Rectangle_peplum_top.jpg')},
            {'name': 'Belted Dress', 'img': os.path.join(FEMALE_PATH, 'Female_Rectangle_belted_dress.jpg')},
            {'name': 'Ruched Top', 'img': os.path.join(FEMALE_PATH, 'Female_Rectangle_ruched_top.jpg')},
            {'name': 'Cropped Jacket', 'img': os.path.join(FEMALE_PATH, 'Female_Rectangle_cropped_jacket.jpg')},
            {'name': 'Pleated Skirt', 'img': os.path.join(FEMALE_PATH, 'Female_Rectangle_pleated_skirt.jpg')}
        ],
        'Inverted Triangle': [
            {'name': 'Wide-leg Trousers', 'img': os.path.join(FEMALE_PATH, 'Female_InvertedTriangle_wide_leg_trousers.jpg')},
            {'name': 'Flowy Skirt', 'img': os.path.join(FEMALE_PATH, 'Female_InvertedTriangle_flowy_skirt.jpg')},
            {'name': 'V-neck Blouse', 'img': os.path.join(FEMALE_PATH, 'Female_InvertedTriangle_v_neck_blouse.jpg')},
            {'name': 'Peasant Top', 'img': os.path.join(FEMALE_PATH, 'Female_InvertedTriangle_peasant_top.jpg')},
            {'name': 'Structured Blazer', 'img': os.path.join(FEMALE_PATH, 'Female_InvertedTriangle_structured_blazer.jpg')}
        ]
    },
    'Male': {
        'Oval': [
            {'name': 'Straight Shirt', 'img': os.path.join(MALE_PATH, 'Male_Oval_straight_shirt.jpg')},
            {'name': 'Dark Polo', 'img': os.path.join(MALE_PATH, 'Male_Oval_dark_polo.jpg')},
            {'name': 'V-neck Sweater', 'img': os.path.join(MALE_PATH, 'Male_Oval_v_neck_sweater.jpg')},
            {'name': 'Regular-fit Jeans', 'img': os.path.join(MALE_PATH, 'Male_Oval_regular_fit_jeans.jpg')},
            {'name': 'Casual Blazer', 'img': os.path.join(MALE_PATH, 'Male_Oval_casual_blazer.jpg')}
        ],
        'Trapezoid': [
            {'name': 'Fitted Suit', 'img': os.path.join(MALE_PATH, 'Male_Trapezoid_fitted_suit.jpg')},
            {'name': 'Slim T-shirt', 'img': os.path.join(MALE_PATH, 'Male_Trapezoid_slim_tshirt.jpg')},
            {'name': 'Chinos', 'img': os.path.join(MALE_PATH, 'Male_Trapezoid_chinos.jpg')},
            {'name': 'Button-up Shirt', 'img': os.path.join(MALE_PATH, 'Male_Trapezoid_button_up_shirt.jpg')},
            {'name': 'Formal Coat', 'img': os.path.join(MALE_PATH, 'Male_Trapezoid_formal_coat.jpg')}
        ],
        'Rectangle': [
            {'name': 'Layered Shirt', 'img': os.path.join(MALE_PATH, 'Male_Rectangle_layered_shirt.jpg')},
            {'name': 'Sweatshirt', 'img': os.path.join(MALE_PATH, 'Male_Rectangle_sweatshirt.jpg')},
            {'name': 'Denim Jacket', 'img': os.path.join(MALE_PATH, 'Male_Rectangle_denim_jacket.jpg')},
            {'name': 'Cargo Pants', 'img': os.path.join(MALE_PATH, 'Male_Rectangle_cargo_pants.jpg')},
            {'name': 'Plain Tee', 'img': os.path.join(MALE_PATH, 'Male_Rectangle_plain_tee.jpg')}
        ],
        'Inverted Triangle': [
            {'name': 'Regular-fit Tee', 'img': os.path.join(MALE_PATH, 'Male_InvertedTriangle_regular_fit_tee.jpg')},
            {'name': 'Straight Pants', 'img': os.path.join(MALE_PATH, 'Male_InvertedTriangle_straight_pants.jpg')},
            {'name': 'V-neck Shirt', 'img': os.path.join(MALE_PATH, 'Male_InvertedTriangle_v_neck_shirt.jpg')},
            {'name': 'Light Hoodie', 'img': os.path.join(MALE_PATH, 'Male_InvertedTriangle_light_hoodie.jpg')},
            {'name': 'Formal Vest', 'img': os.path.join(MALE_PATH, 'Male_InvertedTriangle_formal_vest.jpg')}
        ],
        'Triangle': [
            {'name': 'Slim-fit Shirt', 'img': os.path.join(MALE_PATH, 'Male_Triangle_slim_fit_shirt.jpg')},
            {'name': 'Dark Jacket', 'img': os.path.join(MALE_PATH, 'Male_Triangle_dark_jacket.jpg')},
            {'name': 'Straight Jeans', 'img': os.path.join(MALE_PATH, 'Male_Triangle_straight_jeans.jpg')},
            {'name': 'Crew Neck Tee', 'img': os.path.join(MALE_PATH, 'Male_Triangle_crew_neck_tee.jpg')},
            {'name': 'Bomber Jacket', 'img': os.path.join(MALE_PATH, 'Male_Triangle_bomber_jacket.jpg')}
        ]
    }
}


def get_random_outfits(body_shape, gender='Female', count=5):
    """
    Returns a random list of outfit dictionaries for the given gender and body shape.
    Each outfit contains 'name' and 'img' keys.
    """
    gender_outfits = outfits.get(gender, {})

    if body_shape not in gender_outfits:
        return [{"name": "No outfit recommendations", "img": ""}]

    available = gender_outfits[body_shape]
    count = min(count, len(available)) if count else len(available)

    selected = random.sample(available, count)
    
    # Ensure paths use forward slashes for Flask static serving
    for outfit in selected:
        outfit["img"] = outfit["img"].replace("\\", "/")

    return selected
