import unittest
from pathlib import Path

from tools.verify import validate_repo


class RepositoryQualificationTest(unittest.TestCase):
    def test_exact_repository_contract(self):
        self.assertEqual(validate_repo(Path(".")), [])


if __name__ == "__main__":
    unittest.main()
