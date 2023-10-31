import asyncio

import pyrogram
from pyrogram import Client

from database import actions, on_startup_database
from utils import logger

app = Client(name='session',
             api_id=6,
             api_hash='eb06d4abfb49dc3eeb1aeb98ae0f581e')


@app.on_message(filters=pyrogram.filters.me & pyrogram.filters.text & pyrogram.filters.command(commands=['add_bind',
                                                                                                         'new_bind',
                                                                                                         'create_bind'],
                                                                                               prefixes=['/', '.']))
async def add_new_bind(client: pyrogram.client.Client,
                       message: pyrogram.types.messages_and_media.message.Message) -> None:
    bind_command: str = message.command[1][1:] if message.command[1][0] in ['.', '/'] else message.command[1]
    bind_text: str = ' '.join(message.command[2:])

    if await actions.is_bind_exists(bind_command=bind_command):
        await message.reply(text=f'Bind <code>{bind_command}</code> already exists!',
                            parse_mode=pyrogram.enums.ParseMode.HTML)
        return

    await actions.add_bind(bind_command=bind_command,
                           bind_text=bind_text)

    await message.reply(text=f'Bind <code>{bind_command}</code> successfully added!',
                        parse_mode=pyrogram.enums.ParseMode.HTML)


@app.on_message(filters=pyrogram.filters.me & pyrogram.filters.text & pyrogram.filters.command(commands=['remove_bind',
                                                                                                         'delete_bind'],
                                                                                               prefixes=['/', '.']))
async def remove_bind(client: pyrogram.client.Client,
                      message: pyrogram.types.messages_and_media.message.Message) -> None:
    bind_command: str = message.command[1][1:] if message.command[1][0] in ['.', '/'] else message.command[1]

    await actions.delete_bind_by_command(bind_command=bind_command)

    await message.reply(text=f'Bind <code>{bind_command}</code> successfully removed!',
                        parse_mode=pyrogram.enums.ParseMode.HTML)


@app.on_message(filters=pyrogram.filters.me & pyrogram.filters.text & pyrogram.filters.command(commands=['clear_binds',
                                                                                                         'delete_binds',
                                                                                                         'remove_binds'],
                                                                                               prefixes=['/', '.']))
async def clear_binds(client: pyrogram.client.Client,
                      message: pyrogram.types.messages_and_media.message.Message) -> None:
    await actions.clear_binds()

    await message.reply(text='All binds successfully removed!',
                        parse_mode=pyrogram.enums.ParseMode.HTML)


@app.on_message(filters=pyrogram.filters.me & pyrogram.filters.text)
async def check_bind(client: pyrogram.client.Client,
                     message: pyrogram.types.messages_and_media.message.Message) -> None:
    if message.text.lower()[1:] in await actions.get_bind_commands_list():
        bind_text: str | None = await actions.get_bind_text_by_command(bind_command=message.text.lower()[1:])

        if not bind_text:
            return

        await message.edit_text(text=bind_text,
                                parse_mode=pyrogram.enums.ParseMode.HTML)


if __name__ == '__main__':
    logger.info('Bot successfully started!')
    asyncio.new_event_loop().run_until_complete(on_startup_database())
    app.run()
