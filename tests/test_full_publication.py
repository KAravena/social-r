"""Full Course Publication Test Suite — Social R

Validates that all 13 modules and 89 exercises are published and fully integrated.
"""
from tests.test_partial_publication import TestFullPublication

__all__ = ["TestFullPublication"]

if __name__ == "__main__":
    import unittest
    unittest.main()
