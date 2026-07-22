import asyncio

from aiohttp import web
from pyrogram import idle

from plugins import web_server
from levi import Bot
from config import BOTS, PORT, LOGGER


async def start_bots():
    bots = []
    for cfg in BOTS:
        bot = Bot(
            name=cfg["name"],
            bot_token=cfg["bot_token"],
            db_uri=cfg["db_uri"],
            db_name=cfg["db_name"],
        )
        try:
            await bot.start()
        except Exception as e:
            LOGGER(__name__).error(f"[{cfg['name']}] failed to start: {e}")
            continue
        bots.append(bot)
        # small delay between logins to stay clear of Telegram flood limits
        # when starting many bots back-to-back
        await asyncio.sleep(2)

    if not bots:
        LOGGER(__name__).error("No bots managed to start. Exiting.")
        return

    # ------------------------------------------------------------------
    # A single, shared web server for the whole process (used by Railway
    # for health checks). Only ONE process binds PORT, no matter how many
    # bots (1-10) are running above — this is what fixes the
    # "port is already in use" crash.
    # ------------------------------------------------------------------
    app_runner = web.AppRunner(await web_server())
    await app_runner.setup()
    await web.TCPSite(app_runner, "0.0.0.0", PORT).start()
    LOGGER(__name__).info(f"Web server started on port {PORT} ({len(bots)} bot(s) running)")

    await idle()

    for bot in bots:
        await bot.stop()
    await app_runner.cleanup()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_bots())
