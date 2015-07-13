from werkzeug.wrappers import Request, Response
from compilation_builder.orchestrator import create_app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('localhost', 4000, o)
