import base64

from aiohttp import web
from utils.service import service
from views.users import Users
from views.items import Items
from views.categories import Category

from cryptography import fernet
from aiohttp_session import setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from middlewares.auth_user import auth_middleware


async def init_service(app):
    await service.init()


class Server(web.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        Users().register_routes(self.router)
        Items().register_routes(self.router)
        Category().register_routes(self.router)

        setup(self, self._get_cookie_storage())
        self.middlewares.append(auth_middleware)

    def _get_cookie_storage(self):
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        return EncryptedCookieStorage(secret_key)


server = Server()
server.on_startup.append(init_service)
web.run_app(server, port=8080)