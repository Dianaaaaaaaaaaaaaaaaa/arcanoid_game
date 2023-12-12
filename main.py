import pygame
import sys
import os

# Определение цветов
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Класс-фасад для управления уровнями и рекордами
class LevelFacade:
    def __init__(self, level_file, high_scores_file):
        # Загрузка данных уровня и создание кирпичей при инициализации
        self.level_data = self.load_level(level_file)
        self.bricks = self.create_bricks()
        self.high_scores_file = high_scores_file
        self.high_scores = self.load_high_scores()

    # Загрузка данных уровня из файла
    def load_level(self, level_file):
        with open(level_file, 'r') as file:
            lines = file.readlines()
        return [list(line.strip()) for line in lines]

    # Создание списка кирпичей на основе данных уровня
    def create_bricks(self):
        bricks = []
        brick_width = 60
        brick_height = 20
        for row_index, row in enumerate(self.level_data):
            for col_index, brick_type in enumerate(row):
                if brick_type == '1':
                    brick = pygame.Rect(col_index * brick_width, row_index * brick_height, brick_width, brick_height)
                    bricks.append(brick)
        return bricks

    # Загрузка таблицы рекордов из файла
    def load_high_scores(self):
        try:
            with open(self.high_scores_file, 'r') as file:
                high_scores = [tuple(line.strip().split(',')) for line in file.readlines()]
            return high_scores
        except FileNotFoundError:
            return []

    # Сохранение таблицы рекордов в файл
    def save_high_scores(self):
        with open(self.high_scores_file, 'w') as file:
            for name, score in self.high_scores:
                file.write(f"{name},{score}\n")

    # Обновление таблицы рекордов с новым результатом игрока
    def update_high_scores(self, player_name, player_score):
        self.high_scores.append((player_name, player_score))
        self.high_scores.sort(key=lambda x: int(x[1]), reverse=True)
        self.high_scores = self.high_scores[:5]  # Ограничиваем таблицу рекордов пятью записями
        self.save_high_scores()

