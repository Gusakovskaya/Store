import sys
sys.path.insert(0, '../')

from aiohttp import web


class Users:
    def register_routes(self, router):
        router.add_get('/api/users', self.list_users)

    async def list_users(self, request):
        return web.Response(text="list_users")
