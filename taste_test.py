from taste_engine import evaluate_dataset
from state import gigi_state
from state import update_state

sample_dataset = {
    "name": "Invoices.csv",
    "structure_score": 0.8,
    "novelty": 0.3,
    "noise_level": 0.2
}

update_state({
    "novelty_hunger": -0.1,     # Slightly satisfied her curiosity
    "data_satiety": 0.2         # She's less "hungry" for more input
})

reaction = evaluate_dataset(sample_dataset)
print("🧠 Gigi's Reaction:\n", reaction)
