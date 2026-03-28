import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from sport_oracle.services import ai_analyst


def _parse_matches(text: str) -> list[dict]:
    matches = []
    for part in text.split(","):
        part = part.strip()
        if " vs " in part.lower():
            sides = part.lower().split(" vs ", 1)
            home = sides[0].strip().title()
            away = sides[1].strip().title()
            matches.append({"home": home, "away": away, "competition": "Unknown"})
    return matches


async def combo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = " ".join(context.args) if context.args else ""

    if not text or " vs " not in text.lower():
        await update.message.reply_text(
            "Usage: `/combo [match1], [match2], ...`\n"
            "Example:\n`/combo Arsenal vs Chelsea, Real Madrid vs Barcelona`",
            parse_mode="Markdown",
        )
        return

    matches = _parse_matches(text)

    if not matches:
        await update.message.reply_text(
            "❌ Could not parse any matches. Format each as `Home vs Away`, separated by commas.",
            parse_mode="Markdown",
        )
        return

    match_list = "\n".join(f"• {m['home']} vs {m['away']}" for m in matches)
    await update.message.reply_text(
        f"🎯 Building accumulator for:\n{match_list}\n\n_Analysing with AI..._",
        parse_mode="Markdown",
    )

    try:
        loop = asyncio.get_event_loop()
        combo = await loop.run_in_executor(
            None,
            ai_analyst.build_combo_bet,
            matches,
        )
        header = "🎯 *Sport Oracle Accumulator*\n\n"
        disclaimer = (
            "\n\n⚠️ _For entertainment only. Please gamble responsibly._"
        )
        await update.message.reply_text(header + combo + disclaimer, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error building accumulator: {e}")
