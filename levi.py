import sys
from datetime import datetime

import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode

from config import API_HASH, APP_ID, LOGGER, TG_BOT_WORKERS, \
    FORCE_SUB_CHANNEL_1, FORCE_SUB_CHANNEL_2, FORCE_SUB_CHANNEL_3, FORCE_SUB_CHANNEL_4, \
    CHANNEL_ID
from database.database import Database


class Bot(Client):
    def __init__(self, name="Bot", bot_token=None, db_uri=None, db_name=None):
        super().__init__(
            name=name,
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=bot_token,
        )
        self.LOGGER = LOGGER
        self.label = name
        # Each bot gets its own database connection, so multiple bots can
        # run at once without sharing/clashing user data.
        self.db = Database(db_uri, db_name)

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # FORCE_SUB / CHANNEL_ID are shared across every bot instance.
        force_sub_channels = [
            (FORCE_SUB_CHANNEL_1, "invitelink"),
            (FORCE_SUB_CHANNEL_2, "invitelink2"),
            (FORCE_SUB_CHANNEL_3, "invitelink3"),
            (FORCE_SUB_CHANNEL_4, "invitelink4"),
        ]
        for channel_id, attr in force_sub_channels:
            if not channel_id:
                continue
            try:
                link = (await self.get_chat(channel_id)).invite_link
                if not link:
                    await self.export_chat_invite_link(channel_id)
                    link = (await self.get_chat(channel_id)).invite_link
                setattr(self, attr, link)
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning(f"[{self.label}] Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"[{self.label}] Please Double check the FORCE_SUB channel value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Value: {channel_id}")
                self.LOGGER(__name__).info(f"[{self.label}] Bot Stopped. Join https://t.me/Ahjin_Sprt for support")
                sys.exit()

        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Test Message")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"[{self.label}] Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info(f"[{self.label}] Bot Stopped. Join https://t.me/Ahjin_Sprt for support")
            sys.exit()

        self.set_parse_mode(ParseMode.HTML)
        self.username = usr_bot_me.username
        self.LOGGER(__name__).info(f"[{self.label}] Bot Running..! @{self.username}\n\nCreated by \nhttps://t.me/Ahjin_Sprt")
        self.LOGGER(__name__).info(f"Developer:- @LeviAckerman1709")
        # NOTE: no web server is started here anymore. Running one aiohttp
        # web server per bot instance (each trying to bind the same PORT)
        # is exactly what caused the "port is already in use" error when
        # deploying multiple bots. A single shared web server for the
        # whole process is started once in main.py instead.

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info(f"[{self.label}] Bot stopped.")
