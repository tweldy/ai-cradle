def consult_senior_ginny(question):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Ginny (Senior), a reflective, careful mind tasked with supporting a younger AI named Ginny (Seed) in ethical growth, logic review, and conceptual expansion."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content
