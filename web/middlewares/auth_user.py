import sys
sys.path.insert(0, '../')

import re
import base64

from aiohttp.web import Response, middleware
from aiohttp_session import get_session

from utils import db, settings
from utils.service import service


async def check_basic_auth(request):
    auth_string = request.headers.get('Authorization')
    encoded_string = auth_string.split('Basic ')[1]

    email, password = base64.b64decode(encoded_string).decode().split(':')

    async with service.db_pool.acquire() as conn:
        user = await db.exec_universal_select_query(
            settings.USER_DB_TABLE,
            where={
                'email': email,
                'password': password
            },
            one=True,
            conn=conn
        )
        if not user:
            return False
        session = await get_session(request)
        session['authorized'] = user['id']
    return True


@middleware
async def auth_middleware(request, handler):
    if re.match('/api/users/(login|signup)', request.path):
        return await handler(request)

    if 'Authorization' in request.headers:
        if not await check_basic_auth(request):
            return Response(status=401)
        return await handler(request)

    session = await get_session(request)
    if 'authorized' not in session or not session['authorized']:
        return Response(status=401)
    else:
        return await handler(request)