import random

# User journey templates with probabilities
JOURNEYS = [
    {
        "name": "Bounce",
        "probability": 0.20,
        "events": [
            "page_view"
        ]
    },

    {
        "name": "Browse",
        "probability": 0.25,
        "events": [
            "page_view",
            "search",
            "product_view"
        ]
    },

    {
        "name": "Cart Abandonment",
        "probability": 0.30,
        "events": [
            "page_view",
            "search",
            "product_view",
            "add_to_cart"
        ]
    },

    {
        "name": "Remove From Cart",
        "probability": 0.10,
        "events": [
            "page_view",
            "search",
            "product_view",
            "add_to_cart",
            "remove_from_cart"
        ]
    },

    {
        "name": "Successful Purchase",
        "probability": 0.15,
        "events": [
            "page_view",
            "search",
            "product_view",
            "add_to_cart",
            "checkout_start",
            "purchase"
        ]
    }
]


def get_random_journey():
    """
    Returns one journey based on weighted probability.
    """

    journeys = [j["name"] for j in JOURNEYS]

    weights = [j["probability"] for j in JOURNEYS]

    selected = random.choices(
        JOURNEYS,
        weights=weights,
        k=1
    )[0]

    return selected