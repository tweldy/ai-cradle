from taste_engine import suggest_algorithm_flavor
import json

with open("gigi/instinct/tsp_small_graph.json") as f:
    problem = json.load(f)

print("🧠 Gigi’s Instinctual Response:")
print(suggest_algorithm_flavor(problem))
