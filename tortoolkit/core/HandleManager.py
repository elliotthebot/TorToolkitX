# -*- coding: utf-8 -*-
# (c) YashDK [yash-dk@github]
# (c) modified by AmirulAndalib [amirulandalib@github]

from telethon import TelegramClient,events 
from telethon import __version__ as telever
from pyrogram import __version__ as pyrover
from telethon.tl.types import KeyboardButtonCallback
from ..consts.ExecVarsSample import ExecVars
from ..core.getCommand import get_command
from ..core.getVars import get_val
from ..core.speedtest import get_speed
from ..functions.Leech_Module import check_link,cancel_torrent,pause_all,resume_all,purge_all,get_status,print_files, get_transfer
from ..functions.tele_upload import upload_a_file,upload_handel
from ..functions import Human_Format
from .database_handle import TtkUpload,TtkTorrents, TorToolkitDB
from .settings import handle_settings,handle_setting_callback
from .user_settings import handle_user_settings, handle_user_setting_callback
from functools import partial
from ..functions.rclone_upload import get_config,rclone_driver
from ..functions.admin_check import is_admin
from .. import upload_db, var_db, tor_db, user_db, uptime
import asyncio as aio
import re,logging,time,os,psutil,shutil
from tortoolkit import __version__
from .ttk_ytdl import handle_ytdl_command,handle_ytdl_callbacks,handle_ytdl_file_download,handle_ytdl_playlist,handle_ytdl_playlist_down
from ..functions.instadl import _insta_post_downloader
torlog = logging.getLogger(__name__)
from .status.status import Status
from .status.menu import create_status_menu, create_status_user_menu
import signal
from PIL import Image

