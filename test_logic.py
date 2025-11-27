import unittest
from logic import (
    binary_search, check_eligibility, check_conflicts,
    bfs_unlock_path, parse_time
)

class TestLogic(unittest.TestCase):
    
    def test_binary_search_found(self):
        self.assertTrue(binary_search(["A", "B", "C", "D"], "C"))
    
    def test_binary_search_not_found(self):
        self.assertFalse(binary_search(["A", "B", "C", "D"], "E"))
    
    def test_check_eligibility_ok(self):
        is_eligible, missing = check_eligibility("COURSE1", ["A", "B", "C"], {"COURSE1": ["A", "B"]})
        self.assertTrue(is_eligible)
        self.assertEqual(missing, [])
    
    def test_check_eligibility_missing(self):
        is_eligible, missing = check_eligibility("COURSE1", ["A"], {"COURSE1": ["A", "B"]})
        self.assertFalse(is_eligible)
        self.assertIn("B", missing)
    
    def test_parse_time_simple(self):
        self.assertEqual(parse_time("SAT 1100-1400"), [('SAT', 1100, 1400)])
    
    def test_check_conflicts_none(self):
        sections = [
            {'Code': 'A', 'Section': '1', 'Time': 'M 800-1000'},
            {'Code': 'B', 'Section': '2', 'Time': 'M 1100-1300'}
        ]
        self.assertEqual(check_conflicts(sections), [])
    
    def test_check_conflicts_detected(self):
        sections = [
            {'Code': 'A', 'Section': '1', 'Time': 'M 800-1000'},
            {'Code': 'B', 'Section': '2', 'Time': 'M 930-1100'}
        ]
        self.assertEqual(len(check_conflicts(sections)), 1)
    
    def test_bfs_unlock(self):
        unlocked = bfs_unlock_path("A", {"A": [], "B": ["A"], "C": ["B"]})
        self.assertIn("B", unlocked)
        self.assertIn("C", unlocked)

if __name__ == "__main__":
    unittest.main()
    