import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from risk_logic import calculate_overall_likelihood, calculate_risk

class TestRiskLogic(unittest.TestCase):
    def test_overall_likelihood(self):
        # Test cases based on the matrix implementation
        # Low (2) x Low (2) -> Low (2)
        self.assertEqual(calculate_overall_likelihood(2, 2), 2)
        
        # High (4) x High (4) -> High (4)
        self.assertEqual(calculate_overall_likelihood(4, 4), 4)
        
        # Very High (5) x Very High (5) -> Very High (5)
        self.assertEqual(calculate_overall_likelihood(5, 5), 5)
        
        # Low (2) x High (4) -> Moderate (3)
        self.assertEqual(calculate_overall_likelihood(2, 4), 3)

    def test_risk_calculation(self):
        # Test cases based on the matrix implementation
        # Low Likelihood (2) x Low Impact (2) -> Low Risk (2)
        self.assertEqual(calculate_risk(2, 2), 2)
        
        # High Likelihood (4) x High Impact (4) -> High Risk (4)
        self.assertEqual(calculate_risk(4, 4), 4)
        
        # Moderate Likelihood (3) x High Impact (4) -> Moderate Risk (3)
        self.assertEqual(calculate_risk(3, 4), 3)

if __name__ == '__main__':
    unittest.main()
