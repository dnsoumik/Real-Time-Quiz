from functools import wraps
import tornado.web
from utils.jwt_util import JWTHandler
from utils.log_util import Log

def smkSecureV1(cls):
    """
    A class-level decorator that applies JWT authentication to all HTTP methods (get, post, etc.)
    of the Tornado RequestHandler class.
    """
    original_init = cls.__init__
    jwt_handler = JWTHandler()

    def wrapper_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # Initialize JWTHandler

    cls.__init__ = wrapper_init

    def jwt_authentication_wrapper(method):
        """Reusable JWT authentication wrapper for request handler methods."""
        @wraps(method)
        def wrapped_method(self, *args, **kwargs):

            if 'localhost' in self.request.full_url() and self.request.method == 'OPTIONS':
                self.set_header("Access-Control-Allow-Origin", "*")
                self.set_header("Access-Control-Allow-Headers", "Content-Type,Authorization")
                self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
                return

            token = self.request.headers.get('Authorization', None)
            if token:
                try:
                    # Assuming token comes in "Bearer <token>" format
                    token = token.split(" ")[1]
                    decoded_token = jwt_handler.decode_token(token)
                    cls.accountId = decoded_token['user_id']
                    Log.info('Account Id' + cls.accountId)
                except (tornado.web.HTTPError, IndexError) as e:
                    self.set_status(401)
                    self.write({'error': 'Invalid or missing token', 'message': str(e)})
                    return
            else:
                self.set_status(401)
                self.write({'error': 'Missing Authorization header'})
                return

            # Call the original method
            return method(self, *args, **kwargs)

        return wrapped_method

    # Loop through all standard HTTP methods and apply the wrapper only if the method exists
    for method in ['get', 'post', 'put', 'delete', 'patch', 'options']:
        if hasattr(cls, method):
            original_method = getattr(cls, method)
            setattr(cls, method, jwt_authentication_wrapper(original_method))

    return cls
