from telegram import Update
from telegram.ext import ContextTypes

HELP_TEXT = """⚽ *Sport Oracle — Command Guide* 🔮

━━━━━━━━━━━━━━━━━━━
📊 *LIVE & TODAY'S SCORES*
━━━━━━━━━━━━━━━━━━━
`/scores` — All today's matches (live + scheduled)

━━━━━━━━━━━━━━━━━━━
🏆 *LEAGUE INFO*
━━━━━━━━━━━━━━━━━━━
`/league [code]` — Fixtures & table
`/league PL` → Premier League
`/league CL` → Champions League
`/competitions` → Full list of codes

━━━━━━━━━━━━━━━━━━━
🔮 *AI PREDICTIONS*
━━━━━━━━━━━━━━━━━━━
`/predict [home] vs [away]`
Example: `/predict Liverpool vs Arsenal`

━━━━━━━━━━━━━━━━━━━
👤 *PLAYER STATS*
━━━━━━━━━━━━━━━━━━━
`/player [name] at [team]`
Example: `/player Vinicius Jr at Real Madrid`

━━━━━━━━━━━━━━━━━━━
🎯 *COMBO BETS*
━━━━━━━━━━━━━━━━━━━
`/combo [match1], [match2], ...`
Example:
`/combo Arsenal vs Chelsea, Real Madrid vs Barcelona`

━━━━━━━━━━━━━━━━━━━
⚠️ *Disclaimer*
━━━━━━━━━━━━━━━━━━━
Sport Oracle provides analysis for entertainment purposes only. Always gamble responsibly. 🙏"""


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(HELP_TEXT, parse_mode="Markdown")
