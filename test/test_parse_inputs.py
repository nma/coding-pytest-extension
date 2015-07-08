import hashlib, os, unittest
from compilation_builder.python_packager import Packager, PythonPackager
from test.base_test_case import BaseTestCase


class TestPythonCompilationOfCode(BaseTestCase):

    def test_can_create_unique_key(self):
        test_question_name = "test"
        exp_hash = hashlib.md5(test_question_name.encode('utf-8')).hexdigest()
        got_hash = Packager.generate_key(test_question_name)

        self.assertEqual(got_hash, exp_hash, "hash string not the same")

        exp_hash2 = hashlib.md5(str(test_question_name + "_1").encode('utf-8')).hexdigest()
        got_hash2 = Packager.generate_key_with_versioning(test_question_name, 1)

        self.assertEqual(got_hash2, exp_hash2, "hash string not the same")
        self.assertNotEqual(got_hash2, exp_hash, "versioned hash string should be different from default hash string")

    def test_bundle_code_and_test(self):
        test_question_name = "foo"
        with open(self.get_file('code'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            p = PythonPackager(self.packager_config)
            key = p.bundle(test_question_name, code.read(), test.read())
            
            code_file = os.path.join(self.packager_config.get_code_folder(), key)
            test_file = os.path.join(self.packager_config.get_test_folder(), key)
 
            self.assertTrue(os.path.exists(code_file))
            self.assertTrue(os.path.exists(test_file)) 

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
