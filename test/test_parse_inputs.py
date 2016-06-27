import hashlib
import unittest
from compilation_builder.packager import Packager


class TestStaticMethods(unittest.TestCase):
    """Static methods don't need to import configs and make directories,
    so we skip it for these kind of tests.
    """

    def test_can_create_unique_key(self):
        test_question_name = "test"
        exp_hash = hashlib.md5(test_question_name.encode('utf-8')).hexdigest()
        got_hash = Packager.generate_key(test_question_name)

        self.assertEqual(got_hash, exp_hash, "hash string not the same")

        exp_hash2 = hashlib.md5(str(test_question_name + "_1").encode('utf-8')
                                ).hexdigest()
        got_hash2 = Packager.generate_key_with_versioning(
            test_question_name, 1)

        self.assertEqual(got_hash2, exp_hash2, "hash string not the same")
        self.assertNotEqual(got_hash2, exp_hash,
                            "versioned hash string should be" +
                            " different from default hash string")
