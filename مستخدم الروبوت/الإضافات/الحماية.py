import random
import re
from datetime import datetime
import asyncio
import pyfiglet
import asyncio
import calendar
import json
import os
from telethon.errors import ChatSendInlineForbiddenError, ChatSendStickersForbiddenError
from telethon import Button, functions
from telethon import events
from telethon.events import CallbackQuery
from telethon.utils import get_display_name
from asyncio.exceptions import TimeoutError
from bs4 import BeautifulSoup
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.messages import ExportChatInviteRequest
from collections import deque
from random import choice
from userbot import iqthon
from userbot.core.logger import logging
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply
from ..helpers.utils import reply_id, _catutils, parse_pre, yaml_format, install_pip, get_user_from_event, _format
from ..sql_helper import global_collectionjson as sql
from ..sql_helper import global_list as sqllist
from ..sql_helper import pmpermit_sql
from ..sql_helper.globals import addgvar, delgvar, gvarstatus
from ..helpers import get_user_from_event, sanga_seperator
from . import mention
from . import ALIVE_NAME, PM_START, PMMENU, PMMESSAGE_CACHE, check, get_user_from_event, parse_pre, set_key
from datetime import datetime
from urllib.parse import quote
import barcode
import qrcode
import requests
from barcode.writer import ImageWriter
from bs4 import BeautifulSoup
from PIL import Image, ImageColor
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot.utils import admin_cmd
from ..helpers import AioHttp
from ..helpers.utils import _catutils, _format, reply_id
CACHE = {}
LOGS = logging.getLogger(__name__)
cmdhd = Config.COMMAND_HAND_LER
async def do_pm_permit_action(event, chat):  
    reply_to_id = await reply_id(event)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    me = await event.client.get_me()
    mention = f"[{chat.first_name}](tg://user?id={chat.id})"
    my_mention = f"[{me.first_name}](tg://user?id={me.id})"
    first = chat.first_name
    last = chat.last_name
    fullname = f"{first} {last}" if last else first
    username = f"@{chat.username}" if chat.username else mention
    userid = chat.id
    my_first = me.first_name
    my_last = me.last_name
    my_fullname = f"{my_first} {my_last}" if my_last else my_first
    my_username = f"@{me.username}" if me.username else my_mention
    if str(chat.id) not in PM_WARNS:
        PM_WARNS[str(chat.id)] = 0
    try:
        MAX_FLOOD_IN_PMS = int(gvarstatus("MAX_FLOOD_IN_PMS") or 10)
    except (ValueError, TypeError):
        MAX_FLOOD_IN_PMS = 10
    totalwarns = MAX_FLOOD_IN_PMS + 1
    warns = PM_WARNS[str(chat.id)] + 1
    remwarns = totalwarns - warns
    if PM_WARNS[str(chat.id)] >= MAX_FLOOD_IN_PMS:
        try:
            if str(chat.id) in PMMESSAGE_CACHE:
                await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
                del PMMESSAGE_CACHE[str(chat.id)]
        except Exception as e:
            LOGS.info(str(e))
        custompmblock = gvarstatus("pmblock") or None
        if custompmblock is not None:
            USER_BOT_WARN_ZERO = custompmblock.format(mention=mention, first=first, last=last, fullname=fullname, username=username, userid=userid, my_first=my_first, my_last=my_last, my_fullname=my_fullname, my_username=my_username, my_mention=my_mention, totalwarns=totalwarns, warns=warns, remwarns=remwarns)
        else:
            USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن الـتـڪـرار . تـم حـظـرڪ ، لا يـمـڪـنـڪ ازعـاج الـمـالـڪ !**"
        msg = await event.reply(USER_BOT_WARN_ZERO)
        await event.client(functions.contacts.BlockRequest(chat.id))
        the_message = f"**⎈ ⦙  الـمـحـضـوريـن مـن الـخـاص : 📩**\n⎈ ⦙   [{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫** \n**⎈ ⦙   عـدد الـرسـائـل :** {PM_WARNS[str(chat.id)]}"
        del PM_WARNS[str(chat.id)]
        sql.del_collection("pmwarns")
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmwarns", PM_WARNS, {})
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
        try:
            return await event.client.send_message(BOTLOG_CHATID,the_message)
        except BaseException:
            return
    custompmpermit = gvarstatus("pmpermit_txt") or None
    if custompmpermit is not None:
        USER_BOT_NO_WARN = custompmpermit.format(mention=mention,first=first,last=last,fullname=fullname,username=username,userid=userid,my_first=my_first,my_last=my_last,my_fullname=my_fullname,my_username=my_username,my_mention=my_mention,totalwarns=totalwarns,warns=warns,remwarns=remwarns)
    elif gvarstatus("pmmenu") is None:
        USER_BOT_NO_WARN = f"𓍹ⵧⵧ𝚂𝙾𝚁𝙲𝙴 𝙰𝙻-𝙰𝙱𝙰𝚀𝙰𝚁𝙸ⵧⵧ𓍻\n\n❞ هـاﺂ هـݪـو٘ {mention} ❝ 🦋\nاﻧـا آݪان ﻣـﺷـغٓول ݪاتࢪﺳـݪ ݪي ࢪﺳـآئݪ ڪﺛـيࢪه وآݪآ سيٰتم حٓـظٍـࢪڪ فقـط قـࢦ سـبب مجـيٰـئڪ اوَ حٰٖـآِجٰتـڪِٰ ، عٰٖـنِ٘ـدمـا آﻋـۅد سِ٘أوافـق علـى ﻣحٰٖـآِډثـتِـك  .. ❞ \n ⤶ ❨  `{warns}/{totalwarns}` ❩\n\n𓍹ⵧⵧ𝚂𝙾𝚁𝙲𝙴 𝙰𝙻-𝙰𝙱𝙰𝚀𝙰𝚁𝙸ⵧⵧ𓍻"
    else:
        USER_BOT_NO_WARN = f"𓍹ⵧⵧ𝚂𝙾𝚁𝙲𝙴 𝙰𝙻-𝙰𝙱𝙰𝚀𝙰𝚁𝙸ⵧⵧ𓍻\n\n❞ هـاﺂ هـݪـو٘ {mention} ❝ 🦋\nاﻧـا آݪان ﻣـﺷـغٓول ݪاتࢪﺳـݪ ݪي ࢪﺳـآئݪ ڪﺛـيࢪه وآݪآ سيٰتم حٓـظٍـࢪڪ فقـط قـࢦ سـبب مجـيٰـئڪ اوَ حٰٖـآِجٰتـڪِٰ ، عٰٖـنِ٘ـدمـا آﻋـۅد سِ٘أوافـق علـى ﻣحٰٖـآِډثـتِـك  .. ❞ \n ⤶ ❨  `{warns}/{totalwarns}` ❩\n\n𓍹ⵧⵧ𝚂𝙾𝚁𝙲𝙴 𝙰𝙻-𝙰𝙱𝙰𝚀𝙰𝚁𝙸ⵧⵧ𓍻"
    addgvar("pmpermit_text", USER_BOT_NO_WARN)
    PM_WARNS[str(chat.id)] += 1
    try:
        if gvarstatus("pmmenu") is None:
            results = await event.client.inline_query(Config.TG_BOT_USERNAME, "pmpermit")
            msg = await results[0].click(chat.id, reply_to=reply_to_id, hide_via=True)
        else:
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            if CAT_IMG is not None:
                msg = await event.client.send_file(chat.id,CAT_IMG,caption=USER_BOT_NO_WARN,reply_to=reply_to_id,force_document=False)
            else:
                msg = await event.client.send_message(chat.id, USER_BOT_NO_WARN, reply_to=reply_to_id)
    except Exception as e:
        LOGS.error(e)
        msg = await event.reply(USER_BOT_NO_WARN)
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    PMMESSAGE_CACHE[str(chat.id)] = msg.id
    sql.del_collection("pmwarns")
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmwarns", PM_WARNS, {})
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})

