import anthropic
from sport_oracle.config import ANTHROPIC_API_KEY, CLAUDE_MODEL

_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are Sport Oracle, an expert AI sports analyst specialising in football (soccer).
You have deep knowledge of:
- Team tactics, formations, and playing styles
- Player profiles, strengths, and weaknesses
- Historical head-to-head records and trends
- Competition formats and seasonal context
- Betting markets and value identification

When analysing matches or making predictions:
- Be precise and data-driven when data is provided
- Acknowledge uncertainty honestly
- Structure your response clearly with emojis for readability
- Keep responses concise but insightful (max ~400 words)
- Always include a confidence level (Low / Medium / High) for predictions

Never give financial advice or encourage irresponsible gambling."""


def analyse(prompt: str, context: str = "") -> str:
    full_prompt = f"{context}\n\n{prompt}" if context else prompt
    message = _client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=600,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": full_prompt}],
    )
    return message.content[0].text


def predict_match(home_team: str, away_team: str, competition: str, h2h_context: str = "") -> str:
    prompt = f"""Predict the outcome of: {home_team} vs {away_team} ({competition})

{h2h_context}

Provide:
1. 🏆 Predicted winner (or draw)
2. 📊 Likely scoreline
3. 🔑 Key factors influencing result
4. 📈 Confidence level
5. ⚽ Best bet suggestion (1X2, BTTS, Over/Under goals)"""
    return analyse(prompt)


def build_combo_bet(matches: list[dict]) -> str:
    match_list = "\n".join(
        f"- {m['home']} vs {m['away']} ({m.get('competition', 'Unknown')})"
        for m in matches
    )
    prompt = f"""Build a smart combined accumulator bet from these matches:

{match_list}

For each match suggest:
- Best single pick (1X2 or BTTS or O/U 2.5)
- Reasoning in 1 sentence

Then provide:
- Overall accumulator recommendation
- Risk rating (Low / Medium / High)
- Expected value comment"""
    return analyse(prompt)


def analyse_player(player_name: str, team: str) -> str:
    prompt = f"""Provide a detailed scouting report on {player_name} ({team}):

1. 🌟 Overall rating and role
2. 💪 Key strengths (top 3)
3. ⚠️ Weaknesses/areas to improve
4. 📊 Key stats to watch
5. 🔮 Current season form and impact"""
    return analyse(prompt)


def analyse_standings(competition: str, standings_text: str) -> str:
    prompt = f"""Analyse this {competition} table and provide insights:

{standings_text}

Cover:
1. Title race situation
2. Relegation battle (if applicable)
3. European qualification picture
4. Teams overperforming or underperforming
5. Bold prediction for season end"""
    return analyse(prompt)
