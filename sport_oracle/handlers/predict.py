import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from sport_oracle.services import ai_analyst


async def predict_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else ""

    if " vs " not in text.lower():
        await update.message.reply_text(
            "Usage: `/predict [home team] vs [away team]`\n"
            "Example: `/predict Arsenal vs Chelsea`",
            parse_mode="Markdown",
        )
        return

    parts = text.lower().split(" vs ", 1)
    home = parts[0].strip().title()
    away_raw = parts[1].strip()

    competition = "Unknown Competition"
    if " in " in away_raw.lower():
        away_parts = away_raw.lower().split(" in ", 1)
        away = away_parts[0].strip().title()
        competition = away_parts[1].strip().title()
    else:
        away = away_raw.title()

    await update.message.reply_text(
        f"🔮 Analysing *{home}* vs *{away}*...\n_Consulting the Oracle..._",
        parse_mode="Markdown",
    )

    try:
        loop = asyncio.get_event_loop()
        prediction = await loop.run_in_executor(
            None,
            ai_analyst.predict_match,
            home,
            away,
            competition,
            "",
        )
        header = f"🔮 *Prediction: {home} vs {away}*\n\n"
        await update.message.reply_text(header + prediction, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error generating prediction: {e}")
