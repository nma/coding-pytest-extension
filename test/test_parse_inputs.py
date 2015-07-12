import hashlib, os, unittest, yaml
from compilation_builder.python_packager import Packager, PythonPackager
from test.base_test_case import BaseTestCase


class TestStaticMethods(unittest.TestCase):
    """Static methods don't need to import configs and make directories, so we skip it for these kind of tests.
    """
    def test_can_create_unique_key(self):
        test_question_name = "test"
        exp_hash = hashlib.md5(test_question_name.encode('utf-8')).hexdigest()
        got_hash = Packager.generate_key(test_question_name)

        self.assertEqual(got_hash, exp_hash, "hash string not the same")

        exp_hash2 = hashlib.md5(str(test_question_name + "_1").encode('utf-8')).hexdigest()
        got_hash2 = Packager.generate_key_with_versioning(test_question_name, 1)

        self.assertEqual(got_hash2, exp_hash2, "hash string not the same")
        self.assertNotEqual(got_hash2, exp_hash, "versioned hash string should be different from default hash string")


class TestPythonCompilationOfCode(BaseTestCase):

    def test_bundle_code_and_test_then_execute(self):
        #uncomment this to let unittest print unlimited stacktraces
        #self.maxDiff = None
        test_question_name = "foo"
        with open(self.get_file('code'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            p = PythonPackager(self.packager_config)
            bundle = p.bundle(test_question_name, code.read(), test.read())
            
            code_file = bundle.code_file_path 
            test_file = bundle.test_file_path
 
            self.assertTrue(os.path.exists(code_file))
            self.assertTrue(os.path.exists(test_file)) 

            with open(test_file, 'r') as test, open(self.get_file('expected_test_str'), 'r') as expected_test, \
                 open(code_file, 'r') as code, open(self.get_file('expected_code_str'), 'r') as expected_code:
                
                # cache it to use later
                # TODO: if we .read() it again, it doesn't get the same data? (why?)
                expected_test_str = expected_test.read()
                
                self.assertEqual(test.read(), expected_test_str)
                self.assertEqual(code.read(), expected_code.read())

                exp_test_cases = yaml.load(expected_test_str)
                got_test_cases = Packager.parse_testcases(bundle)                

                self.assertEqual(got_test_cases, exp_test_cases) 

            got_test_output = p.execute(bundle)
            exp_test_output = {
                    "testSimple": {"success": True, "message": None},
                    "testMultiSimple": {"success": True, "message": None}
            }

            self.assertEqual(got_test_output, exp_test_output)

    def test_compile_failure(self):
        self.maxDiff = None
        test_question_name = "foo_fail"
        with open(self.get_file('compilation_error'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            p = PythonPackager(self.packager_config)
            bundle = p.bundle(test_question_name, code.read(), test.read())

            compile_error_keywords = ["Traceback", "builtin_function_or_method", "TypeError", "int()"]

            got_test_output = p.execute(bundle)
            exp_test_output = {
                    "testSimple": {"success": False, "message": compile_error_keywords},
                    "testMultiSimple": {"success": False, "message": compile_error_keywords}
            }
            
            for testcase, test_case_result in got_test_output.items():
                got_test_case_message = test_case_result['message']

                self.assertFalse(test_case_result['success'])
                self.assertIsNotNone(test_case_result['message'])

                exp_key_words = exp_test_output[testcase]['message']
                for word in exp_key_words:
                    self.assertTrue(word in got_test_case_message) 

    @unittest.skip
    def test_test_case_failure(self):
        pass

