import sys
sys.path.insert(0, '../')

from utils import settings, db
from utils.service import service
from .base import BaseView


class Category(BaseView):

    def register_routes(self, router):
        router.add_get('/api/categories', self.list_categories)
        router.add_get('/api/categories/{id:\d+}', self.retrieve_category)
        router.add_post('/api/categories', self.create_category)
        router.add_put('/api/categories/{id:\d+}', self.update_category)
        router.add_delete('/api/categories/{id:\d+}', self.delete_category)

    async def validate_post_data(self, data):
        for required_field in ['name']:
            if not data.get(required_field):
                return 'Field {} is required'.format(required_field)
        return None

    async def validate_put_data(self, data):
        return None

    async def list_categories(self, request):
        return await self.list_objects(settings.CATEGORY_DB_TABLE)

    async def retrieve_category(self, request):
        item_id = int(request.match_info.get('id'))
        return await self.retrieve_object(settings.CATEGORY_DB_TABLE, item_id)

    async def create_category(self, request):
        data = await request.json()
        return await self.create_object(settings.CATEGORY_DB_TABLE, data, self.validate_post_data)

    async def update_category(self, request):
        category_id = int(request.match_info.get('id'))
        data = await request.json()
        return await self.update_object(settings.CATEGORY_DB_TABLE, category_id, data, self.validate_put_data)

    async def delete_category(self, request):
        category_id = int(request.match_info.get('id'))
        async with service.db_pool.acquire() as conn:
            items = await db.exec_universal_select_query(
                settings.ITEM_DB_TABLE,
                where={
                    'category_id': category_id
                },
                conn=conn
            )
            for item in items:
                await db.exec_universal_delete_query(
                    settings.ITEM_DB_TABLE,
                    where={
                        'id': item['id']
                    },
                    conn=conn
                )
        return await self.delete_object(settings.CATEGORY_DB_TABLE, category_id)
