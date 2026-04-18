from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ChatJoinRequestHandler,
    ChatMemberHandler,
    CallbackQueryHandler,
)
import json
import os

BOT_TOKEN = "8755984464:AAEfaVJVdvA7kr0z3qkhaqX8i2zjxKa59WM"
BOT_USERNAME = "XD_REQACCEPTER_BOT"

DATA_FILE = "channels.json"


# ================= FILE HELPERS =================
def load_channels():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_channels(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ================= START =================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton(
                "➕ Add to Channel",
                url="https://t.me/XD_REQACCEPTER_BOT?startchannel=true&admin=invite_users+manage_chat+manage_messages"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 Add to Group",
                url="https://t.me/XD_REQACCEPTER_BOT?startgroup=true&admin=invite_users+manage_chat+manage_messages"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
f"""𝘼𝙙𝙙 @XD_REQACCEPTER_BOT 𝙏𝙤 𝙔𝙤𝙪𝙧 𝘾𝙝𝙖𝙣𝙣𝙚𝙡𝙨 𝙏𝙤 𝘼𝙘𝙘𝙚𝙥𝙩 𝙅𝙤𝙞𝙣 𝙍𝙚𝙦𝙪𝙚𝙨𝙩𝙨 𝘼𝙪𝙩𝙤𝙢𝙖𝙩𝙞𝙘𝙖𝙡𝙡𝙮 ⚡

𝙎𝙝𝙖𝙧𝙚 𝘼𝙣𝙙 𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙐𝙨 🤍""",
        reply_markup=reply_markup
    )


# ================= TRACK CHANNELS / GROUPS =================
async def track_bot_added(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if not update.my_chat_member:
            return

        chat = update.my_chat_member.chat
        new_status = update.my_chat_member.new_chat_member.status

        if new_status in ["administrator", "member"]:
            data = load_channels()
            data[str(chat.id)] = {
                "title": chat.title or "Unknown Chat",
                "type": chat.type,
            }
            save_channels(data)
            print(f"Saved chat: {chat.title} ({chat.id})")

        elif new_status in ["left", "kicked"]:
            data = load_channels()
            if str(chat.id) in data:
                del data[str(chat.id)]
                save_channels(data)
                print(f"Removed chat: {chat.id}")

    except Exception as e:
        print("Track error:", e)


# ================= CHANNEL LIST =================
async def channellist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_channels()

    if not data:
        await update.message.reply_text("❌ No private channels/groups saved yet.")
        return

    await update.message.reply_text("📋 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗟𝗶𝘀𝘁:")

    for chat_id, info in data.items():
        title = info.get("title", "Unknown Chat")

        keyboard = [
            [
                InlineKeyboardButton("🔗 Link", callback_data=f"getlink_{chat_id}"),
                InlineKeyboardButton("❌ Remove", callback_data=f"remove_{chat_id}")
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"📌 {title}",
            reply_markup=reply_markup
        )


# ================= LINK BUTTON =================
async def get_channel_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        chat_id = query.data.split("_", 1)[1]

        invite = await context.bot.create_chat_invite_link(chat_id=chat_id)

        await query.message.reply_text(
            f"🔗 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 𝗟𝗶𝗻𝗸:\n{invite.invite_link}"
        )

    except Exception as e:
        await query.message.reply_text(
            f"❌ Link create failed.\n\nMake sure bot has Invite Users via Link permission.\n\nError: {e}"
        )


# ================= REMOVE BUTTON =================
async def remove_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        chat_id = query.data.split("_", 1)[1]

        data = load_channels()

        if chat_id in data:
            title = data[chat_id]["title"]
            del data[chat_id]
            save_channels(data)

            await query.message.reply_text(f"❌ Removed: {title}")
        else:
            await query.message.reply_text("❌ Channel not found.")

    except Exception as e:
        await query.message.reply_text(f"Error: {e}")


# ================= AUTO ACCEPT =================
async def auto_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.chat_join_request.from_user
    chat = update.chat_join_request.chat

    await context.bot.approve_chat_join_request(chat.id, user.id)

    try:
        await context.bot.send_message(
            user.id,
f"""𝐖𝐄𝐋𝐂𝐎𝐌𝐄 𝐓𝐎 {chat.title}

◆━━━━━━━━━━━━━━━━━━━━━◆
🤖 𝗧𝗵𝗶𝘀 𝗯𝗼𝘁 𝗰𝗮𝗻 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗰𝗮𝗹𝗹𝘆 𝗮𝗽𝗽𝗿𝗼𝘃𝗲 𝗷𝗼𝗶𝗻 𝗿𝗲𝗾𝘂𝗲𝘀𝘁𝘀 🚀
◆━━━━━━━━━━━━━━━━━━━━━◆

𝙅𝙤𝙞𝙣 𝐃𝐄𝐒𝐇𝐈 𝐋𝐈𝐍𝐊 𝐄𝐗𝐏𝐎𝐒𝐄𝐃 ⬇️
https://t.me/+MnNqVwc5UhthMzZl
https://t.me/+MnNqVwc5UhthMzZl"""
        )
    except:
        pass


# ================= MAIN =================
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("channellist", channellist))
app.add_handler(ChatJoinRequestHandler(auto_accept))
app.add_handler(ChatMemberHandler(track_bot_added, ChatMemberHandler.MY_CHAT_MEMBER))
app.add_handler(CallbackQueryHandler(get_channel_link, pattern=r"^getlink_"))
app.add_handler(CallbackQueryHandler(remove_channel, pattern=r"^remove_"))

print("Bot Running...")
app.run_polling()