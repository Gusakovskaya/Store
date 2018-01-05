import sys
sys.path.insert(0, '../')

from aiohttp import web
from utils.service import service
from utils import db, settings
from .base import BaseView


class Users(BaseView):

    def register_routes(self, router):
        router.add_get('/api/users', self.list_users)
        router.add_get('/api/users/{id:\d+}', self.retrieve_user)
        router.add_post('/api/users', self.create_user)
        router.add_put('/api/users/{id:\d+}', self.update_user)
        router.add_delete('/api/users/{id:\d+}', self.delete_user)
        router.add_get('/api/users/{id:\d+}/avatar', self.avatar)
        router.add_post('/api/users/{id:\d+}/avatar', self.avatar)

    async def validate_post_data(self, data):
        for required_field in ['email', 'shipping_adress', 'password', 'role']:
            if not data.get(required_field):
                return 'Field {} is required'.format(required_field)

        async with service.db_pool.acquire() as conn:
            existed_user = await db.exec_universal_select_query(
                settings.USER_DB_TABLE,
                where={
                    'email': data['email']
                },
                one=True,
                conn=conn
            )
            if existed_user:
                return 'User with supplied email already exists'

        if data['role'] not in ['admin', 'customer']:
            return 'Role must be admin|customer'

        return None

    async def validate_put_data(self, user, data):
        email = data.get('email')
        if email and email != user['email']:
            async with service.db_pool.acquire() as conn:
                existed_user = await db.exec_universal_select_query(
                    settings.USER_DB_TABLE,
                    where={
                        'email': data['email']
                    },
                    one=True,
                    conn=conn
                )
                if existed_user:
                    return 'User with supplied email already exists'

        role = data.get('role')
        if role and role not in ['admin', 'customer']:
            return 'Role must be admin|customer'

        return None

    async def list_users(self, request):
        return await self.list_objects(settings.USER_DB_TABLE)

    async def retrieve_user(self, request):
        user_id = int(request.match_info.get('id'))
        return await self.retrieve_object(settings.USER_DB_TABLE, user_id)

    async def create_user(self, request):
        data = await request.json()
        return await self.create_object(settings.USER_DB_TABLE, data, self.validate_post_data)

    async def update_user(self, request):
        user_id = int(request.match_info.get('id'))
        data = await request.json()
        return await self.update_object(settings.USER_DB_TABLE, user_id, data, self.validate_put_data)

    async def delete_user(self, request):
        user_id = int(request.match_info.get('id'))
        return await self.delete_object(settings.USER_DB_TABLE, user_id)

    async def avatar(self, request):
        user_id = int(request.match_info.get('id'))
        user = await self.get_object(settings.USER_DB_TABLE, user_id)

        if not user:
            return web.Response(text='User not found')

        if request.method == 'GET':
            if not user['avatar_key']:
                return web.Response(text='Image is not set', status=404)

            file = await service.s3_client.get_object(Bucket='users',
                                                      Key=user['avatar_key'])
            content = await file['Body'].read()
            return web.Response(body=content, content_type=file['ContentType'])
        else:
            data = await request.post()
            content = data['file'].file.read()
            if user['avatar_key']:
                await service.s3_client.delete_object(
                    Bucket=settings.USER_BUCKET,
                    Key=user['avatar_key']
                )

            avatar_key = '{}/{}'.format(user_id, data['file'].filename)
            await service.s3_client.put_object(Bucket='users',
                                               Key=avatar_key,
                                               Body=content)

            async with service.db_pool.acquire() as conn:
                user = await db.exec_universal_update_query(
                    settings.USER_DB_TABLE,
                    set={
                        'avatar_url': '/api/users/{}/avatar'.format(user['id']),
                        'avatar_key': avatar_key
                    },
                    where={
                        'id': user['id']
                    },
                    conn=conn
                )
            return web.json_response({'avatar_url': user['avatar_url']})