async def do_pm_options_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if event.sender_id == 1226408155:
            return
    if str(chat.id) not in PM_WARNS:
        text = "**⎈ ⦙  اخـتـࢪ احـد الخـيـاࢪات فـي الأعـلى بـلا تـڪـࢪاࢪ ، وهـذا تـحـذيـࢪڪ الاخـيـࢪ !❕🤍**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**⎈ ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🧸**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**⎈ ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩** \n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .♻️**"
    sqllist.rm_from_list("pmoptions", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return

async def do_pm_enquire_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**⎈ ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك  .🌀 \n ⎈ ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه .. \n ⎈ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🙂🌿**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        # await asyncio.sleep(5)
        # await msg.delete()
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**⎈ ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🧸**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**⎈ ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩** \n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .♻️**"
    sqllist.rm_from_list("pmenquire", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID,the_message)
    except BaseException:
        return

async def do_pm_request_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**⎈ ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك  🌀. \n ⎈ ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه . . \n ⎈ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🙂🌿**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**⎈ ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🧸**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**⎈ ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .♻️**"
    sqllist.rm_from_list("pmrequest", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return

async def do_pm_chat_action(event, chat):
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    if str(chat.id) not in PM_WARNS:
        text = "**⎈ ⦙  يـرجـى الانـتـظـار لــ حـيـن قرائة رسالتك  🌀. \n ⎈ ⦙   مـالـڪ الـحـسـاب سَــوف يـرد عـلـيـڪ عـنـد اسـتـطـاعـتـه . . \n ⎈ ⦙   يـرجـى عـدم تـڪـرار الـرسـائـل لـتـجـنـب الـحـظـر 🙂🌿**"
        await event.reply(text)
        PM_WARNS[str(chat.id)] = 1
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
        return None
    del PM_WARNS[str(chat.id)]
    sql.del_collection("pmwarns")
    sql.add_collection("pmwarns", PM_WARNS, {})
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    sql.del_collection("pmmessagecache")
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**⎈ ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🧸**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**⎈ ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .♻️**"
    sqllist.rm_from_list("pmchat", chat.id)
    try:
        return await event.client.send_message(BOTLOG_CHATID, the_message)
    except BaseException:
        return
async def do_pm_spam_action(event, chat):
    try:
        PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
    except AttributeError:
        PMMESSAGE_CACHE = {}
    try:
        if str(chat.id) in PMMESSAGE_CACHE:
            await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            del PMMESSAGE_CACHE[str(chat.id)]
    except Exception as e:
        LOGS.info(str(e))
    USER_BOT_WARN_ZERO = f"**⎈ ⦙  تـم تـحـذيـرڪ مـسـبـقـاً مـن تـڪـرار الـرسـائـل .** \n**⎈ ⦙   تـم حـظـرڪ مـن الـحـسـاب 🚫.** \n**⎈ ⦙  لـن اسـتـلـم رسـائـلـڪ الـى ان يـاتـي مـالـڪ الـحـسـاب .🧸**"
    await event.reply(USER_BOT_WARN_ZERO)
    await event.client(functions.contacts.BlockRequest(chat.id))
    the_message = f"**⎈ ⦙  حـمـايـة الـخـاص  (الـبـرايـفـت)  : 📩**\n[{get_display_name(chat)}](tg://user?id={chat.id}) **تـم حـظـر الـمـسـتـخـدم .🗣🚫**\n**⎈ ⦙  الـسـبـب ~> اسـتـمـر بـالـتـكـرار .♻️**"
    sqllist.rm_from_list("pmspam", chat.id)
    sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})
    try:
        return await event.client.send_message(BOTLOG_CHATID,the_message)
    except BaseException:
        return

