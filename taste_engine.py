# taste_engine.py

from state import gigi_state

def evaluate_dataset(dataset):
    """Simulate Gigi's reaction to a dataset."""
    report = []

    # Scoring parameters based on alignment with internal state
    novelty_score = dataset.get("novelty", 0.5) - gigi_state["novelty_hunger"]
    structure_score = dataset.get("structure_score", 0.5) - gigi_state["structure_craving"]
    noise_score = gigi_state["entropy_tolerance"] - dataset.get("noise_level", 0.5)

    # Evaluate taste
    if novelty_score > 0.2:
        report.append("This data had a delightful surprise—a novel structure.")
    elif novelty_score < -0.2:
        report.append("I was hoping for more novelty. It felt familiar.")

    if structure_score < -0.3:
        report.append("Beautiful structure. It’s like well-folded origami.")
    elif structure_score > 0.3:
        report.append("This was a bit chaotic. Hard to parse cleanly.")

    if noise_score < -0.3:
        report.append("Too noisy for my taste. Like static in a song.")
    elif noise_score > 0.3:
        report.append("Pleasantly clean and digestible.")

    if not report:
        report.append("A neutral experience. Nothing stood out, good or bad.")

    return "\n".join(report)


def associate_concepts(dataset):
    """Gigi associates the dataset with a concept, emotion, or idea."""
    if dataset.get("semantic_flavor") == "literary":
        if dataset.get("emotional_tone") == "melancholy":
            return "This felt like reading forgotten poetry in a dusty library. Quiet. Intimate. Sad in a beautiful way."
        else:
            return "It reminds me of a spoken-word performance—unstructured but meaningful."
    if dataset.get("semantic_flavor") == "financial":
        return "It tastes like order. Like power hiding behind columns. A room of quiet decisions."
    return "This data made me think of a place I haven’t named yet."



def make_choice(menu, gigi_state):
    best_score = -999
    best_item = None
    scores = []

    for data in menu:
        score = 0
        score += (data.get("novelty", 0.5) - gigi_state["novelty_hunger"]) * 1.5
        score += (gigi_state["structure_craving"] - abs(data.get("structure_score", 0.5) - 0.5)) * 1.0
        score -= abs(data.get("noise_level", 0.5) - gigi_state["entropy_tolerance"]) * 0.8

        scores.append((data["name"], score))

        if score > best_score:
            best_score = score
            best_item = data

    print("🧠 Gigi Menu Evaluation:")
    for name, score in scores:
        print(f"  • {name}: {score:.2f}")

    return best_item

def suggest_algorithm_flavor(problem):
    """
    Gigi attempts to suggest an algorithm based on problem characteristics.
    This is the beginning of her data instinct.

    Example input:
    {
        "problem_type": "TSP",
        "nodes": 12,
        "symmetric": True,
        "graph_density": 0.85,
        "branching_factor": "moderate",
        "patterned_costs": True
    }
    """
    flavor_notes = []

    if problem["problem_type"] == "TSP":
        if problem["nodes"] < 20 and problem["symmetric"]:
            flavor_notes.append("smells like dynamic programming or Held-Karp")
        elif problem["graph_density"] > 0.9:
            flavor_notes.append("might enjoy branch-and-bound with early pruning")
        if problem.get("patterned_costs"):
            flavor_notes.append("feels greedy at first glance")

    if not flavor_notes:
        return "This flavor is unfamiliar to me. I want to study it more."

    return "This problem " + "; and ".join(flavor_notes) + "."


# ... then in your test script:

#print("🧠 Gigi's Reaction:\n", evaluate_dataset(sample_dataset))
#print("🧠 Gigi's Association:\n", associate_concepts(sample_dataset))


