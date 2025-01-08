import asyncio 
import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated, UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
import time
import os, sys
import json
from config import API_ID, API_HASH, ADMINS, DUMP
from database.db import database 
from TechVJ.strings import strings, HELP_TXT, BATCH_TXT


def get(obj, key, default=None):
    try:
        return obj[key]
    except:
        return default


async def downstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)
      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"📥 Downloading...\n\n{txt}")
            await asyncio.sleep(4)
        except:
            await asyncio.sleep(5)


# upload status
async def upstatus(client: Client, statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await client.edit_message_text(message.chat.id, message.id, f"📤 Uploading...\n\n{txt}")
            await asyncio.sleep(4)
        except:
            await asyncio.sleep(5)


# progress writer with speed calculation
def progress(current, total, message, type, start_time):
    # Calculate download/upload speed
    elapsed_time = time.time() - start_time
    speed = current / elapsed_time  # Bytes per second
    speed_str = f"{speed / 1024:.2f} KB/s" if speed < 1024 * 1024 else f"{speed / (1024 * 1024):.2f} MB/s"
    
    # Write current progress to file
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"⏳ Done: {current * 100 / total:.1f}%\n📶 Speed: {speed_str}\n📁 Size: {current / (1024 * 1024):.2f} MB / {total / (1024 * 1024):.2f} MB")


