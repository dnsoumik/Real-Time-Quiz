import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.secure_v1 import smkSecureV1
from bson import ObjectId
import json
import time

@smkSecureV1
class QuizHandler(tornado.web.RequestHandler, MongoMixing):

    quizzes = MongoMixing.db['quizzes']

    def is_valid_objectid(self, oid):
        """Helper method to check if a question ID is a valid ObjectId."""
        return ObjectId.is_valid(oid)

    def is_valid_quizName(self, quizName):
        """Helper method to validate quiz name."""
        return isinstance(quizName, str) and len(quizName) > 3

    def is_valid_questions(self, questions):
        """Helper method to validate questions array."""
        return isinstance(questions, list) and all(self.is_valid_objectid(q) for q in questions)

    def is_valid_duration(self, duration):
        """Helper method to validate quiz duration."""
        return isinstance(duration, int) and duration > 0

    def is_valid_timestamp(self, timestamp):
        """Helper method to validate timestamps."""
        return isinstance(timestamp, int) and timestamp > 0

    async def get(self, quiz_id=None):
        """Read Quiz by ID (GET)"""
        code = 4000
        message = ''
        result = []
        status = False

        try:
            if quiz_id and self.is_valid_objectid(quiz_id):
                quiz = await self.quizzes.find_one({'_id': ObjectId(quiz_id)})

                if quiz:
                    quiz['_id'] = str(quiz['_id'])  # Convert ObjectId to string
                    result = quiz
                    code = 2000
                    status = True
                else:
                    message = 'Quiz not found.'
                    code = 4040
            else:
                quizQ = self.quizzes.find()
                async for quiz in quizQ:
                    quiz['_id'] = str(quiz['_id'])
                    result.append(quiz)
                if len(result):
                    code = 2000
                    status = True
                else:
                    message = 'No Quizzes found.'
                    code = 4040

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })

    async def post(self):
        """Create Quiz (POST)"""
        code = 4000
        message = ''
        result = None
        status = False

        try:
            body = json.loads(self.request.body.decode('utf-8'))
            quizName = body.get('quizName')
            questions = body.get('questions')
            duration = body.get('duration')
            startDate = body.get('startDate')
            endDate = body.get('endDate')

            # Validations
            if not self.is_valid_quizName(quizName):
                message = 'Invalid quiz name. It must be a string with at least 3 characters.'
                code = 4150
            elif not self.is_valid_questions(questions):
                message = 'Invalid questions array. Each question must be a valid ObjectId.'
                code = 4150
            elif not self.is_valid_duration(duration):
                message = 'Invalid duration. It must be a positive integer.'
                code = 4150
            elif not self.is_valid_timestamp(startDate):
                message = 'Invalid start date. It must be a valid Unix timestamp.'
                code = 4150
            elif not self.is_valid_timestamp(endDate):
                message = 'Invalid end date. It must be a valid Unix timestamp.'
                code = 4150
            elif startDate >= endDate:
                message = 'Start date must be earlier than end date.'
                code = 4150
            else:
                quiz_data = {
                    'quizName': quizName,
                    'questions': [ObjectId(q) for q in questions],
                    'duration': duration,
                    'startDate': startDate,
                    'endDate': endDate
                }
                insert_result = await self.quizzes.insert_one(quiz_data)
                if insert_result.inserted_id:
                    message = 'Quiz created successfully.'
                    code = 2000
                    status = True
                    result = str(insert_result.inserted_id)
                else:
                    message = 'Quiz creation failed.'
                    code = 5000

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })

    async def put(self, quiz_id):
        """Update Quiz by ID (PUT)"""
        code = 4000
        message = ''
        result = None
        status = False

        try:
            if not self.is_valid_objectid(quiz_id):
                message = 'Invalid Quiz ID.'
                code = 4000
            else:
                body = json.loads(self.request.body.decode('utf-8'))
                quizName = body.get('quizName')
                questions = body.get('questions')
                duration = body.get('duration')
                startDate = body.get('startDate')
                endDate = body.get('endDate')

                # Validations
                if not self.is_valid_quizName(quizName):
                    message = 'Invalid quiz name. It must be a string with at least 3 characters.'
                    code = 4150
                elif not self.is_valid_questions(questions):
                    message = 'Invalid questions array. Each question must be a valid ObjectId.'
                    code = 4150
                elif not self.is_valid_duration(duration):
                    message = 'Invalid duration. It must be a positive integer.'
                    code = 4150
                elif not self.is_valid_timestamp(startDate):
                    message = 'Invalid start date. It must be a valid Unix timestamp.'
                    code = 4150
                elif not self.is_valid_timestamp(endDate):
                    message = 'Invalid end date. It must be a valid Unix timestamp.'
                    code = 4150
                elif startDate >= endDate:
                    message = 'Start date must be earlier than end date.'
                    code = 4150
                else:
                    update_data = {
                        'quizName': quizName,
                        'questions': [ObjectId(q) for q in questions],
                        'duration': duration,
                        'startDate': startDate,
                        'endDate': endDate
                    }

                    update_result = await self.quizzes.update_one(
                        {'_id': ObjectId(quiz_id)},
                        {'$set': update_data}
                    )

                    if update_result.modified_count:
                        message = 'Quiz updated successfully.'
                        code = 2000
                        status = True
                    else:
                        message = 'Quiz update failed or no changes made.'
                        code = 5000

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status,
            'result': result
        })

    async def delete(self, quiz_id):
        """Delete Quiz by ID (DELETE)"""
        code = 4000
        message = ''
        status = False

        try:
            if not self.is_valid_objectid(quiz_id):
                message = 'Invalid Quiz ID.'
                code = 4000
            else:
                delete_result = await self.quizzes.delete_one({'_id': ObjectId(quiz_id)})

                if delete_result.deleted_count:
                    message = 'Quiz deleted successfully.'
                    code = 2000
                    status = True
                else:
                    message = 'Quiz not found or could not be deleted.'
                    code = 4040

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status
        })
