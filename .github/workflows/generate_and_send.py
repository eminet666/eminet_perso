import os
import sys
import requests
from time import sleep

API_KEY = os.getenv("MISTRAL_API_KEY")
if not API_KEY:
    print("ERROR: MISTRAL_API_KEY not set in environment.", file=sys.stderr)
    sys.exit(1)

prompt = """[Tu es un assistant linguistique spécialisé dans la création de dialogues réalistes en grec moderne (niveau B2).
Chaque jour, tu génères une conversation entre Stephanos (un Athénien d’une trentaine d’années, professeur de lycée) et Anna (une artiste française vivant à Athènes depuis presque 8 ans).
Leurs échanges portent sur des sujets d’actualité grecque ou de la vie quotidienne, avec des références culturelles locales.]"""

url = "https://api.mistral.ai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
    "User-Agent": "daily-dialogue-bot/1.0"
}
payload = {
    "model": "mistral-tiny",
    "messages": [{"role": "user", "content": prompt}],
}

# Retry simple (3 essais) avec timeout
max_retries = 3
for attempt in range(1, max_retries + 1):
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
    except requests.RequestException as e:
        print(f"Request failed (attempt {attempt}): {e}", file=sys.stderr)
        if attempt < max_retries:
            sleep(1 * attempt)
            continue
        else:
            sys.exit(1)

    if not resp.ok:
        # affiche le statut et le message retour (sans exposer la clé)
        print(f"API returned status {resp.status_code}: {resp.text}", file=sys.stderr)
        if attempt < max_retries and resp.status_code >= 500:
            sleep(1 * attempt)
            continue
        sys.exit(1)

    try:
        data = resp.json()
    except ValueError:
        print("Failed to parse JSON response.", file=sys.stderr)
        sys.exit(1)

    # Sécurité: vérifier la présence des champs attendus
    try:
        dialogue = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        print("Unexpected response structure:", data, file=sys.stderr)
        sys.exit(1)

    print(dialogue)
    break