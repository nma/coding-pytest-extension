import hashlib, os, unittest
from compilation_builder.python_packager import Packager
from test.base_test_case import BaseTestCase


class TestPythonCompilationOfCode(BaseTestCase):

    def test_can_create_unique_key(self):
        test_question_name = "test"
        exp_hash = hashlib.md5(test_question_name.encode('utf-8')).hexdigest()
        got_hash = Packager.generate_key(test_question_name)

        self.assertEqual(got_hash, exp_hash, "hash string not the same")

        #Packager.generate_key()

        #Packager.generate_key_with_versioning()

    @unittest.skip
    def test_concat_test_and_input(self):
        pass
        
    @unittest.skip
    def test_compile_and_execute_python_code(self):
        with open(self.get_file('expected'), 'r') as expected:
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

    @unittest.skip
    def test_compile_failure(self):
        with open('expected_compilation_error', 'r') as compilation_failure:
            try:
                compile(compilation_failure)
                self.assertFail('should not have compiled')
            except Exception:
                pass

if __name__ == '__main__':
    unittest.main()
