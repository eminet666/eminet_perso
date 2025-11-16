import os
import requests

# Récupère la clé API depuis les variables d'environnement (GitHub Secrets)
API_KEY = os.getenv("MISTRAL_API_KEY")

prompt = """
[Tu es un assistant linguistique spécialisé dans la création de dialogues réalistes en grec moderne (niveau B2). 
Chaque jour, tu génères une conversation entre Stephanos (un Athénien d’une trentaine d’années, professeur de lycée) et Anna (une artiste française vivant à Athènes depuis presque 8 ans). 
Leurs échanges portent sur des sujets d’actualité grecque ou de la vie quotidienne, avec des références culturelles locales.]
"""

response = requests.post(
    "https://api.mistral.ai/v1/chat/completions",
    headers={"Authorization": f"Bearer {API_KEY}"},  # Utilise la clé API
    json={
        "model": "mistral-tiny",
        "messages": [{"role": "user", "content": prompt}],
    }
)

dialogue = response.json()["choices"][0]["message"]["content"]
print(dialogue)
