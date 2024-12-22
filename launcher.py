from dotenv import dotenv_values
from twitch import setup_logging
from core import TwitchBot
import asyncio
import logging

setup_logging(level=logging.INFO)
_logger = logging.getLogger(__name__)

def main():
    config = dotenv_values('.env')
    bot = TwitchBot(client_id=config['CLIENT_ID'], ai_model=config['AI_MODEL'], cli=False)

    try:
        _logger.info("Starting the Twitch bot...")
        asyncio.run(bot.run_bot())
    except KeyboardInterrupt:
        _logger.info("Bot interrupted by user. Shutting down...")
    except Exception as e:
        _logger.error(f"An error occurred: {e}")
    finally:
        _logger.info("Bot has stopped.")


if __name__ == '__main__':
    main()
