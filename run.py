from werkzeug.wrappers import Request, Response
from compilation_builder.orchestrator import create_app
from compilation_builder.python_packager import PackagerConfig
import os

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    packager_config = PackagerConfig("packager_config.cfg") 
    app = create_app(packager_config)
    run_simple('localhost', 4000, app)
