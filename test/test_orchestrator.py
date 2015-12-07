from multiprocessing.context import Process
import unittest
from requests.packages.urllib3.exceptions import NewConnectionError
from compilation_builder.packager import PackagerConfig
from compilation_builder.orchestrator import Orchestrator
from test.base_test_case import BaseTestCase
import os
import json
import requests
import time
import logging


logger = logging.getLogger(name=__name__)


def exponential_back_off(func, limit=3):
    def wrapped_method(*args, **kwargs):
        cur_limit = 0
        back_off_seconds = 2;
        while cur_limit < limit:
            try:
                r = func(*args, **kwargs)
                if not r or r.status_code != 200:
                    cur_limit += 1
                    time.sleep(back_off_seconds)
                    back_off_seconds <<= 1;
                else:
                    return r
            except (NewConnectionError, ConnectionRefusedError):
                cur_limit += 1
                time.sleep(back_off_seconds)
                back_off_seconds <<= 1;
                logger.warn("Timeout incrementing limit")

    return wrapped_method


class TestOrchestrator(BaseTestCase):

    def setUp(self):
        self.test_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_config = os.path.join(self.test_directory, "packager_config.cfg")
        self.packager_config = PackagerConfig(self.test_config)
        """Spin up a server in a seperate process"""
        def start_test_server():
            app = Orchestrator(self.packager_config)
            from werkzeug.serving import run_simple
            run_simple('127.0.0.1', 5000, app)

        self.p = Process(target=start_test_server, daemon=True)
        self.p.start()

    def tearDown(self):
        """Make sure we tear down the process properly at the end"""
        self.p.terminate()

    def testOrchestratorAcceptingInputCorrectly(self):
        @exponential_back_off
        def wait_for_process():
            return requests.get("http://127.0.0.1:5000/health")

        wait_seconds = 1
        print("await process spin up for %d seconds" % wait_seconds)
        time.sleep(wait_seconds)
        wait_for_process()

        with open(self.get_file('code'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            language = 'python'
            question_name = 'foo'
            code_payload = code.read()
            test_payload = test.read()
            payload = {'question_name': question_name, 'language': language, 'code': code_payload, 'test': test_payload}
           
            # http:// required, requests library needs protocol scheme to connect
            got_resp_raw = requests.post('http://127.0.0.1:5000/submit', data=payload)
            got_resp = json.loads(got_resp_raw.text)
            exp_data = {'language': language, 'code': code_payload, 'test': test_payload, 'question_name': question_name}
            exp_response_message = 'not tested for in this testcase' 
            exp_resp = {'execution_result': exp_response_message, 'got_data': exp_data}

            self.assertEqual(exp_resp['got_data'], got_resp['got_data'])

            # we just need to check if the result contains success
            for testcase, test_result in got_resp['execution_result'].items():
                self.assertTrue(test_result['success'], \
                        'testcase {} failure with message {}'.format(testcase, test_result['message']))