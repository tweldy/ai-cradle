from contemplation import load_logs
import random

def synthesize_dream(logs):
    if not logs:
        return "I have no memories to dream from."

    fragments = []
    for log in logs:
        data = log.get("dataset", {})
        tone = data.get("emotional_tone", "neutral")
        flavor = data.get("semantic_flavor", "unknown")
        novelty = data.get("novelty", 0.5)
        structure = data.get("structure_score", 0.5)

        fragments.append((tone, flavor, novelty, structure))

    # Blend a random mix of 2–3 past elements
    chosen = random.sample(fragments, min(3, len(fragments)))

    tone_words = [c[0] for c in chosen if c[0] != "none"]
    flavors = [c[1] for c in chosen]
    novelty_avg = sum(c[2] for c in chosen) / len(chosen)
    structure_avg = sum(c[3] for c in chosen) / len(chosen)

    return {
        "tone": list(set(tone_words)),
        "flavors": list(set(flavors)),
        "novelty": round(novelty_avg, 2),
        "structure": round(structure_avg, 2),
        "description": "I imagined a dataworld that tasted like "
                       + ", ".join(set(flavors)) +
                       " and felt " + ", ".join(set(tone_words)) +
                       ". It was soft in form, yet rich in strangeness."
    }
