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

    command = \
        """
            INSERT INTO "settings" (user_id, forward_info, keep_history)
            VALUES ($1, $2, $3)
        """

    await connector.execute(command, user_id, True, False, execute=True)


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


async def get_user_all_folders(connector: DataBaseClass, user_id: int):
    command = \
        """
            SELECT folder_name FROM "folders"
            WHERE user_id = $1 AND folder_name != 'Избранное';
        """

    result = await connector.execute(command, user_id, fetch=True)

    return list(map(lambda x: str(x['folder_name']) + '_fldBtn', result))


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
                user_id BIGINT,
                username VARCHAR(100) NOT NULL
            );
        ''')

    await conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    user_id BIGINT,
                    forward_info BOOLEAN NOT NULL,
                    keep_history BOOLEAN NOT NULL
                );
            ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS folders (
                id SERIAL PRIMARY KEY,
                folder_name VARCHAR(100) NOT NULL,
                user_id BIGINT
            );
        ''')

    await conn.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                folder_id INT,
                message_type VARCHAR(50) NOT NULL,
                content TEXT[],
                caption TEXT,
                forward_info TEXT,
                file_id TEXT[]
            );
        ''')

    await conn.close()


async def delete_folder(connector: DataBaseClass, user_id: int, folder_name: str):
    command = """
        DELETE FROM "folders"
        WHERE user_id = $1 AND folder_name = $2;
    """
    await connector.execute(command, user_id, folder_name, execute=True)


async def get_user_folder_id(connector: DataBaseClass, user_id: int, folder_name: str):
    command = \
        """
            SELECT id FROM "folders"
            WHERE user_id = $1 AND folder_name = $2;
        """

    result = await connector.execute(command, user_id, folder_name, fetchrow=True)

    return result['id']


async def get_messages_from_folder(connector: DataBaseClass, folder_id: int):
    command = """
            SELECT message_type, content, caption, forward_info, file_id
            FROM messages
            WHERE folder_id = $1;
        """
    return await connector.execute(command, folder_id, fetch=True)


async def add_message(connector: DataBaseClass, folder_id: int, message_type: str, content: list[str], caption: str, forward_info: str, file_id: list[str]):
    command = """
            INSERT INTO messages (folder_id, message_type, content, caption, forward_info, file_id)
            VALUES ($1, $2, $3, $4, $5, $6);
        """

    await connector.execute(command, folder_id, message_type, content, caption, forward_info, file_id, execute=True)


async def delete_message(connector: DataBaseClass, folder_id: int, caption: str, file_id: list[str]):
    command = """
            DELETE FROM messages 
            WHERE id = (
                SELECT id FROM messages 
                WHERE folder_id = $1 AND (caption = $2 OR LEFT(forward_info || E'\n\n' || caption, 1024) = $2) AND (file_id = $3 OR forward_info = '' OR file_id @> $3 OR file_id IS NULL)
                LIMIT 1
            )
        """
    await connector.execute(command, folder_id, caption, file_id, execute=True)


async def update_forward_info(connector: DataBaseClass, user_id: int, forward_info: bool):
    command = \
        """
            UPDATE settings
            SET forward_info = $2
            WHERE user_id = $1
        """
    await connector.execute(command, user_id, forward_info, execute=True)


async def get_user_forward_info(connector: DataBaseClass, user_id: int):
    command = \
        """
            SELECT forward_info FROM "settings"
            WHERE user_id = $1;
        """

    result = await connector.execute(command, user_id, fetchrow=True)

    return result['forward_info']


async def update_keep_history(connector: DataBaseClass, user_id: int, keep_history: bool):
    command = \
        """
            UPDATE settings
            SET keep_history = $2
            WHERE user_id = $1
        """
    await connector.execute(command, user_id, keep_history, execute=True)


async def get_user_keep_history(connector: DataBaseClass, user_id: int):
    command = \
        """
            SELECT keep_history FROM "settings"
            WHERE user_id = $1;
        """

    result = await connector.execute(command, user_id, fetchrow=True)

    return result['keep_history']


async def rename_folder(connector: DataBaseClass, user_id: int, folder_id: int, new_folder_name: str):
    command = \
        """
            UPDATE folders
            SET folder_name = $3
            WHERE user_id = $1 AND id = $2
        """
    await connector.execute(command, user_id, folder_id, new_folder_name, execute=True)
