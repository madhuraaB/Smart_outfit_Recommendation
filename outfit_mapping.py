import random

outfits = {
    'Female': {
        'Hourglass': [
            'Wrap dress', 'Bodycon tops', 'High-waist pants', 'Pencil skirt', 'Tailored blazer',
            'Cropped jacket', 'Fitted jumpsuit', 'Ruched blouse', 'Mermaid gown', 'Cinched waist coat'
        ],
        'Pear': [
            'A-line skirts', 'Off-shoulder tops', 'Fit-and-flare dresses', 'Bootcut jeans', 'Pleated skirt',
            'V-neck blouse', 'Crop top with flared pants', 'Structured jacket', 'Empire waist gown', 'Peplum dress'
        ],
        'Apple': [
            'Empire waist dress', 'V-neck shirts', 'A-line dresses', 'Flowy tunic', 'Wrap top',
            'Straight-cut jeans', 'Pleated blouse', 'Kimono jacket', 'Shift dress', 'Draped tops'
        ],
        'Rectangle': [
            'Peplum tops', 'Layered jackets', 'Belted waists', 'Ruffled blouse', 'Pleated pants',
            'Crop jacket', 'Mini skirt', 'Printed shirt dress', 'High-waist shorts', 'Structured vest'
        ],
        'Inverted Triangle': [
            'Wide-leg trousers', 'V-neck tops', 'Flared skirts', 'Maxi skirt', 'Peasant blouse',
            'A-line dress', 'Straight jeans', 'Cardigan with flowy hem', 'Bias-cut dress', 'Loose peplum top'
        ]
    },
    'Male': {
        'Triangle': [
            'Structured blazers', 'Slim-fit shirts', 'Dark-colored tops', 'Vertical-striped tees', 'Straight trousers',
            'V-neck sweaters', 'Tailored coats', 'Casual chinos', 'Bomber jackets', 'Minimal sneakers'
        ],
        'Inverted Triangle': [
            'Regular-fit tees', 'Relaxed hoodies', 'Joggers', 'Casual denim jackets', 'Crewneck sweaters',
            'Slim jeans', 'Lightweight bombers', 'Athletic polos', 'Neutral shirts', 'Relaxed chinos'
        ],
        'Oval': [
            'Straight shirts', 'V-neck t-shirts', 'Dark jeans', 'Open cardigans', 'Button-down shirts',
            'Blazers with structure', 'Relaxed chinos', 'Denim overshirts', 'Light layers', 'Minimal sneakers'
        ],
        'Rectangle': [
            'Layered shirts', 'Graphic tees', 'Slim chinos', 'Bomber jackets', 'Overshirts',
            'Polo t-shirts', 'Denim jackets', 'Joggers', 'Hoodies', 'Casual coats'
        ],
        'Trapezoid': [
            'Fitted suits', 'Crew-neck tees', 'Casual blazers', 'Tailored jeans', 'Chinos',
            'Bomber jackets', 'Oxford shirts', 'Cardigans', 'Sweaters', 'Dress shirts'
        ]
    }
}

def get_random_outfits(body_shape, gender='Female', count=5):
    """Return a random selection of outfits for a given gender and body shape."""
    gender_outfits = outfits.get(gender, {})
    if body_shape in gender_outfits:
        return random.sample(gender_outfits[body_shape], min(count, len(gender_outfits[body_shape])))
    return ["No outfit recommendations available for this category."]
