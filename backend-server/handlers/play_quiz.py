import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.secure_v1 import smkSecureV1
from bson import ObjectId
import json
import time
from handlers.base_handler import CustomBaseHandler
import time
import sys
import json
from bson.json_util import dumps


class PlayQuizHandler(CustomBaseHandler, MongoMixing):

    quizzes = MongoMixing.db['quizzes']
    quizResults = MongoMixing.db['quizResults']
    questions = MongoMixing.db['questions']

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
            try:
                quiz_id = self.get_argument('id')
            except:
                message = 'Invalid Quiz Id'
                raise Exception
            if quiz_id and self.is_valid_objectid(quiz_id):
                quizQuery = self.quizzes.aggregate(
                    [
                        {
                            '$match': {
                                '_id': ObjectId(quiz_id)
                            }
                        },
                        {
                            '$lookup': {
                                'from': 'questions',
                                'localField': 'questions',
                                'foreignField': '_id',
                                'as': 'questions',
                                'pipeline': [
                                    {
                                        '$project': {
                                            '_id': {
                                                '$toString': '$_id'
                                            },
                                            'question': 1,
                                            'options': 1
                                        }
                                    },
                                    {
                                        '$limit': 10
                                    }
                                ]
                            }
                        },
                        {
                            '$project': {
                                '_id': 1,
                                'quizName': 1,
                                'duration': 1,
                                'startDate': 1,
                                'endDate': 1,
                                'questions': 1
                            }
                        }
                    ]
                )

                async for quiz in quizQuery:
                    # Convert ObjectId to string
                    quiz['_id'] = str(quiz['_id'])
                    result.append(quiz)

                if len(result):
                    status = True
                    code = 2002
                else:
                    message = 'Quiz not found.'
                    code = 4040
            else:
                message = 'Invalid Quiz Id.'
                code = 4040

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write(json.loads(dumps({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })))

    async def post(self):
        """Submit Quiz Results (POST)"""
        code = 4000
        message = ''
        result = []
        status = False

        try:
            body = json.loads(self.request.body.decode('utf-8'))

            fullName = body.get('fullName', '').strip()
            phoneNumber = body.get('phoneNumber', '').strip()
            try:
                if len(phoneNumber) != 10:
                    raise Exception()
                phoneNumber = int(phoneNumber)
            except:
                message = 'Invalid phone number.'
                code = 4123
                raise Exception

            quizId = body.get('_id')
            questions = body.get('questions', [])

            if not fullName or not phoneNumber:
                raise ValueError(
                    'Missing required fields: fullName, or phoneNumber')

            if not self.is_valid_objectid(quizId):
                raise ValueError('Invalid Quiz Id')

            quizId = ObjectId(quizId)
            quizInfo = await self.quizzes.find_one(
                {
                    '_id': quizId,
                    'endDate': {'$gt': time.time()}
                },
                {
                    '_id': 1,
                    'questions': 1,
                    'quizName': 1
                }
            )

            if not quizInfo:
                raise ValueError('Quiz not found or expired')

            exQuizResult = await self.quizResults.find_one(
                {
                    'quizId': quizId,
                    'phoneNumber': phoneNumber
                }
            )
            if exQuizResult:
                message = 'This quiz result has already been submitted.'
                code = 2020
                raise Exception

            score = 0
            for quest in questions:
                questInfo = await self.questions.find_one(
                    {
                        '_id': ObjectId(quest.get('_id'))
                    },
                    {
                        '_id': 1,
                        'ans': 1
                    }
                )
                quest['right'] = quest.get('ans') == questInfo.get('ans')
                if quest['right']:
                    score += 1

            quizResult = {
                'quizId': quizId,
                'quizName': quizInfo.get('quizName'),
                'score': score,
                'time': int(time.time()),
                'questions': questions,
                'total': len(questions),
                'fullName': fullName,
                'phoneNumber': phoneNumber
            }

            insertResult = await self.quizResults.insert_one(quizResult)

            if insertResult.inserted_id:
                del quizResult['_id']
                del quizResult['fullName']
                del quizResult['phoneNumber']
                del quizResult['questions']
                status = True
                code = 2002
                message = 'Quiz result has been submitted.'
                result.append(quizResult)
            else:
                raise ValueError('Failed to submit the result')
        except Exception as e:
            Log.info(e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            Log.info(
                f'EXC {e} - FILE: {exc_tb.tb_frame.f_code.co_filename} LINE: {exc_tb.tb_lineno} TYPE: {exc_type}')
            code = 5010

        self.write(json.loads(dumps({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })))
