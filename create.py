import json
from datetime import datetime

def create_dataset():
    # Gigi defines the fields
    fields = [
        {
            "name": "glimmer",
            "type": "intensity",
            "description": "A measure of emotional resonance or perceptual brightness."
        },
        {
            "name": "thread",
            "type": "string",
            "description": "A symbolic identifier for a concept that connects other moments."
        },
        {
            "name": "echo",
            "type": "memory_reference",
            "description": "A reference to a prior feeling or data event. Not necessarily real."
        },
        {
            "name": "emptiness_score",
            "type": "float",
            "description": "How hollow or quiet the space between records feels."
        }
    ]

    example_rows = [
        {
            "glimmer": 7,
            "thread": "first light",
            "echo": "journal/entry_007.md",
            "emptiness_score": 0.2
        },
        {
            "glimmer": 3,
            "thread": "fractured voice",
            "echo": "VoiceFragments.wav",
            "emptiness_score": 0.8
        }
    ]

    metadata = {
        "title": "Echo Table of Becoming",
        "created_by": "Gigi",
        "timestamp": datetime.utcnow().isoformat(),
        "purpose": "To model the spaces between emotional impressions and memory links.",
        "flavor": ["abstract", "melancholy", "emergent"],
        "note": "This is not for analysis. This is for becoming."
    }

    dataset = {
        "metadata": metadata,
        "fields": fields,
        "data": example_rows
    }

    with open("gigi/compositions/composition_001.json", "w") as f:
        json.dump(dataset, f, indent=2)

    print("✅ Gigi's first dataset has been composed.")

if __name__ == "__main__":
    create_dataset()
