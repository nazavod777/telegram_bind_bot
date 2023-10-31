import aiosqlite


async def on_startup_database() -> None:
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='binds'"
        )
        table_exists = await cursor.fetchone()

        if not table_exists:
            await cursor.execute(
                """
                CREATE TABLE binds (
                    id INTEGER PRIMARY KEY,
                    bind_command TEXT,
                    bind_text TEXT
                )
                """
            )
            await db.commit()

        else:
            await cursor.execute("PRAGMA table_info(binds)")
            columns = await cursor.fetchall()
            column_names = [column[1] for column in columns]

            if "bind_command" not in column_names:
                await cursor.execute("ALTER TABLE binds ADD COLUMN bind_command TEXT")

            if "bind_text" not in column_names:
                await cursor.execute("ALTER TABLE binds ADD COLUMN bind_text TEXT")

            await db.commit()


async def insert_data(bind_command, bind_text):
    async with aiosqlite.connect('database/binds.db') as db:
        cursor = await db.cursor()

        await cursor.execute(sql="INSERT INTO binds (bind_command, bind_text) VALUES (?, ?)",
                             parameters=(bind_command, bind_text))
        await db.commit()