def add_handlers(bot: TelegramClient):
    #bot.add_event_handler(handle_leech_command,events.NewMessage(func=lambda e : command_process(e,get_command("LEECH")),chats=ExecVars.ALD_USR))
    
    bot.add_event_handler(
        handle_leech_command,
        events.NewMessage(pattern=command_process(get_command("LEECH")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_purge_command,
        events.NewMessage(pattern=command_process(get_command("PURGE")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_pauseall_command,
        events.NewMessage(pattern=command_process(get_command("PAUSEALL")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_resumeall_command,
        events.NewMessage(pattern=command_process(get_command("RESUMEALL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_status_command,
        events.NewMessage(pattern=command_process(get_command("STATUS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_u_status_command,
        events.NewMessage(pattern=command_process(get_command("USTATUS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_settings_command,
        events.NewMessage(pattern=command_process(get_command("SETTINGS")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_exec_message_f,
        events.NewMessage(pattern=command_process(get_command("EXEC")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        upload_document_f,
        events.NewMessage(pattern=command_process(get_command("UPLOAD")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_ytdl_command,
        events.NewMessage(pattern=command_process(get_command("YTDL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_ytdl_playlist,
        events.NewMessage(pattern=command_process(get_command("PYTDL")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        about_me,
        events.NewMessage(pattern=command_process(get_command("ABOUT")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        get_logs_f,
        events.NewMessage(pattern=command_process(get_command("GETLOGS")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        handle_test_command,
        events.NewMessage(pattern="/test",
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_server_command,
        events.NewMessage(pattern=command_process(get_command("SERVER")),
        chats=get_val("ALD_USR"))
    )
    
    bot.add_event_handler(
        set_password_zip,
        events.NewMessage(pattern=command_process("/setpass"),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        handle_user_settings_,
        events.NewMessage(pattern=command_process(get_command("USERSETTINGS")))
    )

    bot.add_event_handler(
        _insta_post_downloader,
        events.NewMessage(pattern=command_process(get_command("INSTADL")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        start_handler,
        events.NewMessage(pattern=command_process(get_command("START")))
    )

    bot.add_event_handler(
        clear_thumb_cmd,
        events.NewMessage(pattern=command_process(get_command("CLRTHUMB")),
        chats=get_val("ALD_USR"))
    )

    bot.add_event_handler(
        set_thumb_cmd,
        events.NewMessage(pattern=command_process(get_command("SETTHUMB")),
        chats=get_val("ALD_USR"))
    )
# REMOVED HEROKU BLOCK
    bot.add_event_handler(
        speed_handler,
        events.NewMessage(pattern=command_process(get_command("SPEEDTEST")),
        chats=get_val("ALD_USR"))
    )


    signal.signal(signal.SIGINT, partial(term_handler,client=bot))
    signal.signal(signal.SIGTERM, partial(term_handler,client=bot))
    bot.loop.run_until_complete(booted(bot))

    #*********** Callback Handlers *********** 
    
    bot.add_event_handler(
        callback_handler_canc,
        events.CallbackQuery(pattern="torcancel")
    )

    bot.add_event_handler(
        handle_settings_cb,
        events.CallbackQuery(pattern="setting")
    )

    bot.add_event_handler(
        handle_upcancel_cb,
        events.CallbackQuery(pattern="upcancel")
    )

    bot.add_event_handler(
        handle_pincode_cb,
        events.CallbackQuery(pattern="getpin")
    )

    bot.add_event_handler(
        handle_ytdl_callbacks,
        events.CallbackQuery(pattern="ytdlsmenu")
    )

    bot.add_event_handler(
        handle_ytdl_callbacks,
        events.CallbackQuery(pattern="ytdlmmenu")
    )
    
    bot.add_event_handler(
        handle_ytdl_file_download,
        events.CallbackQuery(pattern="ytdldfile")
    )
    
    bot.add_event_handler(
        handle_ytdl_playlist_down,
        events.CallbackQuery(pattern="ytdlplaylist")
    )

    bot.add_event_handler(
        handle_user_setting_callback,
        events.CallbackQuery(pattern="usetting")
    )
    bot.add_event_handler(
        handle_server_command,
        events.CallbackQuery(pattern="fullserver")
    )

# REMOVED HEROKU BLOCK
#*********** Handlers Below ***********

async def handle_leech_command(e):
    if not e.is_reply:
        await e.reply("⚡𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝗹𝗶𝗻𝗸 𝗼𝗿 𝗺𝗮𝗴𝗻𝗲𝘁")
    else:
        rclone = False
        tsp = time.time()
        buts = [[KeyboardButtonCallback("📦𝗧𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺📦",data=f"leechselect tg {tsp}")]]
        if await get_config() is not None:
            buts.append(
                [KeyboardButtonCallback("📤𝗧𝗼 𝗗𝗿𝗶𝘃𝗲📤",data=f"leechselect drive {tsp}")]
            )
        # tsp is used to split the callbacks so that each download has its own callback
        # cuz at any time there are 10-20 callbacks linked for leeching XD
           
        buts.append(
                [KeyboardButtonCallback("🤐𝗨𝗽𝗹𝗼𝗮𝗱 𝗶𝗻 𝗮 𝗭𝗜𝗣.[𝗧𝗼𝗴𝗴𝗹𝗲🔰]", data=f"leechzip toggle {tsp}")]
        )
        buts.append(
                [KeyboardButtonCallback("🗜️𝗘𝘅𝘁𝗿𝗮𝗰𝘁 𝗳𝗿𝗼𝗺 𝗔𝗿𝗰𝗵𝗶𝘃𝗲.[𝗧𝗼𝗴𝗴𝗹𝗲🔰]", data=f"leechzipex toggleex {tsp}")]
        )
        
        conf_mes = await e.reply(f"𝗙𝗶𝗿𝘀𝘁 𝗰𝗹𝗶𝗰𝗸 𝗶𝗳 𝘆𝗼𝘂 𝘄𝗮𝗻𝘁 𝘁𝗼 𝘇𝗶𝗽 𝘁𝗵𝗲 𝗰𝗼𝗻𝘁𝗲𝗻𝘁𝘀 𝗼𝗿 𝗲𝘅𝘁𝗿𝗮𝗰𝘁 𝗮𝘀 𝗮𝗻 𝗮𝗿𝗰𝗵𝗶𝘃𝗲 (𝗼𝗻𝗹𝘆 𝗼𝗻𝗲 𝘄𝗶𝗹𝗹 𝘄𝗼𝗿𝗸 𝗮𝘁 𝗮 𝘁𝗶𝗺𝗲) 𝘁𝗵𝗲𝗻...\n\n✅𝗖𝗵𝗼𝗼𝘀𝗲 𝘄𝗵𝗲𝗿𝗲 𝘁𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝘆𝗼𝘂𝗿 𝗳𝗶𝗹𝗲𝘀:-\n𝗧𝗵𝗲 𝗳𝗶𝗹𝗲𝘀 𝘄𝗶𝗹𝗹 𝗯𝗲 𝘂𝗽𝗹𝗼𝗮𝗱𝗲𝗱 𝘁𝗼 𝗱𝗲𝗳𝗮𝘂𝗹𝘁 𝗱𝗲𝘀𝘁𝗶𝗻𝗮𝘁𝗶𝗼𝗻: <b>{get_val('DEFAULT_TIMEOUT')}</b> 𝗮𝗳𝘁𝗲𝗿 𝟲𝟬 𝘀𝗲𝗰 𝗼𝗳 𝗻𝗼 𝗮𝗰𝘁𝗶𝗼𝗻 𝗯𝘆 𝘂𝘀𝗲𝗿.</u>\n\n𝗦𝘂𝗽𝗽𝗼𝗿𝘁𝗲𝗱 𝗮𝗿𝗰𝗵𝗶𝘃𝗲𝘀 𝘁𝗼 𝗲𝘅𝘁𝗿𝗮𝗰𝘁:\n<code>zip, 7z, tar, gzip2, iso, wim, rar, tar.gz, tar.bz2</code>",parse_mode="html",buttons=buts)

        # zip check in background
        ziplist = await get_zip_choice(e,tsp)
        zipext = await get_zip_choice(e,tsp,ext=True)
        
        # blocking leech choice 
        choice = await get_leech_choice(e,tsp)
        
        # zip check in backgroud end
        await get_zip_choice(e,tsp,ziplist,start=False)
        await get_zip_choice(e,tsp,zipext,start=False,ext=True)
        is_zip = ziplist[1]
        is_ext = zipext[1]
        
        
        # Set rclone based on choice
        if choice == "drive":
            rclone = True
        else:
            rclone = False
        
        await conf_mes.delete()

        if rclone:
            if get_val("RCLONE_ENABLED"):
                await check_link(e,rclone, is_zip, is_ext, conf_mes)
            else:
                await e.reply("❌𝗗𝗥𝗜𝗩𝗘 𝗜𝗦 𝗗𝗜𝗦𝗔𝗕𝗟𝗘𝗗 𝗕𝗬 𝗧𝗛𝗘 𝗔𝗗𝗠𝗜𝗡",parse_mode="html")
        else:
            if get_val("LEECH_ENABLED"):
                await check_link(e,rclone, is_zip, is_ext, conf_mes)
            else:
                await e.reply("❌𝗧𝗚 𝗟𝗘𝗘𝗖𝗛 𝗜𝗦 𝗗𝗜𝗦𝗔𝗕𝗟𝗘𝗗 𝗕𝗬 𝗧𝗛𝗘 𝗔𝗗𝗠𝗜𝗡",parse_mode="html")


async def get_leech_choice(e,timestamp):
    # abstract for getting the confirm in a context

    lis = [False,None]
    cbak = partial(get_leech_choice_callback,o_sender=e.sender_id,lis=lis,ts=timestamp)
    
# REMOVED HEROKU BLOCK


    e.client.add_event_handler(
        #lambda e: test_callback(e,lis),
        cbak,
        events.CallbackQuery(pattern="leechselect")
    )

    start = time.time()
    defleech = get_val("DEFAULT_TIMEOUT")

    while not lis[0]:
        if (time.time() - start) >= 60: #TIMEOUT_SEC:
            
            if defleech == "leech":
                return "tg"
            elif defleech == "rclone":
                return "drive"
            else:
                # just in case something goes wrong
                return "tg"
            break
        await aio.sleep(1)

    val = lis[1]
    
    e.client.remove_event_handler(cbak)

    return val

async def get_zip_choice(e,timestamp, lis=None,start=True, ext=False):
    # abstract for getting the confirm in a context
    # creating this functions to reduce the clutter
    if lis is None:
        lis = [None, None, None]
    
    if start:
        cbak = partial(get_leech_choice_callback,o_sender=e.sender_id,lis=lis,ts=timestamp)
        lis[2] = cbak
        if ext:
            e.client.add_event_handler(
                cbak,
                events.CallbackQuery(pattern="leechzipex")
            )
        else:
            e.client.add_event_handler(
                cbak,
                events.CallbackQuery(pattern="leechzip")
            )
        return lis
    else:
        e.client.remove_event_handler(lis[2])


async def get_leech_choice_callback(e,o_sender,lis,ts):
    # handle the confirm callback

    if o_sender != e.sender_id:
        return
    data = e.data.decode().split(" ")
    if data [2] != str(ts):
        return
    
    lis[0] = True
    if data[1] == "toggle":
        # encompasses the None situation too
        print("data ",lis)
        if lis[1] is True:
            await e.answer("❌𝗪𝗶𝗹𝗹 𝗡𝗼𝘁 𝗯𝗲 𝘇𝗶𝗽𝗽𝗲𝗱", alert=True)
            lis[1] = False 
        else:
            await e.answer("✅𝗪𝗶𝗹𝗹 𝗯𝗲 𝘇𝗶𝗽𝗽𝗲𝗱", alert=True)
            lis[1] = True
    elif data[1] == "toggleex":
        print("exdata ",lis)
        # encompasses the None situation too
        if lis[1] is True:
            await e.answer("❌𝗜𝘁 𝘄𝗶𝗹𝗹 𝗻𝗼𝘁 𝗯𝗲 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱", alert=True)
            lis[1] = False 
        else:
            await e.answer("ℹ️𝗜𝗳 𝗶𝘁 𝗶𝘀 𝗮 𝗔𝗿𝗰𝗵𝗶𝘃𝗲 𝗶𝘁 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗲𝘅𝘁𝗿𝗮𝗰𝘁𝗲𝗱. 𝗙𝘂𝗿𝘁𝗵𝗲𝗿 𝗶𝗻 𝘆𝗼𝘂 𝗰𝗮𝗻 𝘀𝗲𝘁 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝘁𝗼 𝗲𝘅𝘁𝗿𝗮𝗰𝘁 𝘁𝗵𝗲 𝗭𝗜𝗣...", alert=True)
            lis[1] = True
    else:
        lis[1] = data[1]
    

#add admin checks here - done
async def handle_purge_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await purge_all(e)
    else:
        await e.delete()

# REMOVED HEROKU BLOCK

async def handle_pauseall_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await pause_all(e)
    else:
        await e.delete()

async def handle_resumeall_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await resume_all(e)
    else:
        await e.delete()

async def handle_settings_command(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await handle_settings(e)
    else:
        await e.delete()

async def handle_status_command(e):
    cmds = e.text.split(" ")
    if len(cmds) > 1:
        if cmds[1] == "all":
            await get_status(e,True)
        else:
            await get_status(e)
    else:
        await create_status_menu(e)

async def handle_u_status_command(e):
    await create_status_user_menu(e)
        
async def speed_handler(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await get_speed(e)

    
async def handle_test_command(e):
    pass
    


async def handle_settings_cb(e):
    if await is_admin(e.client,e.sender_id,e.chat_id):
        await handle_setting_callback(e)
    else:
        await e.answer("⚠️ 𝗪𝗔𝗥𝗡 ⚠️ 𝗗𝗼𝗻𝘁 𝗧𝗼𝘂𝗰𝗵 𝗔𝗱𝗺𝗶𝗻 𝗦𝗲𝘁𝘁𝗶𝗻𝗴𝘀.",alert=True)

async def handle_upcancel_cb(e):
    db = upload_db

    data = e.data.decode("UTF-8")
    torlog.info("Data is {}".format(data))
    data = data.split(" ")

    if str(e.sender_id) == data[3]:
        db.cancel_download(data[1],data[2])
        await e.answer("🔴𝗨𝗽𝗹𝗼𝗮𝗱 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗮𝗻𝗰𝗲𝗹𝗲𝗱❌;)",alert=True)
    elif e.sender_id in get_val("ALD_USR"):
        db.cancel_download(data[1],data[2])
        await e.answer("🔴𝗨𝗽𝗹𝗼𝗮𝗱 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗮𝗻𝗰𝗲𝗹𝗲𝗱 𝗜𝗡 𝗔𝗗𝗠𝗜𝗡 𝗠𝗢𝗗𝗘❌ ;)",alert=True)
    else:
        await e.answer("𝗖𝗮𝗻'𝘁 𝗖𝗮𝗻𝗰𝗲𝗹 𝗼𝘁𝗵𝗲𝗿𝘀 𝘂𝗽𝗹𝗼𝗮𝗱 😡",alert=True)


async def callback_handler_canc(e):
    # TODO the msg can be deleted
    #mes = await e.get_message()
    #mes = await mes.get_reply_message()
    

    torlog.debug(f"Here the sender _id is {e.sender_id}")
    torlog.debug("here is the allower users list {} {}".format(get_val("ALD_USR"),type(get_val("ALD_USR"))))

    data = e.data.decode("utf-8").split(" ")
    torlog.debug("data is {}".format(data))

    is_aria = False
    is_mega = False

    if data[1] == "aria2":
        is_aria = True
        data.remove("aria2")
    
    if data[1] == "megadl":
        is_mega = True
        data.remove("megadl")
    

    if data[2] == str(e.sender_id):
        hashid = data[1]
        hashid = hashid.strip("'")
        torlog.info(f"Hashid :- {hashid}")

        await cancel_torrent(hashid, is_aria, is_mega)
        await e.answer("🔴𝗟𝗲𝗲𝗰𝗵 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗮𝗻𝗰𝗲𝗹𝗲𝗱❌ ;)",alert=True)
    elif e.sender_id in get_val("ALD_USR"):
        hashid = data[1]
        hashid = hashid.strip("'")
        
        torlog.info(f"Hashid :- {hashid}")
        
        await cancel_torrent(hashid, is_aria, is_mega)
        await e.answer("🔴𝗟𝗲𝗲𝗰𝗵 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝗰𝗮𝗻𝗰𝗲𝗹𝗲𝗱 𝗶𝗻 𝗔𝗗𝗠𝗜𝗡 𝗠𝗢𝗗𝗘 𝗫𝗗❌ ;)",alert=True)
    else:
        await e.answer("𝗖𝗮𝗻'𝘁 𝗖𝗮𝗻𝗰𝗲𝗹 𝗼𝘁𝗵𝗲𝗿𝘀 𝗹𝗲𝗲𝗰𝗵 😡", alert=True)


async def handle_exec_message_f(e):
    if get_val("REST11"):
        return
    message = e
    client = e.client
    if await is_admin(client, message.sender_id, message.chat_id, force_owner=True):
        PROCESS_RUN_TIME = 100
        cmd = message.text.split(" ", maxsplit=1)[1]

        reply_to_id = message.id
        if message.is_reply:
            reply_to_id = message.reply_to_msg_id

        process = await aio.create_subprocess_shell(
            cmd,
            stdout=aio.subprocess.PIPE,
            stderr=aio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        e = stderr.decode()
        if not e:
            e = "No Error"
        o = stdout.decode()
        if not o:
            o = "No Output"
        else:
            _o = o.split("\n")
            o = "`\n".join(_o)
        OUTPUT = f"**QUERY:**\n__Command:__\n`{cmd}` \n__PID:__\n`{process.pid}`\n\n**stderr:** \n`{e}`\n**Output:**\n{o}"

        if len(OUTPUT) > 3900:
            with open("exec.text", "w+", encoding="utf8") as out_file:
                out_file.write(str(OUTPUT))
            await client.send_file(
                entity=message.chat_id,
                file="exec.text",
                caption=cmd,
                reply_to=reply_to_id
            )
            os.remove("exec.text")
            await message.delete()
        else:
            await message.reply(OUTPUT)
    else:
        await message.reply("𝗢𝗻𝗹𝘆 𝗳𝗼𝗿 𝗼𝘄𝗻𝗲𝗿")

async def handle_pincode_cb(e):
    data = e.data.decode("UTF-8")
    data = data.split(" ")
    
    if str(e.sender_id) == data[2]:
        db = tor_db
        passw = db.get_password(data[1])
        if isinstance(passw,bool):
            await e.answer("🔴𝗧𝗼𝗿𝗿𝗲𝗻𝘁 𝗲𝘅𝗽𝗶𝗿𝗲𝗱...𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝘁𝗮𝗿𝘁𝗲𝗱 𝗻𝗼𝘄.")
        else:
            await e.answer(f"🔐𝗬𝗼𝘂𝗿 𝗣𝗶𝗻𝗰𝗼𝗱𝗲 𝗶𝘀 {passw}",alert=True)

        
    else:
        await e.answer("😂𝗜𝘁'𝘀 𝗻𝗼𝘁 𝘆𝗼𝘂𝗿 𝘁𝗼𝗿𝗿𝗲𝗻𝘁.",alert=True)

async def upload_document_f(message):
    if get_val("REST11"):
        return
    imsegd = await message.reply(
        "𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗶𝗻𝗴 ..."
    )
    imsegd = await message.client.get_messages(message.chat_id,ids=imsegd.id)
    if await is_admin(message.client, message.sender_id, message.chat_id, force_owner=True):
        if " " in message.text:
            recvd_command, local_file_name = message.text.split(" ", 1)
            recvd_response = await upload_a_file(
                local_file_name,
                imsegd,
                False,
                upload_db
            )
            #torlog.info(recvd_response)
    else:
        await message.reply("𝗢𝗻𝗹𝘆 𝗳𝗼𝗿 𝗼𝘄𝗻𝗲𝗿")
    await imsegd.delete()

async def get_logs_f(e):
    if await is_admin(e.client,e.sender_id,e.chat_id, force_owner=True):
        e.text += " torlog.txt"
        await upload_document_f(e)
    else:
        await e.delete()

async def set_password_zip(message):
    #/setpass message_id password
    data = message.raw_text.split(" ")
    passdata = message.client.dl_passwords.get(int(data[1]))
    if passdata is None:
        await message.reply(f"🔴𝗡𝗼 𝗲𝗻𝘁𝗿𝘆 𝗳𝗼𝘂𝗻𝗱 𝗳𝗼𝗿 𝘁𝗵𝗶𝘀 𝗷𝗼𝗯 𝗶𝗱 {data[1]}")
    else:
        print(message.sender_id)
        print(passdata[0])
        if str(message.sender_id) == passdata[0]:
            message.client.dl_passwords[int(data[1])][1] = data[2]
            await message.reply(f"✅𝗣𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝘂𝗽𝗱𝗮𝘁𝗲𝗱 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆.")
        else:
            await message.reply(f"❌𝗖𝗮𝗻𝗻𝗼𝘁 𝘂𝗽𝗱𝗮𝘁𝗲 𝘁𝗵𝗲 𝗽𝗮𝘀𝘀𝘄𝗼𝗿𝗱 𝘁𝗵𝗶𝘀 𝗶𝘀 𝗻𝗼𝘁 𝘆𝗼𝘂𝗿 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱.")

async def start_handler(event):
    msg = "<b>Hello This is TorToolkitX running on heroku an instance of <a href='https://github.com/XcodersHub/TorToolkitX'>This Repo</a>. Try the repo for yourself and dont forget to put a STAR and fork.</b>"
    await event.reply(msg, parse_mode="html")

def progress_bar(percentage):
    """Returns a progress bar for download
    """
    #percentage is on the scale of 0-1
    comp = get_val("COMPLETED_STR")
    ncomp = get_val("REMAINING_STR")
    pr = ""

    if isinstance(percentage, str):
        return "NaN"

    try:
        percentage=int(percentage)
    except:
        percentage = 0

    for i in range(1,11):
        if i <= int(percentage/10):
            pr += comp
        else:
            pr += ncomp
    return pr

async def handle_server_command(message):
    print(type(message))
    if isinstance(message, events.CallbackQuery.Event):
        callbk = True
    else:
        callbk = False

    try:
        # Memory
        mem = psutil.virtual_memory()
        memavailable = Human_Format.human_readable_bytes(mem.available)
        memtotal = Human_Format.human_readable_bytes(mem.total)
        mempercent = mem.percent
        memfree = Human_Format.human_readable_bytes(mem.free)
    except:
        memavailable = "N/A"
        memtotal = "N/A"
        mempercent = "N/A"
        memfree = "N/A"

    try:
        # Frequencies
        cpufreq = psutil.cpu_freq()
        freqcurrent = cpufreq.current
        freqmax = cpufreq.max
    except:
        freqcurrent = "N/A"
        freqmax = "N/A"

    try:
        # Cores
        cores = psutil.cpu_count(logical=False)
        lcores = psutil.cpu_count()
    except:
        cores = "N/A"
        lcores = "N/A"

    try:
        cpupercent = psutil.cpu_percent()
    except:
        cpupercent = "N/A"
    
    try:
        # Storage
        usage = shutil.disk_usage("/")
        totaldsk = Human_Format.human_readable_bytes(usage.total)
        useddsk = Human_Format.human_readable_bytes(usage.used)
        freedsk = Human_Format.human_readable_bytes(usage.free)
    except:
        totaldsk = "N/A"
        useddsk = "N/A"
        freedsk = "N/A"


    try:
        upb, dlb = await get_transfer()
        dlb = Human_Format.human_readable_bytes(dlb)
        upb = Human_Format.human_readable_bytes(upb)
    except:
        dlb = "N/A"
        upb = "N/A"

    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    if callbk:
        msg = (
            f"<b>╭─────────「 🤖 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗦 🤖 」\n"
            f"<b>│</b>\n"
            f"<b>├</b> ⏰𝗕𝗢𝗧 𝗨𝗣𝗧𝗜𝗠𝗘:- {diff}\n"
            f"<b>│</b>\n"
            f"<b>├</b> 🖥️𝗖𝗣𝗨 𝗦𝗧𝗔𝗧𝗦:-\n"
            f"<b>│</b> Cores: {cores} Logical: {lcores}\n"
            f"<b>│</b> CPU Frequency: {freqcurrent}  Mhz Max: {freqmax}\n"
            f"<b>│</b> CPU Utilization: {cpupercent}%\n"
            f"<b>│</b>\n"
            f"<b>├</b> 📀𝗦𝗧𝗢𝗥𝗔𝗚𝗘 𝗦𝗧𝗔𝗧𝗦:-\n"
            f"<b>│</b> Total: {totaldsk}\n"
            f"<b>│</b> Used: {useddsk}\n"
            f"<b>│</b> Free: {freedsk}\n"
            f"<b>│</b>\n"
            f"<b>├</b> 🎮𝗠𝗘𝗠𝗢𝗥𝗬 𝗦𝗧𝗔𝗧𝗦:-\n"
            f"<b>│</b> Available: {memavailable}\n"
            f"<b>│</b> Total: {memtotal}\n"
            f"<b>│</b> Usage: {mempercent}%\n"
            f"<b>│</b> Free: {memfree}\n"
            f"<b>│</b>\n"
            f"<b>├</b> ↕️𝗧𝗥𝗔𝗡𝗦𝗙𝗘𝗥 𝗜𝗡𝗙𝗢:-\n"
            f"<b>│</b> Download: {dlb}\n"
            f"<b>│</b> Upload: {upb}\n"
            f"<b>│</b>\n"
            f"<b>╰──────────「 TorToolKitX 」</b>\n"
        )
        await message.edit(msg, parse_mode="html", buttons=None)
    else:
        try:
            storage_percent = round((usage.used/usage.total)*100,2)
        except:
            storage_percent = 0

        
        msg = (
            f"<b>╭─────「 🤖 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗦 🤖 」\n"
            f"<b>│</b>\n"
            f"<b>├</b> ⏰𝗕𝗢𝗧 𝗨𝗣𝗧𝗜𝗠𝗘:- {diff}\n"
            f"<b>│</b>\n"
            f"<b>├</b> 🖥️𝗖𝗣𝗨 𝗨𝘁𝗶𝗹𝗶𝘇𝗮𝘁𝗶𝗼𝗻: {progress_bar(cpupercent)} - {cpupercent}%\n"
            f"<b>│</b>\n"
            f"<b>├</b> 💽𝗦𝘁𝗼𝗿𝗮𝗴𝗲 𝘂𝘀𝗲𝗱:- {progress_bar(storage_percent)} - {storage_percent}%\n"
            f"<b>│</b> Total: {totaldsk} Free: {freedsk}\n"
            f"<b>│</b>\n"
            f"<b>├</b> 🎮𝗠𝗲𝗺𝗼𝗿𝘆 𝘂𝘀𝗲𝗱:- {progress_bar(mempercent)} - {mempercent}%\n"
            f"<b>│</b> Total: {memtotal} Free: {memfree}\n"
            f"<b>│</b>\n"            
            f"<b>├</b> 🔽𝗧𝗿𝗮𝗻𝘀𝗳𝗲𝗿 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱:- {dlb}\n"
            f"<b>├</b> 🔼𝗧𝗿𝗮𝗻𝘀𝗳𝗲𝗿 𝗨𝗽𝗹𝗼𝗮𝗱:- {upb}\n"
            f"<b>│</b>\n"             
            f"<b>╰─────「 TorToolKitX 」</b>\n"            
        )
        await message.reply(msg, parse_mode="html", buttons=[[KeyboardButtonCallback("Get detailed stats.","fullserver")]])


async def about_me(message):
    db = var_db
    _, val1 = db.get_variable("RCLONE_CONFIG")
    if val1 is None:
        rclone_cfg = "❌𝗡𝗼 𝗥𝗰𝗹𝗼𝗻𝗲 𝗖𝗼𝗻𝗳𝗶𝗴 𝗶𝘀 𝗹𝗼𝗮𝗱𝗲𝗱."
    else:
        rclone_cfg = "✅𝗥𝗰𝗹𝗼𝗻𝗲 𝗖𝗼𝗻𝗳𝗶𝗴 𝗶𝘀 𝗹𝗼𝗮𝗱𝗲𝗱"

    val1  = get_val("RCLONE_ENABLED")
    if val1 is not None:
        if val1:
            rclone = "✅𝗥𝗰𝗹𝗼𝗻𝗲 𝗲𝗻𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻."
        else:
            rclone = "❌𝗥𝗰𝗹𝗼𝗻𝗲 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻."
    else:
        rclone = "N/A"

    val1  = get_val("LEECH_ENABLED")
    if val1 is not None:
        if val1:
            leen = "✅𝗟𝗲𝗲𝗰𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗲𝗻𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻."
        else:
            leen = "❌𝗟𝗲𝗲𝗰𝗵 𝗰𝗼𝗺𝗺𝗮𝗻𝗱 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱 𝗯𝘆 𝗮𝗱𝗺𝗶𝗻."
    else:
        leen = "N/A"


    diff = time.time() - uptime
    diff = Human_Format.human_readable_timedelta(diff)

    msg = (
        "<b>Name</b>: <code>TorToolkitX-Heroku</code>\n"
        f"<b>Version</b>: <code>{__version__}</code>\n"
        f"<b>Telethon Version</b>: {telever}\n"
        f"<b>Pyrogram Version</b>: {pyrover}\n"
        "<b>Modified By</b>: @XcodersHub\n\n"
        "<u>Currents Configs:-</u>\n\n"
        f"<b>Bot Uptime:-</b> {diff}\n"
        "<b>Torrent Download Engine:-</b> <code>qBittorrent [4.3.0 fix active]</code> \n"
        "<b>Direct Link Download Engine:-</b> <code>aria2</code> \n"
        "<b>Upload Engine:-</b> <code>RCLONE</code> \n"
        "<b>Youtube Download Engine:-</b> <code>youtube-dl</code>\n"
        f"<b>Rclone config:- </b> <code>{rclone_cfg}</code>\n"
        f"<b>Leech:- </b> <code>{leen}</code>\n"
        f"<b>Rclone:- </b> <code>{rclone}</code>\n"
        "\n"
        f"<b>Latest {__version__} Changelog :- </b>\n"
        "1.DB Optimizations.\n"
        "2.Database handling on disconnections..\n"
        "3.Support for ARM devices.\n"
        "4.Gdrive Support for PYTDL and YTDL\n"
        "5.Upload YT Playlist even when some vids are errored.\n"
        "6.Changed /server menu. Add /speedtest\n"
        "7.Minor fixes.\n"
        "8.Deploy takes less then 2 mins now.\n"
        "9.MegaDL added.\n"
        "10.Overall download and upload progress.\n"
        "11.Pixeldrain DL support.\n"
        "12.Alert on when the bot boots up.\n"
        "<b>13.Fixed Heroku Stuff.</b>\n"
    )

    await message.reply(msg,parse_mode="html")


async def set_thumb_cmd(e):
    thumb_msg = await e.get_reply_message()
    if thumb_msg is None:
        await e.reply("𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝗽𝗵𝗼𝘁𝗼 𝗼𝗿 𝗽𝗵𝗼𝘁𝗼 𝗮𝘀 𝗮 𝗱𝗼𝗰𝘂𝗺𝗲𝗻𝘁.")
        return
    
    if thumb_msg.document is not None or thumb_msg.photo is not None:
        value = await thumb_msg.download_media()
    else:
        await e.reply("𝗥𝗲𝗽𝗹𝘆 𝘁𝗼 𝗮 𝗽𝗵𝗼𝘁𝗼 𝗼𝗿 𝗽𝗵𝗼𝘁𝗼 𝗮𝘀 𝗮 𝗱𝗼𝗰𝘂𝗺𝗲𝗻𝘁.")
        return

    try:
        im = Image.open(value)
        im.convert("RGB").save(value,"JPEG")
        im = Image.open(value)
        im.thumbnail((320,320), Image.ANTIALIAS)
        im.save(value,"JPEG")
        with open(value,"rb") as fi:
            data = fi.read()
            user_db.set_thumbnail(data, e.sender_id)
        os.remove(value)
    except Exception:
        torlog.exception("Set Thumb")
        await e.reply("🔴𝗘𝗿𝗿𝗼𝗿 𝗶𝗻 𝘀𝗲𝘁𝘁𝗶𝗻𝗴 𝘁𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹.")
        return
    
    try:
        os.remove(value)
    except:pass

    user_db.set_var("DISABLE_THUMBNAIL",False, str(e.sender_id))
    await e.reply("✅𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝘀𝗲𝘁. 𝘁𝗿𝘆 𝘂𝘀𝗶𝗻𝗴 /usettings 𝘁𝗼 𝗴𝗲𝘁 𝗺𝗼𝗿𝗲 𝗰𝗼𝗻𝘁𝗿𝗼𝗹. 𝗖𝗮𝗻 𝗯𝗲 𝘂𝘀𝗲𝗱 𝗶𝗻 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝘁𝗼𝗼.")

async def clear_thumb_cmd(e):
    user_db.set_var("DISABLE_THUMBNAIL",True, str(e.sender_id))
    await e.reply("❌𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹 𝗱𝗶𝘀𝗮𝗯𝗹𝗲𝗱. 𝗧𝗿𝘆 𝘂𝘀𝗶𝗻𝗴 /usettings 𝘁𝗼 𝗴𝗲𝘁 𝗺𝗼𝗿𝗲 𝗰𝗼𝗻𝘁𝗿𝗼𝗹. 𝗖𝗮𝗻 𝗯𝗲 𝘂𝘀𝗲𝗱 𝗶𝗻 𝗽𝗿𝗶𝘃𝗮𝘁𝗲 𝘁𝗼𝗼.")

async def handle_user_settings_(message):
    if not message.sender_id in get_val("ALD_USR"):
        if not get_val("USETTINGS_IN_PRIVATE") and message.is_private:
            return

    await handle_user_settings(message)

def term_handler(signum, frame, client):
    torlog.info("TERM RECEIVED")
    async def term_async():
        omess = None
        st = Status().Tasks
        msg = "Bot Rebooting Re Add your Tasks\n\n"
        for i in st:
            if not await i.is_active():
                continue

            omess = await i.get_original_message()
            if str(omess.chat_id).startswith("-100"):
                chat_id = str(omess.chat_id)[4:]
                chat_id = int(chat_id)
            else:
                chat_id = omess.chat_id
            
            sender = await i.get_sender_id()
            msg += f"<a href='tg://user?id={sender}'>REBOOT</a> - <a href='https://t.me/c/{chat_id}/{omess.id}'>Task</a>\n"
        
        if omess is not None:
            await omess.respond(msg, parse_mode="html")
        exit(0)

    client.loop.run_until_complete(term_async())

async def booted(client):
    chats = get_val("ALD_USR")
    for i in chats:
        try:
            await client.send_message(i, "𝗧𝗵𝗲 𝗯𝗼𝘁 𝗶𝘀 𝗯𝗼𝗼𝘁𝗲𝗱 𝗮𝗻𝗱 𝗶𝘀 𝗿𝗲𝗮𝗱𝘆 𝘁𝗼 𝘂𝘀𝗲.")
        except Exception as e:
            torlog.info(f"Not found the entity {i}")
def command_process(command):
    return re.compile(command,re.IGNORECASE)
