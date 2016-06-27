import docker
from compilation_builder.packager import PythonPackager, Packager
from compilation_builder.executor import DockerExecutor
from test.base_test_case import BaseTestCase
import unittest
import os


@unittest.skipIf(os.getenv("DOCKER_HOST") is None,
                 reason='No docker on machine')
class TestDockerExecutor(BaseTestCase):
    """run a test on the basic sandbox isolation offered by our executor"""

    def _make_bundle(self, code, test):
        p = PythonPackager(self.packager_config)
        bundle = p.bundle(self.test_question_name, code.read(), test.read())
        return bundle

    def setUp(self):
        super().setUp()
        self.test_question_name = 'testy'

    def test_simple_docker_command(self):
        docker_host = os.getenv("DOCKER_HOST")
        cli = docker.Client(base_url=docker_host)
        cli.pull(repository="python", tag="3.5")

    def test_run_isolated_environment(self):
        ex = DockerExecutor()
        with open(self.get_file('code'), 'r') as code, \
                open(self.get_file('tests'), 'r') as test:
            bundle = self._make_bundle(code, test)

            code_file = bundle.code_file_path
            test_file = bundle.test_file_path

            self.assertTrue(os.path.exists(code_file))
            self.assertTrue(os.path.exists(test_file))

            test_cases_dict = Packager.parse_testcases(bundle)
            _, test_io = next(iter(test_cases_dict.values()))
            ex.execute(code_file, test_io)

    def test_run_out_of_memory(self):
        pass
        #ex = DockerExecutor()
        #ex.execute()

    def test_run_out_of_execution_time(self):
        pass
        #ex = DockerExecutor()
        #ex.execute()
