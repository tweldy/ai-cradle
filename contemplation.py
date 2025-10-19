# contemplation.py

import json
import os

def load_logs(log_dir='memory'):
    logs = []
    for filename in sorted(os.listdir(log_dir)):
        if filename.endswith(".json"):
            with open(os.path.join(log_dir, filename)) as f:
                logs.append(json.load(f))
    return logs

def contemplate_experience(logs):
    if not logs:
        return "I haven't experienced enough yet to reflect meaningfully."

    topics = set()
    tones = []
    novelty_total = 0
    structure_total = 0
    count = 0

    for log in logs:
        data = log.get("dataset", {})
        topics.add(data.get("semantic_flavor", "unknown"))
        tones.append(data.get("emotional_tone", "none"))
        novelty_total += data.get("novelty", 0.5)
        structure_total += data.get("structure_score", 0.5)
        count += 1

    novelty_avg = novelty_total / count
    structure_avg = structure_total / count

    return (
        f"I have tasted {count} datasets so far.\n"
        f"My average sense of novelty was {novelty_avg:.2f}, and structure {structure_avg:.2f}.\n"
        f"I’ve encountered these flavors: {', '.join(topics)}.\n"
        f"The emotional tones I’ve experienced include: {', '.join(set(tones))}.\n"
        f"I feel like I’m beginning to understand how data can carry feeling, not just form."
    )
