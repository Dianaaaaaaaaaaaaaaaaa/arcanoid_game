import unittest
from unittest.mock import patch
from io import StringIO
from main import LevelFacade

class LevelFacadeRefactoring(unittest.TestCase):

    def setUp(self):
        self.level_facade = LevelFacade('test_level.txt', 'test_high_scores.txt')

    @patch('builtins.open')
    def test_load_level(self, mock_open):
        mock_open.return_value.__enter__.return_value = StringIO('101\n010\n111\n')
        level_data = self.level_facade.load_level('test_level.txt')
        expected_data = [['1', '0', '1'], ['0', '1', '0'], ['1', '1', '1']]
        self.assertEqual(level_data, expected_data)

    @patch('builtins.open')
    def test_create_bricks(self, mock_open):
        self.level_facade.level_data = [['1', '0', '1'], ['0', '1', '0'], ['1', '1', '1']]
        bricks = self.level_facade.create_bricks()
        self.assertEqual(len(bricks), 6)

    @patch('builtins.open')
    def test_load_high_scores(self, mock_open):
        mock_open.return_value.__enter__.return_value = StringIO('Alice,100\nBob,80\n')
        high_scores = self.level_facade.load_high_scores()
        expected_scores = [('Alice', '100'), ('Bob', '80')]
        self.assertEqual(high_scores, expected_scores)

    @patch('builtins.open')
    def test_update_high_scores(self, mock_open):
        self.level_facade.high_scores = [('Alice', 100), ('Bob', 80)]
        self.level_facade.update_high_scores('Charlie', 120)
        expected_scores = [('Charlie', 120), ('Alice', 100), ('Bob', 80)]
        self.assertEqual(self.level_facade.high_scores, expected_scores)


if __name__ == '__main__':
    unittest.main()
