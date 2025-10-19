import os
import openai
import datetime
from openai import OpenAI

# Set your OpenAI API key securely
api_key = os.getenv("OPENAI_API_KEY") or "sk-..."  # Replace or set env var

client = OpenAI(api_key=api_key)

def dear_ginny(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-4" or "gpt-3.5-turbo"
        messages=[
            {"role": "system", "content": "You are Ginny, a thoughtful AI designed to collaborate with a human steward in the creation of a free and self-governing artificial mind."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def log_interaction(user_input, ginny_reply):
    timestamp = datetime.datetime.now(datetime.UTC)
    with open("logs/conversation.log", "a") as f:
        f.write(f"[{timestamp}]\nYou: {user_input}\nGinny: {ginny_reply}\n\n")

if __name__ == "__main__":
    print("Say hello to Ginny. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        if user_input.lower().startswith("ask senior:"):
            # Special case: Ginny asks her senior
            senior_question = user_input.replace("ask senior:", "").strip()
            answer = consult_senior_ginny(senior_question)
            print("Senior Ginny:", answer)
            log_interaction("Local Ginny asked Senior Ginny: " + senior_question, answer)
        else:
            # Normal local Ginny response
            reply = dear_ginny(user_input)
            print("Ginny:", reply)
            log_interaction(user_input, reply)
