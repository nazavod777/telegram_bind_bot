import aiosqlite


async def get_bind_commands_list() -> list:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute("SELECT bind_command FROM binds")
        rows = await cursor.fetchall()

        bind_commands_values: list = [row[0] for row in rows]

        return bind_commands_values


async def get_bind_text_by_command(bind_command: str) -> str | None:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute("SELECT bind_text FROM binds WHERE bind_command = ?", (bind_command,))
        row = await cursor.fetchone()

        return row[0].replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r') if row else None


async def add_bind(bind_command: str,
                   bind_text: str) -> None:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute(sql="INSERT INTO binds (bind_command, bind_text) VALUES (?, ?)",
                             parameters=(bind_command,
                                         bind_text))
        await db.commit()


async def delete_bind_by_command(bind_command: str) -> None:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute("DELETE FROM binds WHERE bind_command = ?", (bind_command,))
        await db.commit()


async def clear_binds() -> None:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute("DELETE FROM binds")
        await db.commit()


async def is_bind_exists(bind_command: str) -> bool:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute("SELECT COUNT(*) FROM binds WHERE bind_command = ?", (bind_command,))
        count = await cursor.fetchone()

        return count[0] > 0
