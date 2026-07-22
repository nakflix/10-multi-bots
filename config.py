#(©)t.me/Ahjin_Sprt
# Multi-bot config — supports deploying multiple bots (each with its own
# bot token + database) from a single codebase/deployment.

import os
import logging
from logging.handlers import RotatingFileHandler


# ----------------------------------------------------------------------
# SHARED SETTINGS (same for every bot instance — no need to change per bot)
# ----------------------------------------------------------------------

# Your API ID / Hash from my.telegram.org (same app credentials can be
# reused for every bot token)
APP_ID = int(os.environ.get("APP_ID", "14298205"))
API_HASH = os.environ.get("API_HASH", "28df6d84da76d8606bf5f0e71ecfb62c")

# Your database channel Id (shared across all bots)
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1001755253960"))

# OWNER ID (shared across all bots)
OWNER_ID = int(os.environ.get("OWNER_ID", "1458235021"))

# Single PORT exposed by the deployment (Railway injects this). Only ONE
# web server is started for the whole process (see main.py) no matter how
# many bots are running, so there is no "port already in use" clash.
PORT = int(os.environ.get("PORT", "8080"))

# force sub channel id, if you want enable force sub (shared across all bots)
FORCE_SUB_CHANNEL_1 = int(os.environ.get("FORCE_SUB_CHANNEL_1", "-1001899642588"))
FORCE_SUB_CHANNEL_2 = int(os.environ.get("FORCE_SUB_CHANNEL_2", "-1001840563301"))
FORCE_SUB_CHANNEL_3 = int(os.environ.get("FORCE_SUB_CHANNEL_3", "-1001858199915"))
FORCE_SUB_CHANNEL_4 = int(os.environ.get("FORCE_SUB_CHANNEL_4", "-1001878979530"))

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "4"))

# start message
START_MSG = os.environ.get("START_MESSAGE", "<b>Hello {first}\nI store private files for @NAKFLIXTV.</b>")

try:
    ADMINS = [5976081364]
    for x in (os.environ.get("ADMINS", "1458235021").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")

# Force sub message
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "<b>Hello👋 {first}</b>\n<b>Kindly JOIN CHANNEL 1, 2, 3 and 4 Then press ♻️ Try Again ♻️ to continue. 👇</b>")

# set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "➥ 𝗩𝗜𝗦𝗜𝗧 & 𝗝𝗢𝗜𝗡 👉 @NAKFLIXTV")

# set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

# Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Send your request here 👉<a href='https://t.me/nakflix_bot?start='>@NAKFLIX_BOT</a>🤏"

ADMINS.append(OWNER_ID)
ADMINS.append(1737646273)

LOG_FILE_NAME = "logs.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


# ----------------------------------------------------------------------
# PER-BOT SETTINGS (each bot gets its own token + database)
# ----------------------------------------------------------------------
# Configure each bot with numbered env vars, from 1 up to MAX_BOTS (10):
#
#   BOT_TOKEN_1=...          (required to enable bot #1)
#   DATABASE_URL_1=...       (mongo connection string for bot #1)
#   DATABASE_NAME_1=...      (optional, defaults to FileShareDB_1)
#   BOT_NAME_1=...           (optional, friendly name used in logs/session file)
#
#   BOT_TOKEN_2=...
#   DATABASE_URL_2=...
#   ... and so on up to _10
#
# Any slot without a BOT_TOKEN_<n> is simply skipped, so you can run
# anywhere from 1 to 10 bots. FORCE_SUB / OWNER_ID / CHANNEL_ID above are
# shared by every bot and do not need to be repeated.

MAX_BOTS = int(os.environ.get("MAX_BOTS", "10"))

# Fallback single-bot vars (kept for backward compatibility with the
# original single-bot deployments of this repo)
_LEGACY_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "8652870030:AAG6v5WSyYGztsi9L4AUNPaLHz9wbmTjWg4")
_LEGACY_DB_URI = os.environ.get("DATABASE_URL", "mongodb+srv://Alphanakflix:alpha3720@netflixtvshowsbot.wrc5c.mongodb.net/?retryWrites=true&w=majority")
_LEGACY_DB_NAME = os.environ.get("DATABASE_NAME", "FileSharedb")

BOTS = []
for i in range(1, MAX_BOTS + 1):
    bot_token = os.environ.get(f"BOT_TOKEN_{i}")
    if not bot_token:
        continue
    db_uri = os.environ.get(f"DATABASE_URL_{i}", _LEGACY_DB_URI)
    db_name = os.environ.get(f"DATABASE_NAME_{i}", f"FileShareDB_{i}")
    bot_name = os.environ.get(f"BOT_NAME_{i}", f"Bot{i}")
    BOTS.append({
        "index": i,
        "name": bot_name,
        "bot_token": bot_token,
        "db_uri": db_uri,
        "db_name": db_name,
    })

# If no numbered BOT_TOKEN_<n> vars were set, fall back to the classic
# single-bot env vars so old deployments keep working unchanged.
if not BOTS and _LEGACY_BOT_TOKEN:
    BOTS.append({
        "index": 1,
        "name": "Bot1",
        "bot_token": _LEGACY_BOT_TOKEN,
        "db_uri": _LEGACY_DB_URI,
        "db_name": _LEGACY_DB_NAME,
    })

if not BOTS:
    raise Exception(
        "No bots configured! Set BOT_TOKEN_1 (and DATABASE_URL_1) at minimum, "
        "or the legacy TG_BOT_TOKEN / DATABASE_URL vars."
    )

# Kept for any code/plugins that still import a single TG_BOT_TOKEN /
# DB_URI / DB_NAME (points at the first configured bot).
TG_BOT_TOKEN = BOTS[0]["bot_token"]
DB_URI = BOTS[0]["db_uri"]
DB_NAME = BOTS[0]["db_name"]
