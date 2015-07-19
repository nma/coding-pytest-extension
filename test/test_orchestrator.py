from compilation_builder.python_packager import PackagerConfig
from compilation_builder.orchestrator import Orchestrator
from test.base_test_case import BaseTestCase
from werkzeug.wrappers import Request
from multiprocessing import Process
import unittest, os, json, requests

class TestOrchestrator(BaseTestCase):

    @classmethod
    def start_test_server(cls):
        test_directory = os.path.dirname(os.path.realpath(__file__))
        test_config = os.path.join(test_directory, "packager_config.cfg")

        packager_config = PackagerConfig(test_config)
        app = Orchestrator(packager_config)
       
        from werkzeug.serving import run_simple
        run_simple('127.0.0.1', 5000, app)

    @classmethod
    def setUpClass(cls):
        """Spin up a server in a seperate process
        """
        cls.p = Process(target=cls.start_test_server, daemon=True)
        cls.p.start()
       
    @classmethod
    def tearDownClass(cls):
        """Make sure we tear down the process properly at the end 
        """
        cls.p.terminate()

    def testOrchestratorAcceptingInput(self):
        with open(self.get_file('code'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            language = 'python'
            code_payload = code.read()
            test_payload = test.read()
            payload = {'language': language, 'code': code_payload, 'test': test_payload}
           
            # http:// required, requests library needs protocol scheme to connect
            got_resp = requests.post('http://127.0.0.1:5000/submit', data=payload)
            exp_data = {'language': language, 'code': code_payload, 'test': test_payload}
            exp_response_message = '' 
            exp_resp = {'response': exp_response_message, 'got_data': exp_data}

            self.assertEquals(exp_resp, json.loads(got_resp.text))
            
