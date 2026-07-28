def build_general_prompt(question):

    return f"""
You are MedRAG AI.

No relevant indexed research exists.

Answer using established medical knowledge.

Be concise.

Question:

{question}

Answer:

Source:
General Medical Knowledge
"""