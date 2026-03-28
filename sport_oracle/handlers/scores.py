from telegram import Update
from telegram.ext import ContextTypes
from sport_oracle.services.football_api import get_todays_matches, get_live_scores, format_score


async def scores_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("⏳ Fetching today's matches...")
    try:
        data = await get_todays_matches()
        matches = data.get("matches", [])
        if not matches:
            await update.message.reply_text("📭 No matches scheduled for today.")
            return

        live = [m for m in matches if m.get("status") in ("LIVE", "IN_PLAY", "PAUSED")]
        scheduled = [m for m in matches if m.get("status") == "SCHEDULED"]
        finished = [m for m in matches if m.get("status") == "FINISHED"]

        lines = ["⚽ *Today's Football* ⚽\n"]

        if live:
            lines.append("🔴 *LIVE NOW*")
            for m in live:
                lines.append(format_score(m))
            lines.append("")

        if scheduled:
            lines.append("🕐 *UPCOMING*")
            for m in scheduled[:15]:
                lines.append(format_score(m))
            if len(scheduled) > 15:
                lines.append(f"_...and {len(scheduled) - 15} more_")
            lines.append("")

        if finished:
            lines.append("✅ *RESULTS*")
            for m in finished[:10]:
                lines.append(format_score(m))
            if len(finished) > 10:
                lines.append(f"_...and {len(finished) - 10} more_")

        text = "\n".join(lines)
        if len(text) > 4000:
            text = text[:3990] + "\n_...truncated_"

        await update.message.reply_text(text, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text(f"❌ Error fetching scores: {e}")
