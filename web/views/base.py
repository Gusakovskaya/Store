import sys
sys.path.insert(0, '../')

from aiohttp import web
from utils.service import service
from utils import db, settings


class BaseView:

    async def get_object(self, db_table, object_id):
        async with service.db_pool.acquire() as conn:
            return await db.exec_universal_select_query(
                db_table,
                where={
                    'id': object_id,
                },
                one = True,
                conn = conn
            )

    async def list_objects(self, db_table):
        async with service.db_pool.acquire() as conn:
            records = await db.exec_universal_select_query(
                db_table,
                conn=conn
            )
        objects = list(map(dict, records))
        return web.json_response(objects)

    async def retrieve_object(self, db_table, pk):
        async with service.db_pool.acquire() as conn:
            object = await db.exec_universal_select_query(
                db_table,
                where={
                    'id': pk,
                },
                one=True,
                conn=conn
            )
        if not object:
            return web.Response(text='Not found', status=404)
        else:
            return web.json_response(dict(object))

    async def create_object(self, db_table, data, validator):
        fail_reason = await validator(data)
        if fail_reason:
            return web.Response(text=fail_reason, status=400)
        async with service.db_pool.acquire() as conn:
            object = await db.exec_universal_insert_query(
                db_table,
                set=data,
                conn=conn
            )
        return web.json_response(dict(object))

    async def update_object(self, db_table, pk, data, validator):
        object = await self.get_object(db_table, pk)
        if not object:
            return web.Response(text='User not found')

        fail_reason = await validator(data)
        if fail_reason:
            return web.Response(text=fail_reason, status=400)

        async with service.db_pool.acquire() as conn:
            object = await db.exec_universal_update_query(
                settings.USER_DB_TABLE,
                set=data,
                where={
                    'id': pk
                },
                conn=conn
            )
        return web.json_response(dict(object))

    async def delete_object(self, db_table, pk):
        async with service.db_pool.acquire() as conn:
            await db.exec_universal_delete_query(
                db_table,
                where={
                    'id': pk
                },
                conn=conn
            )
        return web.Response(status=204)