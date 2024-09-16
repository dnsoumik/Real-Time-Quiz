
import tornado
from utils.log_util import Log

class CustomBaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        # Add CORS headers or any other headers you may need
        if 'localhost' in self.request.full_url():
            self.set_header("Access-Control-Allow-Origin", "*")
            self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
            self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    def options(self):
        # Respond with 200 OK for any OPTIONS request
        self.set_status(200)
        self.finish()
