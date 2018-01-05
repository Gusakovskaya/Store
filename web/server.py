from aiohttp import web
from views.users import Users
from views.items import Items
from utils.service import service


async def init_service(app):
    await service.init()


class Server(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Users().register_routes(self.router)
        Items().register_routes(self.router)


server = Server()
server.on_startup.append(init_service)
web.run_app(server, port=8080)