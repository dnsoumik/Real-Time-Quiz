
import tornado.ioloop
import tornado.web

from handlers.sign_in import SignInHandler
from handlers.profile import MyProfileHandler

def make_app():
    return tornado.web.Application([
        (r"/sign_in", SignInHandler),
        (r'/my_profile', MyProfileHandler)
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado server running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
