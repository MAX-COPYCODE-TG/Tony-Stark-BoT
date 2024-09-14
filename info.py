import re
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time
from Script import script 

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
PORT = environ.get("PORT", "8080")
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 9999))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://telegra.ph/file/f909b79e22a4c4bc3a5eb.jpg')).split()
NOR_IMG = environ.get('NOR_IMG', "https://envs.sh/PvY.jpg")
SPELL_IMG = environ.get('SPELL_IMG', "https://graph.org/file/70f66b2e3279e7b1bed5e.jpg")
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
support_chat_id = environ.get('SUPPORT_CHAT_ID')
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '<b>𝖧𝖾𝗅𝗅𝗈{user}!!</b>\n\n<b>𝖨𝗆 𝖠𝗎𝗍𝗈-𝖥𝗂𝗅𝗍𝖾𝗋 𝖡𝗈𝗍 𝖨 𝖼𝖺𝗇 𝖲𝖾𝗇𝖽 𝗒𝗈𝗎 𝖬𝗈𝗏𝗂𝖾 𝗂𝗇 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉𝗌.!!</b>\n\n<b>𝖨 𝖼𝖺𝗇 𝖯𝗋𝗈𝗏𝗂𝖽𝖾 𝗆𝗈𝗏𝗂𝖾𝗌 𝖺𝗇𝖽 𝗐𝖾𝖻-𝗌𝖾𝗋𝗂𝖾𝗌 𝗂𝗇 𝖸𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉𝗌. 𝖨𝗍𝗌 𝖤𝖺𝗌𝗒 𝗍𝗈 𝖴𝗌𝖾 𝗆𝖾 𝖩𝗎𝗌𝗍 𝖺𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗌 𝖺𝖽𝗆𝗂𝗇 𝗍𝗁𝖺𝗍𝗌 𝖺𝗅𝗅 𝗂 𝗐𝗂𝗅𝗅 𝖯𝗋𝗈𝗏𝗂𝖽𝖾 𝖬𝗈𝗏𝗂𝖾𝗌 𝖳𝗁𝖾𝗋𝖾.!!</b>')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "👋𝖧𝖾𝗒 {query}! ഇത് നിന്റെ അല്ല.....🥴")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', '<b>𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 " 🔌 𝖩𝗈𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 🔌 " 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖩𝗈𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝗉𝗋𝖾𝗌𝗌 " 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 🔃 " 𝖻𝗎𝗍𝗍𝗈𝗇 𝗍𝗈 𝗀𝖾𝗍 𝗍𝗁𝖾 𝗆𝗈𝗏𝗂𝖾.!!\n\nതാഴെ കാണുന്ന " 🔌 𝖩𝗈𝗂𝗇 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 🔌 " എന്ന ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത് ചാനലിൽ ജോയിൻ ചെയ്ത ശേഷം " 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 🔃 " എന്ന ബട്ടണിൽ അമർത്തിയാൽ സിനിമ ലഭിക്കുന്നതാണ്.!!</b>')
WELCOM_PIC = environ.get("WELCOM_PIC", "https://graph.org/file/b386a561b6c4a1be48411.jpg")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "<b>ʜᴀɪ {user}\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {chat}</b>")
PMFILTER = bool(environ.get("PMFILTER", True))
G_FILTER = bool(environ.get("G_FILTER", True))
SUPPORT_CHAT_ID = -1002055541286
BUTTON_LOCK = bool(environ.get("BUTTON_LOCK", True))

# Others
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '0').split()]
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "9999"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'chat_group_1100')
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "True")), True)
IMDB = is_enabled((environ.get('IMDB', "None")), None)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
NO_RESULTS_MSG = bool(environ.get('NO_RESULTS_MSG', False))
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "True")), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CUSTOM_FILE_CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>🗂️ Title:</b><code>{search}</code>\n\n<b>⭐ Rating:</b><code><a href={url}/ratings>{rating}</a> / 10</code>\n<b>🎭 Genre:</b> <code>{genres}</code>")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "True")), True)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), False)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)

#log srt
LOG_STR = "Current Cusomized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for you queries.\n" if IMDB else "IMBD Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found , Users will be redirected to send /start to Bot PM instead of sending file file directly\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled files will be send in PM, instead of sending start.\n")
LOG_STR += ("SINGLE_BUTTON is Found, filename and files size will be shown in a single button instead of two separate buttons\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled , filename and file_sixe will be shown as different buttons\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be send along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled , Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode Is Enabled, bot will be suggesting related movies if movie not found\n" if SPELL_CHECK_REPLY else "SPELL_CHECK_REPLY Mode disabled\n")
LOG_STR += (f"MAX_LIST_ELM Found, long list will be shortened to first {MAX_LIST_ELM} elements\n" if MAX_LIST_ELM else "Full List of casts and crew will be shown in imdb template, restrict them by adding a value to MAX_LIST_ELM\n")
LOG_STR += f"Your current IMDB template is {IMDB_TEMPLATE}"


