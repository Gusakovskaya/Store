import psycopg2
import psycopg2.extras


async def exec_universal_select_query(db_table, where=None, sep=' AND ', one=False, conn=None):
    query = 'SELECT * FROM {}'.format(db_table)
    if where:
        query = '{} WHERE {}'.format(
            query,
            sep.join(['{}=%s'.format(key) for key in where.keys()])
        )
    async with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        if where:
            await cursor.execute(query, tuple(where.values()))
        else:
            await cursor.execute(query)

        if one:
            return await cursor.fetchone()
        else:
            return await cursor.fetchall()


async def exec_universal_insert_query(db_table, set, conn):
    query = 'INSERT INTO {db_table} ({fields}) VALUES ({values}) RETURNING *;'.format(
        db_table=db_table,
        fields=",".join(map(str, set.keys())).replace("'", ''),
        values=",".join('%s' for _ in range(len(set)))
    )

    async with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        await cursor.execute(query, tuple(set.values()))
        return await cursor.fetchone()


async def exec_universal_update_query(db_table, set, where, sep=' AND ', conn=None):
    if len(set) == 1:
        query = 'UPDATE {db_table} SET {set_keys} = {set_values} WHERE {where} RETURNING *;'.format(
            db_table=db_table,
            set_keys=list(set.keys())[0],
            set_values='%s',
            where=sep.join(['{}=%s'.format(key) for key in where.keys()])
        )
    else:
        query = 'UPDATE {db_table} SET ({set_keys}) = ({set_values}) WHERE {where} RETURNING *;'.format(
            db_table=db_table,
            set_keys=','.join(set.keys()),
            set_values=','.join('%s' for _ in range(len(set))),
            where=sep.join(['{}=%s'.format(key) for key in where.keys()])
        )

    async with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        await cursor.execute(query, tuple(set.values()) + tuple(where.values()))
        return await cursor.fetchone()


async def exec_universal_delete_query(db_table, where, sep=' AND ', conn=None):
    query = 'DELETE FROM {db_table} WHERE {where}'.format(
        db_table=db_table,
        where=sep.join(['{}=%s'.format(key) for key in where.keys()])
    )

    async with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        await cursor.execute(query, tuple(where.values()))
