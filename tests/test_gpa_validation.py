import unittest
import pandas as pd
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.gpa_calculator import GpaCalculator

class TestGpaValidation(unittest.TestCase):
    def setUp(self):
        self.policy = {
            "school": "Test School",
            "gpa_policy_version": "1.0",
            "grade_scale": {"A": 4.0, "B": 3.0},
            "grade_selection": {
                "use_columns": ["grade1", "grade2"],
                "ignore_values": [None]
            },
            "calculation": {
                "rounding": {"precision": 2}
            }
        }
        self.tmp_dir = "tmp_policies"

    def test_missing_columns_raises_error(self):
        df = pd.DataFrame([{"credits": 1.0, "grade1": "A"}])
        # "grade2" is missing from columns
        calc = GpaCalculator(df, self.tmp_dir)
        with self.assertRaisesRegex(KeyError, "Missing grade columns"):
            calc.calculate_gpa(self.policy)

    def test_multiple_semester_grades_raises_error(self):
        df = pd.DataFrame([
            {"credits": 1.0, "grade1": "A", "grade2": "B"} # Both present
        ])
        calc = GpaCalculator(df, self.tmp_dir)
        with self.assertRaisesRegex(ValueError, "Row contains multiple semester grades"):
            calc.calculate_gpa(self.policy)

    def test_nan_values_ignored_safely(self):
        df = pd.DataFrame([
            {"credits": 1.0, "grade1": float('nan'), "grade2": "B"}, # NaN should be ignored
            {"credits": 1.0, "grade1": None, "grade2": "A"} # None should be ignored
        ])
        calc = GpaCalculator(df, self.tmp_dir)
        result = calc.calculate_gpa(self.policy)
        
        # (3.0 * 1.0 + 4.0 * 1.0) / 2.0 = 3.5
        self.assertEqual(result["gpa"], 3.5)
        self.assertEqual(result["semester_grades_counted"], 2)

if __name__ == '__main__':
    unittest.main()
