import tornado
from utils.log_util import Log
from utils.mongo_util import MongoMixing
from utils.secure_v1 import smkSecureV1
from bson import ObjectId
import json
import re

@smkSecureV1
class QuestionsHandler(tornado.web.RequestHandler, MongoMixing):

    questions = MongoMixing.db['questions']

    def is_valid_objectid(self, oid):
        """Helper method to check if the question_id is a valid ObjectId."""
        return ObjectId.is_valid(oid)

    def is_valid_question(self, question):
        """Helper method to validate question."""
        return isinstance(question, str) and len(question) > 5

    def is_valid_options(self, options):
        """Helper method to validate options."""
        return isinstance(options, list) and len(options) >= 2

    def is_valid_ans(self, ans, options):
        """Helper method to validate answer (ans) with respect to options."""
        return isinstance(ans, int) and 0 <= ans < len(options)

    async def get(self, question_id=None):
        """Read Question by ID (GET)"""
        code = 4000
        message = ''
        result = []
        status = False

        try:
            if question_id and self.is_valid_objectid(question_id):
                question = await self.questions.find_one({'_id': ObjectId(question_id)})

                if question:
                    question['_id'] = str(question['_id'])  # Convert ObjectId to string
                    result = question
                    code = 2000
                    status = True
                else:
                    message = 'Question not found.'
                    code = 4040
            else:
                questionQ = self.questions.find()
                async for quest in questionQ:
                    quest['_id'] = str(quest['_id'])
                    result.append(quest)
                if len(result):
                    code = 2000
                    status = True
                else:
                    message = 'No Questions found.'
                    code = 4040
                code = 2200

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
        """Create Question (POST)"""
        code = 4000
        message = ''
        result = None
        status = False

        try:
            body = json.loads(self.request.body.decode('utf-8'))
            question = body.get('question')
            options = body.get('options')
            ans = body.get('ans')

            if not self.is_valid_question(question):
                message = 'Invalid question. It must be a string with at least 5 characters.'
                code = 4150
            elif not self.is_valid_options(options):
                message = 'Invalid options. It must be a list with at least 2 items.'
                code = 4150
            elif not self.is_valid_ans(ans, options):
                message = 'Invalid answer. It must be an index of one of the options.'
                code = 4150
            else:
                question_data = {
                    'question': question,
                    'options': options,
                    'ans': ans
                }
                insert_result = await self.questions.insert_one(question_data)
                if insert_result.inserted_id:
                    message = 'Question created successfully.'
                    code = 2000
                    status = True
                    result = str(insert_result.inserted_id)
                else:
                    message = 'Question creation failed.'
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

    async def put(self, question_id):
        """Update Question by ID (PUT)"""
        code = 4000
        message = ''
        result = None
        status = False

        try:
            if not self.is_valid_objectid(question_id):
                message = 'Invalid Question ID.'
                code = 4000
            else:
                body = json.loads(self.request.body.decode('utf-8'))
                question = body.get('question')
                options = body.get('options')
                ans = body.get('ans')

                if not self.is_valid_question(question):
                    message = 'Invalid question. It must be a string with at least 5 characters.'
                    code = 4150
                elif not self.is_valid_options(options):
                    message = 'Invalid options. It must be a list with at least 2 items.'
                    code = 4150
                elif not self.is_valid_ans(ans, options):
                    message = 'Invalid answer. It must be an index of one of the options.'
                    code = 4150
                else:
                    update_data = {
                        'question': question,
                        'options': options,
                        'ans': ans
                    }

                    update_result = await self.questions.update_one(
                        {'_id': ObjectId(question_id)},
                        {'$set': update_data}
                    )

                    if update_result.modified_count:
                        message = 'Question updated successfully.'
                        code = 2000
                        status = True
                    else:
                        message = 'Question update failed or no changes made.'
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

    async def delete(self, question_id):
        """Delete Question by ID (DELETE)"""
        code = 4000
        message = ''
        status = False

        try:
            if not self.is_valid_objectid(question_id):
                message = 'Invalid Question ID.'
                code = 4000
            else:
                delete_result = await self.questions.delete_one({'_id': ObjectId(question_id)})

                if delete_result.deleted_count:
                    message = 'Question deleted successfully.'
                    code = 2000
                    status = True
                else:
                    message = 'Question not found or could not be deleted.'
                    code = 4040

        except Exception as e:
            Log.info(e)
            message = 'Server error.'

        self.write({
            'code': code,
            'message': message,
            'status': status
        })
