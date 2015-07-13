import unittest
from base_test_case import BaseTestCase
from compilation_builder.orchestrator import Orchestrator

class TestOrchestrator(BaseTestCase):

    @unittest.skip
    def testOrchestratorAcceptingInput(self):
        o = Orchestrator(self.packager_config)

        got_resp = o.dispatch_request(request)
        exp_resp = Response('Hello World!')


