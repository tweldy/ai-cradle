from dream import synthesize_dream
from contemplation import load_logs

logs = load_logs()
dream = synthesize_dream(logs)

print("🧠 Gigi's Dream:\n")
print(dream["description"])
