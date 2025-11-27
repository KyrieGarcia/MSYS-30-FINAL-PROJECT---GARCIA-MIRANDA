import unittest
from logic import (
    binary_search, check_eligibility, check_conflicts,
    bfs_unlock_path, parse_time
)

class TestLogic(unittest.TestCase):
    
    def test_binary_search_found(self):
        sorted_list = ["A", "B", "C", "D"]
        self.assertTrue(binary_search(sorted_list, "C"))
    
    def test_binary_search_not_found(self):
        sorted_list = ["A", "B", "C", "D"]
        self.assertFalse(binary_search(sorted_list, "E"))
    
    def test_check_eligibility_ok(self):
        prereqs = {"COURSE1": ["A", "B"]}
        completed = ["A", "B", "C"]
        is_eligible, missing = check_eligibility("COURSE1", completed, prereqs)
        self.assertTrue(is_eligible)
        self.assertEqual(missing, [])
    
    def test_check_eligibility_missing(self):
        prereqs = {"COURSE1": ["A", "B"]}
        completed = ["A"]
        is_eligible, missing = check_eligibility("COURSE1", completed, prereqs)
        self.assertFalse(is_eligible)
        self.assertIn("B", missing)
    
    def test_parse_time_simple(self):
        result = parse_time("SAT 1100-1400")
        self.assertEqual(result, [('SAT', 1100, 1400)])
    
    def test_check_conflicts_none(self):
        sections = [
            {'Code': 'A', 'Section': '1', 'Time': 'M 800-1000'},
            {'Code': 'B', 'Section': '2', 'Time': 'M 1100-1300'}
        ]
        conflicts = check_conflicts(sections)
        self.assertEqual(conflicts, [])
    
    def test_check_conflicts_detected(self):
        sections = [
            {'Code': 'A', 'Section': '1', 'Time': 'M 800-1000'},
            {'Code': 'B', 'Section': '2', 'Time': 'M 930-1100'}
        ]
        conflicts = check_conflicts(sections)
        self.assertEqual(len(conflicts), 1)
    
    def test_bfs_unlock(self):
        prereqs = {
            "A": [],
            "B": ["A"],
            "C": ["B"]
        }
        unlocked = bfs_unlock_path("A", prereqs)
        self.assertIn("B", unlocked)
        self.assertIn("C", unlocked)

if __name__ == "__main__":
    unittest.main()
