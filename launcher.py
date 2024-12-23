"""
The MIT License (MIT)

Copyright (c) 2024-present Snifo

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from __future__ import annotations

from dotenv import dotenv_values
from twitch import setup_logging
from typing import TYPE_CHECKING
from core import TwitchBot
import asyncio
import logging

if TYPE_CHECKING:
    from typing import Dict, Optional

setup_logging(level=logging.INFO)
_logger = logging.getLogger(__name__)

def main() -> None:
    config: Dict[str, Optional[str]] = dotenv_values('.env')

    # CLI: https://twitchpy.readthedocs.io/v3.2.6/reference/debug/
    bot: TwitchBot = TwitchBot(client_id=config['CLIENT_ID'], ai_model=config['AI_MODEL'], cli=False)

    # Start da bot.
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
