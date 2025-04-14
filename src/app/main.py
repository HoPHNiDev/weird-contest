from pyrogram import Client, filters
from pyrogram.types import Message

from src.app.buttons import buttons
from src.app.crud import get_or_create_user, get_user_works_count
from src.app.messages import (
    welcome_text,
    max_work_sent,
    unknown_command,
    main_menu,
    terms_text,
    schedule_text,
    prizes_text,
    help_text,
)
from config import logger, settings, bot
from src.app.service import (
    new_work,
    reply_message,
)


@bot.on_message(filters.command(["start"]))
async def reply_start(client: Client, message: Message):
    """
    Reply to the start command.
    """
    async for session in settings.db_helper.session_dependency():
        user = await get_or_create_user(
            session=session,
            user=message.from_user,
        )

    await message.reply_text(
        welcome_text,
        reply_markup=buttons.main_menu,
    )


@bot.on_message(filters.command(["help"]))
async def reply_help(client: Client, message: Message):
    """
    Reply to the help command.
    """
    return await reply_message(client, message, help_text)


@bot.on_message()
async def handle_message(client: Client, message: Message):
    """
    Handle incoming messages.
    """
    logger.info(f"Received message: {message.text}")

    user_works_count = 0
    user = None
    async for session in settings.db_helper.session_dependency():
        user = await get_or_create_user(
            session=session,
            user=message.from_user,
        )
        user_works_count = await get_user_works_count(session=session, user=user)

    msg_text = message.text or message.caption
    is_text = msg_text and not message.media

    if is_text and "Условия конкурса" in msg_text:
        return await reply_message(client, message, terms_text)
    elif is_text and "Отправить работу" in msg_text:
        if user_works_count >= settings.MAX_ENTRIES_PER_USER:
            return await message.reply_text(max_work_sent)
        return await new_work(client, message, user)
    elif is_text and "Сроки проведения" in msg_text:
        return await reply_message(client, message, schedule_text)
    elif is_text and "Призы" in msg_text:
        return await reply_message(client, message, prizes_text)
    elif is_text and "Помощь" in msg_text:
        return await reply_message(client, message, help_text)
    elif is_text and buttons.cancel_text in msg_text:
        return await message.reply_text(
            text=main_menu,
            reply_markup=buttons.main_menu,
        )
    elif message.media and message.photo:
        if user_works_count >= settings.MAX_ENTRIES_PER_USER:
            return await message.reply_text(max_work_sent)
        return await new_work(client, message, user)
    else:
        await message.reply_text(unknown_command)


if __name__ == "__main__":
    logger.info(f"Running {__name__}")
    bot.run()
