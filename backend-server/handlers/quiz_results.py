import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.secure_v1 import smkSecureV1
from bson import ObjectId
import json
import time
from handlers.base_handler import CustomBaseHandler

@smkSecureV1
class QuizResultsHandler(CustomBaseHandler, MongoMixing):

    quizResults = MongoMixing.db['quizResults']

    def is_valid_objectid(self, oid):
        """Helper method to check if a question ID is a valid ObjectId."""
        return ObjectId.is_valid(oid)

    async def get(self):
        """Read Quiz by ID (GET)"""
        code = 4000
        message = ''
        result = []
        status = False

        try:
            f_limit = 100
            f_skip = 0
            try:
                f_limit = int(self.get_argument('limit'))
                f_skip = int(self.get_argument('skip'))
            except:
                f_limit = 100
                f_skip = 0

            quizResults = self.quizResults.aggregate(
                [
                    {
                        '$sort': {
                            'time': -1
                        }
                    },
                    {
                        '$skip': f_limit * f_skip
                    },
                    {
                        '$limit': f_limit
                    },
                    {
                        '$project': {
                            '_id': {
                                '$toString': '$quizId'
                            },
                            'fullName': 1,
                            'score': 1,
                            'total': 1,
                            'time': 1
                        }
                    }
                ]
            )
            async for qResult in quizResults:
                result.append(qResult)
            if len(result):
                code = 2020
                status = True
                message = ''
            else:
                message = 'No results found'
                code = 4067
        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })
