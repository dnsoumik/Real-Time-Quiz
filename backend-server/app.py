import tornado.ioloop
import tornado.web

from handlers.sign_in import SignInHandler
from handlers.profile import MyProfileHandler
from handlers.questions import QuestionsHandler
from handlers.quizzes import QuizHandler
from handlers.play_quiz import PlayQuizHandler
from handlers.base_handler import CustomBaseHandler
from handlers.quiz_results import QuizResultsHandler

# Catch-all handler for OPTIONS requests on any path
class CatchAllOptionsHandler(CustomBaseHandler):
    def options(self, *args, **kwargs):
        self.set_status(200)
        self.finish()

def make_app():
    return tornado.web.Application([
        (r"/api/sign_in", SignInHandler),
        (r'/api/my_profile', MyProfileHandler),
        (r'/api/questions', QuestionsHandler),
        (r'/api/quizzes', QuizHandler),
        (r'/api/play_quiz', PlayQuizHandler),
        (r'/api/quiz_results', QuizResultsHandler),
        (r".*", CatchAllOptionsHandler)  # Catch all for OPTIONS
    ])


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado server running on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
