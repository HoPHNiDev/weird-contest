from pyrogram import Client
from pyromod import Client as PyromodClient
from pyromod.exceptions import ListenerTimeout
from pyrogram.types import Message, ReplyParameters

from src.app.config import settings
from src.app.crud import create_work
from src.app.messages import (
    send_work_media,
    timeout_text,
    send_work_text,
    new_work_msg,
    success_work_msg,
    main_menu,
)
from src.app.buttons import buttons
from src.app.models import User


async def get_media(
    client: PyromodClient,
    message: Message,
):
    if message.media:
        return message.id

    send_media_message = await message.reply(
        text=send_work_media,
        reply_markup=buttons.cancel_button,
    )
    try:
        media_message = await client.listen(
            chat_id=message.chat.id,
            user_id=message.from_user.id,
            timeout=300,
        )

        if (
            media_message
            and media_message.text
            and buttons.cancel_text in media_message.text
        ):
            await message.reply(main_menu, reply_markup=buttons.main_menu)
            return None

        if (
            media_message.text
            and buttons.cancel_text not in media_message.text
            or media_message.caption
            and buttons.cancel_text not in media_message.caption
            or media_message.media
        ):
            await client.delete_messages(
                chat_id=send_media_message.chat.id,
                message_ids=send_media_message.id,
            )

            return media_message.id

    except ListenerTimeout:
        await message.reply(text=timeout_text, reply_markup=buttons.main_menu)
        await client.delete_messages(
            chat_id=send_media_message.chat.id,
            message_ids=send_media_message.id,
        )
        return None


async def get_media_description(client: PyromodClient, message: Message) -> str | None:
    if message.media and (message.text or message.caption):
        return message.text or message.caption

    require_description_message = await message.reply(
        text=send_work_text,
        reply_markup=buttons.cancel_button,
    )
    try:
        response = await client.listen(
            chat_id=message.chat.id, user_id=message.from_user.id, timeout=300
        )
    except ListenerTimeout:
        await message.reply(text=timeout_text, reply_markup=buttons.main_menu)
        await client.delete_messages(
            chat_id=require_description_message.chat.id,
            message_ids=require_description_message.id,
        )
        return None

    if response and response.text and buttons.cancel_text in response.text:
        await message.reply(main_menu, reply_markup=buttons.main_menu)
        return None
    return response.text


async def new_work(client: PyromodClient, message: Message, user: User) -> None:
    media_message_id = await get_media(client, message)
    if not media_message_id:
        return None
    media_description = await get_media_description(client, message)
    if not media_description:
        return None

    forwarded_images = await client.forward_messages(
        chat_id=settings.ADMIN_CHAT,
        from_chat_id=message.chat.id,
        message_ids=media_message_id,
    )

    async for session in settings.db_helper.session_dependency():
        work = await create_work(
            session=session, user=user, work_link=forwarded_images.link
        )

    new_work_message = new_work_msg(user=user, description=media_description, work=work)
    work_message = await client.send_message(
        chat_id=settings.ADMIN_CHAT,
        text=new_work_message,
        reply_parameters=ReplyParameters(message_id=forwarded_images.id),
    )
    if work_message:
        success_text = success_work_msg(work=work)
        await message.reply(
            text=success_text,
            reply_markup=buttons.main_menu,
        )


async def reply_message(client: Client, message: Message, text):
    await client.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_parameters=ReplyParameters(message_id=message.id),
    )
