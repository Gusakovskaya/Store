import aiobotocore
import asyncio
import botocore
import aiopg

from utils.meta import Singleton
from utils.settings import MINIO_SECRET_KEY, MINIO_ACCESS_KEY, CONNECTION_STRING


class Service(metaclass=Singleton):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.s3_client = None
        self.db_pool = None

    async def init_s3(self):
        session = aiobotocore.get_session(loop=self.loop)
        self.s3_client = session.create_client('s3',
                                               endpoint_url='http://localhost:9000',
                                               aws_secret_access_key=MINIO_SECRET_KEY,
                                               aws_access_key_id=MINIO_ACCESS_KEY,
                                               config=botocore.config.Config(signature_version='s3v4'))
        try:
            await self.s3_client.head_bucket(Bucket='users')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                await self.s3_client.create_bucket(Bucket='users')

    async def init_db_pool(self):
        self.db_pool = await aiopg.create_pool(CONNECTION_STRING)

    async def init(self):
        await self.init_s3()
        await self.init_db_pool()


service = Service()