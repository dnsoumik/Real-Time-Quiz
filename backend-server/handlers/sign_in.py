
import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.jwt_util import JWTHandler
from handlers.base_handler import CustomBaseHandler

class SignInHandler(CustomBaseHandler, MongoMixing):

    accounts = MongoMixing.db['accounts']

    async def post(self):

        code = 4000
        message = ''
        result = []
        status = False

        # Get username and password from form input
        try:
            try:
                username = self.get_argument("username")
                if type(username) is not str:
                    raise Exception('username error')
            except Exception as e:
                Log.info(e)
                message = 'Please enter a valid username.'
                code = 4100
                raise Exception

            try:
                password = self.get_argument("password")
                if type(password) is not str:
                    raise Exception('pass error')
            except Exception as e:
                Log.info(e)
                message = 'Please enter a valid password.'
                code = 4200
                raise Exception

            accountInfo = await self.accounts.find_one(
                {
                    'username': username,
                    'password': password
                },
                {
                    '_id': 1
                }
            )
            if accountInfo:
                enToken = JWTHandler().generate_token(user_id=str(accountInfo.get('_id')))
                Log.info(enToken)
                result.append(enToken)
                status = True
                code = 2000
            else:
                message = 'Wrong username or password.'
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