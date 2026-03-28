from telegram import Update
from telegram.ext import ContextTypes
from sport_oracle.services.football_api import (
    get_competition_matches,
    get_competition_standings,
    format_score,
)
from sport_oracle.config import SUPPORTED_COMPETITIONS


async def competitions_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lines = ["🏆 *Supported Competitions*\n"]
    for code, name in SUPPORTED_COMPETITIONS.items():
        lines.append(f"`{code}` — {name}")
    lines.append("\nUsage: `/league PL`")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def league_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text(
            "Usage: `/league [code]`\nExample: `/league PL`\nSee `/competitions` for codes.",
            parse_mode="Markdown",
        )
        return

    code = context.args[0].upper()
    if code not in SUPPORTED_COMPETITIONS:
        await update.message.reply_text(
            f"❓ Unknown competition `{code}`. Use `/competitions` for the full list.",
            parse_mode="Markdown",
        )
        return

    name = SUPPORTED_COMPETITIONS[code]
    await update.message.reply_text(f"⏳ Fetching {name} data...")

    try:
        matches_data = await get_competition_matches(code)
        matches = matches_data.get("matches", [])

        live = [m for m in matches if m.get("status") in ("LIVE", "IN_PLAY", "PAUSED")]
        upcoming = [m for m in matches if m.get("status") == "SCHEDULED"][:8]
        recent = [m for m in matches if m.get("status") == "FINISHED"][-5:]

        lines = [f"🏆 *{name}*\n"]

        if live:
            lines.append("🔴 *LIVE*")
            for m in live:
                lines.append(format_score(m))
            lines.append("")

        if upcoming:
            lines.append("🕐 *Upcoming Fixtures*")
            for m in upcoming:
                lines.append(format_score(m))
            lines.append("")

        if recent:
            lines.append("✅ *Recent Results*")
            for m in recent:
                lines.append(format_score(m))
            lines.append("")

        try:
            standings_data = await get_competition_standings(code)
            table = standings_data.get("standings", [{}])[0].get("table", [])[:5]
            if table:
                lines.append("📊 *Top 5 Standings*")
                for row in table:
                    pos = row["position"]
                    team = row["team"]["name"]
                    pts = row["points"]
                    played = row["playedGames"]
                    lines.append(f"{pos}. {team} — {pts}pts ({played}G)")
        except Exception:
            pass

        text = "\n".join(lines)
        if len(text) > 4000:
            text = text[:3990] + "\n_...truncated_"

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching {name} data: {e}")
