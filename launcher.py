from asyncio import SelectorEventLoop, set_event_loop
from dotenv import dotenv_values
from core import Twitch




if __name__ == '__main__':
    config = dotenv_values('.env')
    bot = Twitch(config['CLIENT_ID'], config["AI_MODEL"])

    loop = SelectorEventLoop()
    set_event_loop(loop)

    try:
        loop.run_until_complete(bot.run_bot())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()