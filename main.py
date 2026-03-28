import logging
from telegram.ext import ApplicationBuilder, CommandHandler

from sport_oracle.config import TELEGRAM_BOT_TOKEN
from sport_oracle.handlers.start import start_command
from sport_oracle.handlers.help import help_command
from sport_oracle.handlers.scores import scores_command
from sport_oracle.handlers.league import league_command, competitions_command
from sport_oracle.handlers.predict import predict_command
from sport_oracle.handlers.player import player_command
from sport_oracle.handlers.combo import combo_command

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Starting Sport Oracle bot...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("scores", scores_command))
    app.add_handler(CommandHandler("league", league_command))
    app.add_handler(CommandHandler("competitions", competitions_command))
    app.add_handler(CommandHandler("predict", predict_command))
    app.add_handler(CommandHandler("player", player_command))
    app.add_handler(CommandHandler("combo", combo_command))

    logger.info("Sport Oracle is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=["message"])


if __name__ == "__main__":
    main()
