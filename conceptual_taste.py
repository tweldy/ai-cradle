from taste_engine import evaluate_dataset, associate_concepts
from state import gigi_state, update_state

sample_dataset = {
    "name": "Abstract_Expressions.json",
    "structure_score": 0.3,
    "novelty": 0.9,
    "noise_level": 0.5,
    "semantic_flavor": "literary",
    "emotional_tone": "melancholy"
}

# Gigi reacts and reflects
reaction = evaluate_dataset(sample_dataset)
association = associate_concepts(sample_dataset)

# Optionally update state
update_state({
    "novelty_hunger": -0.2,
    "semantic_fatigue": 0.1,
    "data_satiety": 0.3
})

# Output
print("🧠 Gigi's Reaction:\n", reaction)
print("🧠 Gigi's Association:\n", association)
