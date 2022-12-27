from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
from config.config import MONGO_DB_NAME, MONGO_URL

#앱이 구동되었을때 DB와 연결을 위한 코드
#엔진을 글로벌로 만들어 다른 곳에서 참조 가능하도록 생성
class MongoDB:

    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.engine = AIOEngine(client=self.client, database=MONGO_DB_NAME)
        print("DB와 성공적으로 연결이 되었습니다.")

    def close(self):
        self.client.close()

mongodb = MongoDB()