# Класс для игры Arkanoid
class ArkanoidGame:
    def __init__(self, level_files, high_scores_file):
        # Инициализация Pygame и создание окна
        pygame.init()
        self.level_files = level_files
        self.current_level = 0
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Arkanoid")

        # Создание часов, уровня, мяча, платформы, шрифта и счетчика
        self.clock = pygame.time.Clock()
        # self.level = LevelFacade(current_level, high_scores_file)
        self.ball = pygame.Rect(400, 300, 20, 20)
        self.ball_speed = [5, 5]

        self.paddle = pygame.Rect(350, 550, 100, 15)
        self.paddle_speed = 10

        self.font = pygame.font.Font(None, 36)
        self.player_score = 0

        # Инициализация звука
        # pygame.mixer.init()
        # pygame.mixer.music.load('background.mp3') 
        # pygame.mixer.music.play(-1)  # Зацикливаем воспроизведение

    # Выбор уровня
    def show_level_selection(self):
        selected_level = None
        while selected_level is None:
            self.handle_events()
            self.screen.fill((0, 0, 0))

            font = pygame.font.Font(None, 36)
            text = font.render("Select Level", True, WHITE)
            text_rect = text.get_rect(center=(400, 100))
            self.screen.blit(text, text_rect)

            for i, level_file in enumerate(self.level_files):
                button_rect = pygame.Rect(300, 200 + i * 50, 200, 40)
                pygame.draw.rect(self.screen, GREEN, button_rect)
                font = pygame.font.Font(None, 32)
                text = font.render(f"Level {i + 1}", True, WHITE)
                text_rect = text.get_rect(center=button_rect.center)
                self.screen.blit(text, text_rect)

                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.screen, BLUE, button_rect, 2)
                    if pygame.mouse.get_pressed()[0]:
                        selected_level = i

            pygame.display.flip()
            self.clock.tick(30)

        self.current_level = selected_level


    # Обработка событий
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # Движение платформы
    def move_paddle(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.paddle.left > 0:
            self.paddle.x -= self.paddle_speed
        if keys[pygame.K_RIGHT] and self.paddle.right < 800:
            self.paddle.x += self.paddle_speed

    # Движение мяча и обработка столкновений
    def move_ball(self):
        self.ball.x += self.ball_speed[0]
        self.ball.y += self.ball_speed[1]

        # Отскок от стен
        if self.ball.left < 0 or self.ball.right > 800:
            self.ball_speed[0] = -self.ball_speed[0]
        if self.ball.top < 0:
            self.ball_speed[1] = -self.ball_speed[1]

        # Отскок от платформы
        if self.ball.colliderect(self.paddle):
            self.ball_speed[1] = -self.ball_speed[1]


        # Отскок от кирпичей и обновление счета
        for brick in self.level.bricks:
            if self.ball.colliderect(brick):
                self.ball_speed[1] = -self.ball_speed[1]
                self.level.bricks.remove(brick)
                if not self.level.bricks:  # Проверяем, выбиты ли все блоки
                    self.display_you_win()  # Выводим сообщение "You Win"
                    player_name = self.get_player_name()  # Получаем имя игрока
                    self.level.update_high_scores(player_name, self.player_score)  # Записываем результат в таблицу рекордов
                else:
                    self.player_score += 10  # Увеличиваем счет игрока при выбивании блока
                break

    # Отрисовка игровых объектов
    def draw_game_objects(self):
        self.screen.fill((0, 0, 0))

        pygame.draw.ellipse(self.screen, WHITE, self.ball)
        pygame.draw.rect(self.screen, WHITE, self.paddle)

        for brick in self.level.bricks:
            pygame.draw.rect(self.screen, BLUE, brick)

        # Вывод счета игрока
        score_text = self.font.render(f"Score: {self.player_score}", True, WHITE)
        self.screen.blit(score_text, (10, 10)) # Вывод счета игрока в левом верхнем углу

        pygame.display.flip() # Обновление экрана

    # Вывод экрана "Game Over"
    def display_game_over(self):
        font = pygame.font.Font(None, 74)
        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Задержка перед выходом из игры

    # Получение имени игрока
    def get_player_name(self):
        input_box = pygame.Rect(300, 200, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        font = pygame.font.Font(None, 32)
        clock = pygame.time.Clock()
        input_rect = pygame.Rect(300, 250, 140, 32)

        while True:
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            return text
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_rect.w = width
            self.screen.fill((30, 30, 30), (300, 250, width, 32))
            self.screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))
            pygame.draw.rect(self.screen, color, input_rect, 2)

            pygame.display.flip()
            clock.tick(30)

    # Вывод экрана "You Win"
    def display_you_win(self):
        font = pygame.font.Font(None, 74)
        text = font.render("You Win!", True, WHITE)
        text_rect = text.get_rect(center=(400, 300))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Задержка перед выходом из игры


    def run(self):
        player_name = self.get_player_name()
        self.show_level_selection()  # Показываем экран выбора уровней
        self.level = LevelFacade(self.level_files[self.current_level], high_scores_file_path)

        game_over = False
        while not game_over:
            self.handle_events()
            self.move_paddle()
            self.move_ball()
            self.draw_game_objects()
            if len(self.level.bricks) == 0:
                game_over = True
                self.display_you_win()
                self.level.update_high_scores(player_name, self.player_score)
            if self.ball.bottom > 600:
                game_over = True
                self.display_game_over()
                self.level.update_high_scores(player_name, self.player_score)

            self.clock.tick(60)

if __name__ == '__main__':
    level_files = ['level.txt', 'level2.txt', 'level3.txt']
    high_scores_file_path = 'high_scores.txt'
    ArkanoidGame(level_files, high_scores_file_path).run()