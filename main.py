from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import Config  # Import your config

Telegram = Client(
    "DC Tracker Bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

@Telegram.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.dc_id)
    reply_markup = START_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )

@Telegram.on_message(filters.private & filters.command(["help"]))
async def help_command(bot, update):
    help_text = "Here are the commands you can use:\n\n"
    help_text += "/start - Get your Telegram DC ID\n"
    help_text += "/info - Get more information about you\n"
    help_text += "/about - Learn more about this bot\n"
    await update.reply_text(help_text, quote=True)

@Telegram.on_message(filters.private & filters.command(["info"]))
async def info_command(bot, update):
    user = update.from_user
    
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
        await update.reply_photo(profile_photo, caption=user_info)
    else:
        user_info += "🖼 **Profile Picture**: `No profile picture`\n"
        await update.reply_text(user_info, quote=True)
    
    # Fetch old usernames (if available)
    recent_updates = await bot.get_chat_event_log(update.chat.id, user_id=user.id, limit=10)
    if recent_updates:
        old_usernames = [update.old_username for update in recent_updates if update.old_username]
        if old_usernames:
            user_info += "\n🕑 **Old Usernames:**\n" + "\n".join(f" - `{uname}`" for uname in old_usernames)
    
    # Send user information
    await update.reply_text(user_info, quote=True)

@Telegram.on_message(filters.private & filters.command(["about"]))
async def about_command(bot, update):
    about_text = "This bot provides detailed information about your Telegram account.\n"
    about_text += "It was built using Pyrogram and Python."
    await update.reply_text(about_text, quote=True)

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
