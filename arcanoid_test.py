import unittest
from unittest.mock import patch
from main import LevelFacade

class TestLevelFacade(unittest.TestCase):

    def setUp(self):
        # Здесь вы можете инициализировать необходимые объекты или переменные перед каждым тестом
        pass

    def tearDown(self):
        # Здесь вы можете выполнять необходимые завершающие действия после каждого теста
        pass

    def test_load_level(self):
        # Тест загрузки уровня
        level_facade = LevelFacade('test_level.txt', 'test_high_scores.txt')
        level_data = level_facade.load_level('test_level.txt')
        expected_data = [['1', '0', '1'], ['0', '1', '0'], ['1', '1', '1']]
        self.assertEqual(level_data, expected_data)

    def test_create_bricks(self):
        # Тест создания кирпичей
        level_facade = LevelFacade('test_level.txt', 'test_high_scores.txt')
        level_facade.level_data = [['1', '0', '1'], ['0', '1', '0'], ['1', '1', '1']]
        bricks = level_facade.create_bricks()
        self.assertEqual(len(bricks), 6)  # Проверка, что количество кирпичей соответствует ожидаемому

    def test_load_high_scores(self):
        # Тест загрузки таблицы рекордов
        level_facade = LevelFacade('test_level.txt', 'test_high_scores.txt')
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = ['Alice,100\n', 'Bob,80\n']
            high_scores = level_facade.load_high_scores()
            expected_scores = [('Alice', '100'), ('Bob', '80')]
            self.assertEqual(high_scores, expected_scores)

    def test_update_high_scores(self):
        # Тест обновления таблицы рекордов
        level_facade = LevelFacade('test_level.txt', 'test_high_scores.txt')
        level_facade.high_scores = [('Alice', 100), ('Bob', 80)]
        level_facade.update_high_scores('Charlie', 120)
        expected_scores = [('Charlie', 120), ('Alice', 100), ('Bob', 80)]
        self.assertEqual(level_facade.high_scores, expected_scores)

if __name__ == '__main__':
    unittest.main()
