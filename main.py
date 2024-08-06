from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config

Telegram = Client(
    "DC Tracker Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

@Telegram.on_message(filters.private & filters.command(["start"]))
async def start(bot, message):
    text = START_TEXT.format(message.from_user.dc_id)
    await message.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=START_BUTTON,
        quote=True
    )

@Telegram.on_message(filters.private & filters.command(["help"]))
async def help_command(bot, message):
    help_text = "Here are the commands you can use:\n\n"
    help_text += "/start - Get your Telegram DC ID\n"
    help_text += "/info - Get more information about your account\n"
    help_text += "/user_info [user_id] - Get information about another user\n"
    help_text += "/get_info - Get details about a forwarded message\n"
    help_text += "/about - Learn more about this bot\n"
    await message.reply_text(help_text, quote=True)

@Telegram.on_message(filters.private & filters.command(["info"]))
async def info_command(bot, message):
    user = message.from_user
    
    # Basic information
    user_info = f"🆔 **Telegram ID**: `{user.id}`\n"
    user_info += f"🗂 **DC ID**: `{user.dc_id}`\n"
    user_info += f"📝 **Username**: `@{user.username}`\n" if user.username else "📝 **Username**: `None`\n"
    user_info += f"🔍 **First Name**: `{user.first_name}`\n"
    user_info += f"🔎 **Last Name**: `{user.last_name}`\n" if user.last_name else ""
    
    # Account creation date
    account_creation_date = datetime.fromtimestamp(user.date)
    user_info += f"📅 **Account Creation Date**: `{account_creation_date.strftime('%Y-%m-%d')}`\n"
    
    # Calculate account age
    account_age_years = (datetime.now() - account_creation_date).days // 365
    user_info += f"⏳ **Account Age**: `{account_age_years}` years\n"
    
    # Language code
    if user.language_code:
        user_info += f"🌐 **Language Code**: `{user.language_code}`\n"
    
    # Fetch and count profile pictures
    photos = await bot.get_profile_photos(user.id)
    if photos.total_count > 0:
        profile_photo = await bot.download_media(photos.photos[0].file_id)
        user_info += f"🖼 **Profile Pictures Count**: `{photos.total_count}`\n"
        await message.reply_photo(profile_photo, caption=user_info)
    else:
        user_info += "🖼 **Profile Picture**: `No profile picture`\n"
        await message.reply_text(user_info, quote=True)
    
    # Fetch old usernames (if available)
    recent_updates = await bot.get_chat_event_log(message.chat.id, user_id=user.id, limit=10)
    if recent_updates:
        old_usernames = [update.old_username for update in recent_updates if update.old_username]
        if old_usernames:
            user_info += "\n🕑 **Old Usernames:**\n" + "\n".join(f" - `{uname}`" for uname in old_usernames)
    
    # Send user information
    await message.reply_text(user_info, quote=True)

@Telegram.on_message(filters.private & filters.command(["user_info"]))
async def user_info_command(bot, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Please provide a user ID. Usage: `/user_info [user_id]`", quote=True)
        return

    user_id = args[1]
    
    try:
        user = await bot.get_users(user_id)
    except Exception as e:
        await message.reply_text(f"Failed to retrieve user information: {str(e)}", quote=True)
        return
    
    # Basic information
    user_info = f"🆔 **Telegram ID**: `{user.id}`\n"
    user_info += f"🗂 **DC ID**: `{user.dc_id}`\n"
    user_info += f"📝 **Username**: `@{user.username}`\n" if user.username else "📝 **Username**: `None`\n"
    user_info += f"🔍 **First Name**: `{user.first_name}`\n"
    user_info += f"🔎 **Last Name**: `{user.last_name}`\n" if user.last_name else ""
    
    # Account creation date
    account_creation_date = datetime.fromtimestamp(user.date)
    user_info += f"📅 **Account Creation Date**: `{account_creation_date.strftime('%Y-%m-%d')}`\n"
    
    # Calculate account age
    account_age_years = (datetime.now() - account_creation_date).days // 365
    user_info += f"⏳ **Account Age**: `{account_age_years}` years\n"
    
    # Language code
    if user.language_code:
        user_info += f"🌐 **Language Code**: `{user.language_code}`\n"
    
    # Fetch and count profile pictures
    photos = await bot.get_profile_photos(user.id)
    if photos.total_count > 0:
        profile_photo = await bot.download_media(photos.photos[0].file_id)
        user_info += f"🖼 **Profile Pictures Count**: `{photos.total_count}`\n"
        await message.reply_photo(profile_photo, caption=user_info)
    else:
        user_info += "🖼 **Profile Picture**: `No profile picture`\n"
        await message.reply_text(user_info, quote=True)
    
    # Fetch old usernames (if available)
    recent_updates = await bot.get_chat_event_log(message.chat.id, user_id=user.id, limit=10)
    if recent_updates:
        old_usernames = [update.old_username for update in recent_updates if update.old_username]
        if old_usernames:
            user_info += "\n🕑 **Old Usernames:**\n" + "\n".join(f" - `{uname}`" for uname in old_usernames)
    
    # Send user information
    await message.reply_text(user_info, quote=True)

@Telegram.on_message(filters.private & filters.command(["get_info"]))
async def get_info_command(bot, message):
    if not message.forward_from:
        await message.reply_text("This command must be used in response to a forwarded message.", quote=True)
        return

    forwarded_message = message.reply_to_message
    
    if forwarded_message:
        info = f"🔗 **Forwarded Message Details**:\n\n"
        info += f"📜 **Message ID**: `{forwarded_message.message_id}`\n"
        info += f"📅 **Date**: `{forwarded_message.date.strftime('%Y-%m-%d %H:%M:%S')}`\n"
        info += f"✉️ **From**: `{forwarded_message.from_user.id}` - `@{forwarded_message.from_user.username}`\n" if forwarded_message.from_user else "✉️ **From**: `Unknown`\n"
        info += f"📤 **Forwarded From**: `{forwarded_message.forward_from.id}` - `@{forwarded_message.forward_from.username}`\n" if forwarded_message.forward_from else "📤 **Forwarded From**: `Unknown`\n"
        info += f"📝 **Text**: `{forwarded_message.text}`\n" if forwarded_message.text else "📝 **Text**: `No text`\n"
        
        if forwarded_message.photo:
            photo = await bot.download_media(forwarded_message.photo.file_id)
            info += f"📷 **Contains Photo**\n"
            await message.reply_photo(photo, caption=info)
        else:
            info += "📷 **Contains Photo**: `No`\n"
            await message.reply_text(info, quote=True)
    else:
        await message.reply_text("Failed to retrieve information about the forwarded message.", quote=True)

@Telegram.on_message(filters.private & filters.command(["about"]))
async def about_command(bot, message):
    about_text = "This bot provides detailed information about your Telegram account, others, and forwarded messages.\n"
    about_text += "It was built using Pyrogram and Python."
    await message.reply_text(about_text, quote=True)

START_TEXT = """🎸 Your Telegram DC Is : `{}`

The DC ID represents the data center that stores your data on Telegram's servers. It's a unique identifier that helps in understanding where your data is stored.
"""
START_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('♻️ Updates Channel ♻️', url=f"https://telegram.me/{Config.UPDATE_CHANNEL}"),
            InlineKeyboardButton('❓ Help ❓', callback_data="help")
        ]
    ]
)

@Telegram.on_callback_query(filters.regex("help"))
async def on_help_callback(bot, update):
    await help_command(bot, update.message)

Telegram.run()