# start command
@Client.on_message(filters.command(["start"]))
async def send_start(client: Client, message: Message):
    buttons = [[
        InlineKeyboardButton("Developer", url = "tg://settings")
    ],[
        InlineKeyboardButton('🔞 ᴀᴅᴜʟᴛ ᴄʜᴀᴛ 💦', url='https://t.me/+EN7avEgX4ks5NGRl'),
        InlineKeyboardButton('💫 ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ', url='https://t.me/all_from_adult_verse')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    H = await client.send_message(message.chat.id, f"<b>👋 Hi {message.from_user.mention}, I am Slave Saver Bot, I can send you public channel's restricted contents.\n\nFor more info how to use bot press - /help</b>", reply_markup=reply_markup, reply_to_message_id=message.id)
    
    await asyncio.sleep(60)
    await H.delete()
    await message.delete()


# help command
@Client.on_message(filters.command(["help"]))
async def send_help(client: Client, message: Message):
   L = await client.send_message(message.chat.id, f"{HELP_TXT}")
       
   await asyncio.sleep(42)
   await L.delete()
   await message.delete()
  
@Client.on_message(filters.command(["batch"]))
async def send_batch(client: Client, message: Message):
   Y = await client.send_message(message.chat.id, f"{BATCH_TXT}")
    
   await asyncio.sleep(25)
   await Y.delete()
   await message.delete()

@Client.on_message(filters.command('restart') & filters.private)
async def restart_command(client: Client, message: Message):
    admins = [ADMINS] if isinstance(ADMINS, int) else ADMINS

    if message.from_user.id not in admins:
        R = await message.reply_text("Ohh Babe! Sorry But You Can't Restart Me 🙁")
        await asyncio.sleep(12)
        await message.delete()
        await R.delete()
        return

    await message.reply_text("🔄 Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    
@Client.on_message(filters.text & filters.private)
async def save(client: Client, message: Message):
    if "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single","").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID
        for msgid in range(fromID, toID+1):
            # private
            if "https://t.me/c/" in message.text:
                user_data = database.find_one({'chat_id': message.chat.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                chatid = int("-100" + datas[4])
                await handle_private(client, acc, message, chatid, msgid)
    
            # bot
            elif "https://t.me/b/" in message.text:
                user_data = database.find_one({"chat_id": message.chat.id})
                if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                    await client.send_message(message.chat.id, strings['need_login'])
                    return
                acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                await acc.connect()
                username = datas[4]
                try:
                    await handle_private(client, acc, message, username, msgid)
                except Exception as e:
                    await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            
            # public
            else:
                username = datas[3]

                try:
                    msg = await client.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    await client.send_message(message.chat.id, "The username is not occupied by anyone", reply_to_message_id=message.id)
                    return
    
                try:
        # Copy the message to the user
                    sent_msg = await client.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
        
        # Forward to Dump
                    await client.forward_messages(DUMP, sent_msg.chat.id, sent_msg.id)
                except:
                    try:    
                        user_data = database.find_one({"chat_id": message.chat.id})
                        if not get(user_data, 'logged_in', False) or user_data['session'] is None:
                            await client.send_message(message.chat.id, strings['need_login'])
                            return
                        acc = Client("saverestricted", session_string=user_data['session'], api_hash=API_HASH, api_id=API_ID)
                        await acc.connect()
            
            # Handle private messages
                        await handle_private(client, acc, message, username, msgid)
                    except Exception as e:
                        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

            # wait time
            await asyncio.sleep(3)

# handle private
async def handle_private(client: Client, acc, message: Message, chatid: int, msgid: int):
    msg: Message = await acc.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)
    chat = message.chat.id
    if "Text" == msg_type:
        try:
            sent_msg = await client.send_message(chat, msg.text, entities=msg.entities, reply_to_message_id=message.id)
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
            return

    smsg = await client.send_message(message.chat.id, '📥 Trying To Download', reply_to_message_id=message.id)
    dosta = asyncio.create_task(downstatus(client, f'{message.id}downstatus.txt', smsg))
    
    start_time = time.time()
    try:
        file = await acc.download_media(msg, progress=progress, progress_args=[message, "down", start_time])
        os.remove(f'{message.id}downstatus.txt')
        
    except Exception as e:
        await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)  
    
    upsta = asyncio.create_task(upstatus(client, f'{message.id}upstatus.txt', smsg))
    
    if msg.caption:
        caption = msg.caption
    else:
        caption = None
            
    if "Document" == msg_type:
        try:
            ph_path = await acc.download_media(msg.document.thumbs[0].file_id)
        except:
            ph_path = None

        start_time = time.time()
        try:
            sent_msg = await client.send_document(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        if ph_path is not None:
            os.remove(ph_path)
    
    elif "Video" == msg_type:
        try:
            ph_path = await acc.download_media(msg.video.thumbs[0].file_id)
        except:
            ph_path = None

        start_time = time.time()
        try:
            sent_msg = await client.send_video(chat, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)
        if ph_path is not None:
            os.remove(ph_path)

    elif "Photo" == msg_type:
        start_time = time.time()
        try:
            sent_msg = await client.send_photo(chat, file, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

    elif "Audio" == msg_type:
        try:
            ph_path = await acc.download_media(msg.audio.thumbs[0].file_id)
        except:
            ph_path = None

        start_time = time.time()
        try:
            sent_msg = await client.send_audio(chat, file, thumb=ph_path, caption=caption, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])   
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

        if ph_path is not None:
            os.remove(ph_path)

    elif "Animation" == msg_type:
        start_time = time.time()
        try:
            sent_msg = await client.send_animation(chat, file, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

    elif "Sticker" == msg_type:
        start_time = time.time()
        try:
            sent_msg = await client.send_sticker(chat, file, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

    elif "Voice" == msg_type:
        start_time = time.time()
        try:
            sent_msg = await client.send_voice(chat, file, caption=caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up", start_time])
            # Forward to Dump
            await client.forward_messages(DUMP, chat, sent_msg.id)
        except Exception as e:
            await client.send_message(message.chat.id, f"Error: {e}", reply_to_message_id=message.id)

    if os.path.exists(f'{message.id}upstatus.txt'): 
        os.remove(f'{message.id}upstatus.txt')
        os.remove(file)
    
    await client.delete_messages(message.chat.id, [smsg.id])


# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass

# Run the client
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH)

if __name__ == "__main__":
    app.run()
