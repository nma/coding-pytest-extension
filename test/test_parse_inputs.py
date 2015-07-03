import unittest
from python_packager import Packager

class TestPythonCompilationOfCode(unittest.TestCase):
    
    def test_concat_test_and_input(self):
        with open('code', 'r') as code, open('tests', 'r') as tests, open('expected', 'r') as expected:
            p = Packager()
            complete_code_snippet = p.bundle(code.readlines(), tests.readlines())
            self.assertEqual(complete_code_snippet, expected)

    def test_compile_and_execute_python_code(self):
        with open('expected', 'r') as expected:
            code = compile(expected)
            namespace = {}
            '''
            Why should you do that? 
            Cleaner for starters, also because exec without a dictionary has to hack around some implementation details 
            in the interpreter. We will cover that later. 
            
            For the moment: if you want to use exec and you plan on executing that code more than once, 
            make sure you compile it into bytecode first and then execute that bytecode only and only in a 
            new dictionary as namespace.
            '''
            # execute the compiled python code 
            exec(code) in namespace
            print(namespace)

    def test_compile_failure(self):
        with open('expected_compilation_error', 'r') as compilation_failure:
            try:
                compile(compilation_failure)
                self.assertFail('should not have compiled')
            except Exception:
                pass


if __name__ == '__main__':
    unittest.main()
