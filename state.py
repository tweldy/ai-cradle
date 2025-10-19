# state.py

# Gigi's internal "taste" state
gigi_state = {
    "novelty_hunger": 0.7,            # Craves new patterns or structures
    "structure_craving": 0.6,         # Desires clean, consistent schemas
    "entropy_tolerance": 0.4,         # How much noise/disorder she’s okay with
    "semantic_fatigue": 0.2,          # Low = ready to process deep content
    "trust_baseline": 0.5,            # Neutral: no reason to trust/distrust input
    "data_satiety": 0.1               # Low: she's “hungry” for new input
}

def update_state(new_values):
    """Update Gigi's state based on reactions to input data."""
    for key, val in new_values.items():
        if key in gigi_state:
            gigi_state[key] = min(max(gigi_state[key] + val, 0.0), 1.0)
