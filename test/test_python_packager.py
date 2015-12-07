import hashlib, os, unittest, yaml
from compilation_builder.packager import Packager, PythonPackager
from test.base_test_case import BaseTestCase
from compilation_builder.executor import Executor


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

            with open(test_file, 'r') as test_out, open(self.get_file('expected_test_str'), 'r') as expected_test, \
                 open(code_file, 'r') as code_out, open(self.get_file('expected_code_str'), 'r') as expected_code:
                
                # cache it to use later
                # TODO: if we .read() it again, it doesn't get the same data? (why?)
                expected_test_str = expected_test.read()
                
                self.assertEqual(test_out.read(), expected_test_str)
                self.assertEqual(code_out.read(), expected_code.read())

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
        test_question_name = "foo_compile_fail"
        with open(self.get_file('compilation_error'), 'r') as code, open(self.get_file('tests'), 'r') as test:
            p = PythonPackager(self.packager_config)
            bundle = p.bundle(test_question_name, code.read(), test.read())

            got_test_output = p.execute(bundle)

            for testcase, test_case_result in got_test_output.items():
                self.assertFalse(test_case_result['success'])
                self.assertIsNotNone(test_case_result['message'])

    def test_test_case_failure(self):
        test_question_name = "foo_test_fail"
        with open(self.get_file('code'), 'r') as code, open(self.get_file('failing_tests'), 'r') as test:
            p = PythonPackager(self.packager_config)
            bundle = p.bundle(test_question_name, code.read(), test.read())

            got_test_output = p.execute(bundle)
            exp_test_output = {
                    "testFail": {"success": False, "message": "Got Output: 6\nExpected Output: 2\n"}
            }

            self.assertEqual(got_test_output, exp_test_output)
