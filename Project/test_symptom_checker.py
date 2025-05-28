# test_symptom_checker.py

import unittest
from symptom_checker import find_possible_conditions


class TestSymptomChecker(unittest.TestCase):

    def test_known_symptoms(self):
        symptoms = ["fever", "cough"]
        conditions, unknowns = find_possible_conditions(symptoms)
        expected_conditions = {
            "flu",
            "common cold",
            "malaria",
            "bronchitis",
            "covid-19",
        }
        self.assertEqual(set(conditions), expected_conditions)
        self.assertEqual(unknowns, [])

    def test_unknown_symptoms(self):
        symptoms = ["tired", "blurred vision"]
        conditions, unknowns = find_possible_conditions(symptoms)
        self.assertEqual(conditions, set())
        self.assertEqual(unknowns, ["tired", "blurred vision"])

    def test_mixed_symptoms(self):
        symptoms = ["fever", "tired"]
        conditions, unknowns = find_possible_conditions(symptoms)
        self.assertIn("flu", conditions)
        self.assertIn("malaria", conditions)
        self.assertIn("common cold", conditions)
        self.assertIn("tired", unknowns)


if __name__ == "__main__":
    unittest.main()
