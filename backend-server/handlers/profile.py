import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.secure_v1 import smkSecureV1
from bson import ObjectId
from handlers.base_handler import CustomBaseHandler

@smkSecureV1
class MyProfileHandler(CustomBaseHandler, MongoMixing):

    accounts = MongoMixing.db['accounts']

    async def get(self):

        code = 4000
        message = ''
        result = []
        status = False

        try:
            accountInfo = await self.accounts.find_one(
                {
                    '_id': ObjectId(self.accountId),
                },
                {
                    '_id': 0,
                    'firstName': 1,
                    'lastName': 1
                }
            )
            if accountInfo:
                result.append(accountInfo)
                status = True
                code = 2000
            else:
                message = 'Profile not found.'
                code = 4150
                status = False

        except Exception as e:
            Log.info(e)

        self.write(
            {
                'code': code,
                'message': message,
                'status': status,
                'result': result
            }
        )