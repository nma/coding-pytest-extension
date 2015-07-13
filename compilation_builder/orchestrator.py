from werkzeug.wrappers import Request, Response

class Orchestrator(object):

    def __init__(self, configs):
        self.configs = configs

    def dispatch_request(self, request):
        return Response('Hello World!')

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def create_app(program_configs=None):
    app = Orchestrator(program_configs)
    return app
