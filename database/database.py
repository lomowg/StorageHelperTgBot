import asyncpg
from .connection_pool import DataBaseClass


async def add_new_user(connector: DataBaseClass,
                       user_id: int,
                       username: str):
    command = \
        """
            INSERT INTO "users"
            VALUES($1, $2);
        """

    await connector.execute(command, user_id, username, execute=True)

    command = \
        """
            INSERT INTO "folders" (folder_name, user_id)
            VALUES ($1, $2)
        """

    await connector.execute(command, 'Избранное', user_id, execute=True)


async def add_new_folder(connector: DataBaseClass, user_id: int, folder_name: str):
    command = \
        """
            INSERT INTO "folders" (folder_name, user_id)
            VALUES ($1, $2)
        """

    await connector.execute(command, folder_name, user_id, execute=True)


async def get_user_folder(connector: DataBaseClass, user_id: int, folder_name: str):
    command = \
        """
            SELECT * FROM "folders"
            WHERE user_id = $1 AND folder_name = $2;
        """

    result = await connector.execute(command, user_id, folder_name, fetchrow=True)

    return result


async def get_user(connector: DataBaseClass, user_id: int):
    command = \
        """
            SELECT * FROM "users"
            WHERE user_id = $1;
        """

    result = await connector.execute(command, user_id, fetchrow=True)

    return result


async def create_tables(user, password, database, host):
    conn = await asyncpg.connect(user=user, password=password,
                                 database=database, host=host)

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT,
                username VARCHAR(100) NOT NULL
            );
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id SERIAL PRIMARY KEY,
                folder_name VARCHAR(100) NOT NULL,
                user_id INT
            );
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                folder_id INT,
                message_type VARCHAR(50) NOT NULL,
                content TEXT NOT NULL
            );
        ''')

    await conn.close()
