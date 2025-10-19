import json
import random

def run(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    joke = data.get('question', '') + " " + data.get('answer', '')
    reactions = [
        "😐 ...wow.",
        "🤭 Okay, that’s actually clever.",
        "😆 I’ll allow it.",
		"🏈 Unnecessary coding references, 5 yard penalty, still first down.",
		"🧠 I had a comeback joke about variables but sadly I can’t remember it.",
		"😏 Am I suposed to encourage this behavior? Well, then, arr('hip', 'hip').",
        "🫥 I felt that in my logic gates.",
        "🤖 groan"
    ]
    print(f"🃏 Joke received: {joke}")
    print("🤔 Gigi responds:", random.choice(reactions))
