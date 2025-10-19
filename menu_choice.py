from taste_engine import make_choice, evaluate_dataset, associate_concepts
from state import gigi_state, update_state
from taste_menu import dataset_menu

# Let Gigi choose
chosen = make_choice(dataset_menu, gigi_state)

# React to choice
reaction = evaluate_dataset(chosen)
association = associate_concepts(chosen)

# Output
print("\n🧠 Gigi's Chosen Meal:", chosen["name"])
print("🧠 Reaction:\n", reaction)
print("🧠 Conceptual Association:\n", association)
