import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are Sport Oracle, an expert AI sports analyst. 
Analyze football matches with detailed statistics, predictions, and betting insights.
Always respond in French with emojis and clear structure."""

def get_ai_analysis(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(SYSTEM_PROMPT + "\n\n" + prompt)
        return response.text
    except Exception as e:
        return f"❌ Erreur analyse: {str(e)}"

async def analyze_match(home_team: str, away_team: str, match_data: dict) -> str:
    prompt = f"""Analyse ce match de football:
{home_team} vs {away_team}

Données: {match_data}

Donne:
1. Analyse des deux équipes
2. Prédiction du résultat avec probabilités
3. Meilleur pari recommandé
4. Niveau de confiance"""
    return get_ai_analysis(prompt)

async def analyze_player(player_name: str, team: str) -> str:
    prompt = f"""Analyse complète du joueur {player_name} de {team}:
- Stats récentes
- Points forts/faibles  
- Forme actuelle
- Impact sur l'équipe"""
    return get_ai_analysis(prompt)

async def build_combo(matches: list) -> str:
    prompt = f"""Construis le meilleur combiné avec ces matchs: {matches}
- Sélectionne les paris les plus sûrs
- Calcule la cote totale estimée
- Donne le niveau de risque"""
    return get_ai_analysis(prompt)
