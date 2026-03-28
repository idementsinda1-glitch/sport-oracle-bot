from telegram import Update
from telegram.ext import ContextTypes

WELCOME_TEXT = """⚽ *Welcome to Sport Oracle!* 🔮

Your AI-powered football analysis companion. Here's what I can do:

📊 */scores* — Today's live & scheduled matches
🏆 */league [code]* — Matches & standings for a competition
🔮 */predict [home] vs [away]* — AI match prediction
👤 */player [name] at [team]* — Player scouting report
🎯 */combo [match1], [match2]...* — Build a smart accumulator
📋 */competitions* — List all supported leagues
❓ */help* — Full command guide

*Example commands:*
• `/scores`
• `/predict Arsenal vs Chelsea`
• `/league PL`
• `/player Erling Haaland at Manchester City`
• `/combo Arsenal vs Chelsea, Real Madrid vs Barcelona`

Let's find the edge! 🎯"""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown")
