from werkzeug.wrappers import Request, Response
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.routing import Map, Rule
from compilation_builder.packager import PythonPackager, PackagerException
import json

'''
Control class for our little service
'''


class Orchestrator(object):
    def __init__(self, configs):
        self.configs = configs
        self.url_map = Map([
            Rule('/health', endpoint='health'),
            Rule('/submit', endpoint='submit'),
            Rule('/getresult', endpoint='getresult')
        ])

    def on_health(self, request):
        return Response("I'm up and alive")

    def on_getresult(self, request):
        return Response("not implemented")

    def on_submit(self, request):
        question_name = ''
        lang = ''
        code = ''
        test = ''
        execution_result = ''
        if request.method == 'POST':
            question_name = request.form['question_name']
            lang = request.form['language']
            code = request.form['code']
            test = request.form['test']

            if lang.lower() == 'python':
                py_packager = PythonPackager(self.configs)
                bundle = py_packager.bundle(question_name, code, test)

                execution_result = py_packager.execute(bundle)
            else:
                raise PackagerException("Unexpected language type.")

        got_data = {
            'language': lang,
            'code': code,
            'test': test,
            'question_name': question_name
        }
        response_payload = {
            'execution_result': execution_result,
            'got_data': got_data
        }
        # dispatch_request expects any response object or throws an exception
        return Response(json.dumps(response_payload), mimetype='text/json')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except NotFound as e:
            return e
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(program_configs=None):
    app = Orchestrator(program_configs)
    return app
