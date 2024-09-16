
from motor.motor_tornado import MotorClient
from datetime import datetime, timedelta
from utils.log_util import Log

class MongoMixing:

    try:
        # MongoDB setup
        client = MotorClient("mongodb://localhost:27017")
        db = client.ElsaQuiz
    except Exception as e:
        Log.error('Mongo Connection Error')