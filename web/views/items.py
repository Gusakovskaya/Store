import sys
sys.path.insert(0, '../')

from utils import settings
from .base import BaseView


class Items(BaseView):

    def register_routes(self, router):
        router.add_get('/api/items', self.list_items)
        router.add_get('/api/items/{id:\d+}', self.retrieve_item)
        router.add_post('/api/items', self.create_item)
        router.add_put('/api/items/{id:\d+}', self.update_item)
        router.add_delete('/api/items/{id:\d+}', self.delete_item)

    async def validate_post_data(self, data):
        for required_field in ['name', 'category_id']:
            if not data.get(required_field):
                return 'Field {} is required'.format(required_field)

        for positive_field in ['value', 'quantity']:
            value = data.get(positive_field)
            if value and value < 0:
                return 'Field {} must be positive'

        category_id = data.get('category_id')
        category = await self.get_object(settings.CATEGORY_DB_TABLE, category_id)
        if not category:
            return 'Category with supplied id does not exists'
        return None

    async def validate_put_data(self, data):
        for positive_field in ['value', 'quantity']:
            value = data.get(positive_field)
            if value and value < 0:
                return 'Field {} must be positive'

        category_id = data.get('category_id')
        if category_id:
            category = await self.get_object(settings.CATEGORY_DB_TABLE, category_id)
            if not category:
                return 'Category with supplied id does not exists'

        return None

    async def list_items(self, request):
        return await self.list_objects(settings.ITEM_DB_TABLE)

    async def retrieve_item(self, request):
        item_id = int(request.match_info.get('id'))
        return await self.retrieve_object(settings.ITEM_DB_TABLE, item_id)

    async def create_item(self, request):
        data = await request.json()
        return await self.create_object(settings.ITEM_DB_TABLE, data, self.validate_post_data)

    async def update_item(self, request):
        user_id = int(request.match_info.get('id'))
        data = await request.json()
        return await self.update_object(settings.ITEM_DB_TABLE, user_id, data, self.validate_put_data)

    async def delete_item(self, request):
        user_id = int(request.match_info.get('id'))
        return await self.delete_object(settings.ITEM_DB_TABLE, user_id)