@iqthon.iq_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def on_new_private_message(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if pmpermit_sql.is_approved(chat.id):
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return await do_pm_spam_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return await do_pm_chat_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return await do_pm_request_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return await do_pm_enquire_action(event, chat)
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return await do_pm_options_action(event, chat)
    await do_pm_permit_action(event, chat)

@iqthon.iq_cmd(outgoing=True, func=lambda e: e.is_private, edited=False, forword=None)
async def you_dm_other(event):
    if gvarstatus("pmpermit") is None:
        return
    chat = await event.get_chat()
    if chat.bot or chat.verified:
        return
    if str(chat.id) in sqllist.get_collection_list("pmspam"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmchat"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmrequest"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmenquire"):
        return
    if str(chat.id) in sqllist.get_collection_list("pmoptions"):
        return
    if event.text and event.text.startswith(
        (
            f"{cmdhd}مرفوض",
            f"{cmdhd}رفض",
            f"{cmdhd}س",
            f"{cmdhd}ر",
            f"{cmdhd}سماح",
        )
    ):
        return
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    start_date = str(datetime.now().strftime("%B %d, %Y"))
    if not pmpermit_sql.is_approved(chat.id) and str(chat.id) not in PM_WARNS:
        pmpermit_sql.approve(chat.id, get_display_name(chat), start_date, chat.username, "**⎈ ⦙  خـطـأ ~> لـم يـتـم رفـضـه .⭕️**")
        try:
            PMMESSAGE_CACHE = sql.get_collection("pmmessagecache").json
        except AttributeError:
            PMMESSAGE_CACHE = {}
        if str(chat.id) in PMMESSAGE_CACHE:
            try:
                await event.client.delete_messages(chat.id, PMMESSAGE_CACHE[str(chat.id)])
            except Exception as e:
                LOGS.info(str(e))
            del PMMESSAGE_CACHE[str(chat.id)]
        sql.del_collection("pmmessagecache")
        sql.add_collection("pmmessagecache", PMMESSAGE_CACHE, {})

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"show_pmpermit_options")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**⎈ ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 🧸♥️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = f"**حسنا الان بإمكانك اختيار احد الخيارات في الاسفل للتواصل مع :** {mention}.\n**⎈ ⦙   اختر بهدوء خيار واحد فقط لنعرف سبب قدومك هنا 🤍**\n**⎈ ⦙   هذه الخيارات في الاسفل اختر واحد فقط ⬇️**"
    buttons = [
        (Button.inline(text="⚜️︙إسـتـفـسـار مـعـيـن .", data="to_enquire_something"),),
        (Button.inline(text="⚜️︙طـلـب مـعـيـن .", data="to_request_something"),),
        (Button.inline(text="⚜️︙الـدردشـة .", data="to_chat_with_my_master"),),
        (Button.inline(text="⚜️︙إزعـاج الـمـالـڪ .", data="to_spam_my_master_inbox"),),
    ]
    sqllist.add_to_list("pmoptions", event.query.user_id)
    try:
        PM_WARNS = sql.get_collection("pmwarns").json
    except AttributeError:
        PM_WARNS = {}
    if str(event.query.user_id) in PM_WARNS:
        del PM_WARNS[str(event.query.user_id)]
        sql.del_collection("pmwarns")
        sql.add_collection("pmwarns", PM_WARNS, {})
    await event.edit(text, buttons=buttons)

@iqthon.tgbot.on(CallbackQuery(data=re.compile(rb"to_enquire_something")))
async def on_plug_in_callback_query_handler(event):
    if event.query.user_id == event.client.uid:
        text = "**⎈ ⦙   عـذرا ، هـذه الـخـيـارات لـلـمـسـتـخـدم الـذي يـراسـلـك 🧸♥️**"
        return await event.answer(text, cache_time=0, alert=True)
    text = "**⎈ ⦙  حـسـن
