import unittest
import excalibur

class TestMisc(unittest.TestCase):
    def test_merge_dicts(self):
        merged_dict = excalibur.merge_dicts({"a":123}, {"b":123}, {"c":123})
        assert merged_dict == {"a":123, "b":123, "c":123}



