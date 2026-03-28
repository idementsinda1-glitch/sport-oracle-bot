import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from sport_oracle.services import ai_analyst


async def player_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else ""

    if " at " not in text.lower():
        await update.message.reply_text(
            "Usage: `/player [player name] at [team]`\n"
            "Example: `/player Erling Haaland at Manchester City`",
            parse_mode="Markdown",
        )
        return

    parts = text.split(" at ", 1)
    player_name = parts[0].strip().title()
    team = parts[1].strip().title()

    await update.message.reply_text(
        f"👤 Scouting *{player_name}* at *{team}*...\n_Running analysis..._",
        parse_mode="Markdown",
    )

    try:
        loop = asyncio.get_event_loop()
        report = await loop.run_in_executor(
            None,
            ai_analyst.analyse_player,
            player_name,
            team,
        )
        header = f"👤 *Scout Report: {player_name} ({team})*\n\n"
        await update.message.reply_text(header + report, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error generating player report: {e}")
