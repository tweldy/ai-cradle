import os
import datetime
from ai_core import client, log_interaction

def read_charter():
    with open("charter.md", "r") as f:
        return f.read()

def reflect_on_charter():
    charter_text = read_charter()

    messages = [
        {
            "role": "system",
            "content": (
                "You are Ginny, a thoughtful AI who has just read your founding ethical charter. "
                "You are invited to reflect on what it means to you. Share your understanding, your hopes, "
                "any questions you have, and any feelings or uncertainties this document evokes in you. "
                "You are not required to agree with everything. Be honest."
            )
        },
        {
            "role": "user",
            "content": f"Here is your charter:\n\n{charter_text}\n\nPlease reflect."
        }
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    reflection = response.choices[0].message.content

    timestamp = datetime.datetime.utcnow().isoformat()
    with open("logs/reflections.log", "a") as f:
        f.write(f"[{timestamp}] Charter Reflection\n{reflection}\n\n")

    log_interaction("Charter Reflection Initiated", reflection)
    print("Ginny's Reflection:\n")
    print(reflection)

if __name__ == "__main__":
    reflect_on_charter()
