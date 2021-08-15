# (c) @AbirHasan2005
# I just made this for searching a channel message from inline.
# Maybe you can use this for something else.
# I first made this for @AHListBot ...
# Edit according to your use.

from configs import Config
from pyrogram import Client, filters, idle
from pyrogram.errors import QueryIdInvalid
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InlineQuery, InlineQueryResultArticle, \
    InputTextMessageContent

# Bot Client for Inline Search
Bot = Client(
    session_name=Config.BOT_SESSION_NAME,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)
# User Client for Searching in Channel.
User = Client(
    session_name=Config.USER_SESSION_STRING,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)


@Bot.on_message(filters.private & filters.command("start"))
async def start_handler(_, event: Message):
    await event.reply_text(
        "**Welcome to Pocket Fm Hub bot**\n\n"
        "Here You can search all the stories of pocket fm hub.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Group", url="https://t.me/pocketfmhubchat")],
            [InlineKeyboardButton("Join Channel", url="https://t.me/pocketfmhub")]
        ])
    )


@Bot.on_inline_query()
async def inline_handlers(_, event: InlineQuery):
    answers = list()
    # If Search Query is Empty
    if event.query == "":
        answers.append(
            InlineQueryResultArticle(
                title="Tutorial Video",
                description="If you are facing any problem on using this bot, Watch this Tutorial...",
                thumb_url="https://i.imgur.com/6jZsMYG.png",
                input_message_content=InputTextMessageContent(
                    message_text="Please watch this video if you are facing problem in opening links.",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Watch Tutorial", url="https://jmp.sh/q24v5ga")]
                ])
            )
        )
        answers.append(
            InlineQueryResultArticle(
                title="Support Channel & Group",
                description="Channel - @pocketfmhub\nGroup - @pocketfmhubchat",
                thumb_url="https://i.ibb.co/cNYJHYZ/IMG-20210815-144921.jpg",
                input_message_content=InputTextMessageContent(
                    message_text="Using this bot you can search all the available audiobooks of pocket Fm Hub without visiting main channel",
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Support Group", url="https://t.me/pocketfmhubchat"),
                     InlineKeyboardButton("Bots Channel", url="https://t.me/pocketfmhub")],
                    [InlineKeyboardButton("Search Here", switch_inline_query_current_chat="")]
                ])
            )
        )
    # Search Channel Message using Search Query Words
    else:
        async for message in User.search_messages(chat_id=Config.CHANNEL_ID, limit=50, query=event.query):
            if message.text:
                answers.append(InlineQueryResultArticle(
                    title="{}".format(message.text.split("\n", 1)[0]),
                    description="{}".format(message.text.rsplit("\n", 1)[-1]),
                    thumb_url="https://i.ibb.co/cNYJHYZ/IMG-20210815-144921.jpg",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")]]),
                    input_message_content=InputTextMessageContent(
                        message_text=message.text.markdown,
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                ))
    try:
        await event.answer(
            results=answers,
            cache_time=0
        )
        print(f"[{Config.BOT_SESSION_NAME}] - Answered Successfully - {event.from_user.first_name}")
    except QueryIdInvalid:
        print(f"[{Config.BOT_SESSION_NAME}] - Failed to Answer - {event.from_user.first_name}")

# Start Clients
Bot.start()
User.start()
# Loop Clients till Disconnects
idle()
# After Disconnects,
# Stop Clients
Bot.stop()
User.stop()
