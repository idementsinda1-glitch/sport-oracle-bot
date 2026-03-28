import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """Tu es Sport Oracle, un expert IA en analyse sportive.
Analyse les matchs de football avec précision.
Réponds toujours en français avec des emojis et une structure claire."""

def get_ai_analysis(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f" Erreur: {str(e)}"

async def analyze_match(home_team: str, away_team: str, match_data: dict) -> str:
    prompt = f"""Analyse ce match: {home_team} vs {away_team}
Données: {match_data}
Donne: analyse des équipes, prédiction avec probabilités, meilleur pari, niveau de confiance."""
    return get_ai_analysis(prompt)

async def analyze_player(player_name: str, team: str) -> str:
    prompt = f"""Analyse du joueur {player_name} de {team}: stats, points forts/faibles, forme actuelle."""
    return get_ai_analysis(prompt)

async def build_combo(matches: list) -> str:
    prompt = f"""Construis le meilleur combiné avec: {matches}. Paris sûrs, cote totale, niveau de risque."""
    return get_ai_analysis(prompt)
