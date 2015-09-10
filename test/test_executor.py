from compilation_builder.executor import SandboxedExecutor
import unittest

class TestExecutorSandbox(unittest.TestCase):
    """run a test on the basic sandbox isolation offered by our executor
    """
    def test_run_isolated_environment(self):
        ex = SandboxedExecutor()
        pass

    def test_run_out_of_memory(self):
        ex = SandboxedExecutor()
        pass

    def test_run_out_of_execution_time(self):
        ex = SandboxedExecutor()
        pass
