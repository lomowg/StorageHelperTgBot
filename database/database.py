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
            id SERIAL PRIMARY KEY,
            username VARCHAR(100)
        )
    ''')

    await conn.close()
