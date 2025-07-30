from random import choice, randint, random
import pygame as pg
import time

SCREEN_SIZE = (640, 480)
GRID_SIZE = 20
GRID_WIDTH = SCREEN_SIZE[0] // GRID_SIZE
GRID_HEIGHT = SCREEN_SIZE[1] // GRID_SIZE
STARTING_POSITION = (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2)

DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}

COLORS = {
    'background': (0, 0, 0),
    'border': (93, 216, 228),
    'apple': (255, 0, 0),
    'golden_apple': (255, 215, 0),
    'snake': (0, 255, 0),
    'text': (255, 255, 255)
}


class GameObject:
    """Base class for all game objects."""

    def __init__(self, position=STARTING_POSITION):
        self.position = position

    def draw(self):
        raise NotImplementedError("Subclasses must implement draw()")


class Apple(GameObject):
    """Regular apple that snake needs to collect."""

    def __init__(self):
        super().__init__()
        self.randomize_position([])

    def randomize_position(self, occupied_positions):
        """Find random unoccupied position."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, COLORS['apple'], rect)
        pg.draw.rect(screen, COLORS['border'], rect, 1)


class GoldenApple(GameObject):
    """
    Special golden apple that
    gives 3 points and disappears after 6 seconds.
    """

    def __init__(self):
        super().__init__()
        self.spawn_time = 0
        self.active = False
        self.blink_state = False
        self.blink_timer = 0
        self.position = (-GRID_SIZE, -GRID_SIZE)

    def spawn(self, occupied_positions):
        """Spawn golden apple at random position."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break
        self.spawn_time = time.time()
        self.active = True
        self.blink_state = False
        self.blink_timer = 0

    def update(self):
        """Update apple state and check if it should disappear."""
        if not self.active:
            return

        current_time = time.time()
        elapsed = current_time - self.spawn_time

        if elapsed > 4:
            self.blink_timer += 1
            if self.blink_timer >= 5:
                self.blink_state = not self.blink_state
                self.blink_timer = 0

        if elapsed > 6:
            self.active = False
            self.position = (-GRID_SIZE, -GRID_SIZE)

    def draw(self):
        if not self.active:
            return

        if self.blink_state and (time.time() - self.spawn_time) > 4:
            return

        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, COLORS['golden_apple'], rect)
        pg.draw.rect(screen, COLORS['border'], rect, 1)


def draw_text(surface, text, size, x, y, color=COLORS['text']):
    font = pg.font.SysFont('arial', size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))
    surface.blit(text_surface, text_rect)


class Snake(GameObject):
    """The player-controlled snake."""

    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.positions = [self.position]
        self.direction = choice(list(DIRECTIONS.values()))
        self.next_direction = None
        self.length = 1
        self.score = 0
        self.start_time = time.time()
        self.end_time = None
        self.game_over = False
        self.victory = False

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * GRID_SIZE) % SCREEN_SIZE[0]
        new_y = (head_y + dir_y * GRID_SIZE) % SCREEN_SIZE[1]
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, COLORS['snake'], rect)
            pg.draw.rect(screen, COLORS['border'], rect, 1)

    def get_elapsed_time(self):
        if self.end_time is not None:
            return int(self.end_time - self.start_time)
        return int(time.time() - self.start_time)


def handle_keys(snake):
    """Process keyboard input."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            return False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DIRECTIONS['DOWN']:
                snake.next_direction = DIRECTIONS['UP']
            elif event.key == pg.K_DOWN \
                    and snake.direction != DIRECTIONS['UP']:
                snake.next_direction = DIRECTIONS['DOWN']
            elif event.key == pg.K_LEFT \
                    and snake.direction != DIRECTIONS['RIGHT']:
                snake.next_direction = DIRECTIONS['LEFT']
            elif event.key == pg.K_RIGHT and \
                    snake.direction != DIRECTIONS['LEFT']:
                snake.next_direction = DIRECTIONS['RIGHT']
            elif event.key == pg.K_r and (snake.game_over or snake.victory):
                snake.reset()
    return True


def main():
    """Main game loop."""
    pg.init()
    global screen
    screen = pg.display.set_mode(SCREEN_SIZE)
    pg.display.set_caption('Змейка')
    clock = pg.time.Clock()

    snake = Snake()
    apple = Apple()
    golden_apple = GoldenApple()
    last_golden_spawn = 0
    golden_spawn_interval = 15

    running = True
    while running:
        clock.tick(20)

        running = handle_keys(snake)

        current_time = time.time()

        if (not snake.game_over and not golden_apple.active
            and current_time - last_golden_spawn > golden_spawn_interval
                and random() < 0.1):
            golden_apple.spawn(snake.positions + [apple.position])
            last_golden_spawn = current_time

        golden_apple.update()

        if not snake.game_over and not snake.victory:
            snake.update_direction()
            snake.move()

            if snake.positions[0] == apple.position:
                snake.length += 1
                snake.score += 1
                apple.randomize_position(snake.positions)

            if golden_apple.active \
                    and snake.positions[0] == golden_apple.position:
                snake.length += 3
                snake.score += 3
                golden_apple.active = False
                golden_apple.position = (-GRID_SIZE, -GRID_SIZE)

            if len(snake.positions) == GRID_WIDTH * GRID_HEIGHT:
                snake.victory = True
                snake.game_over = True
                snake.end_time = time.time()

            if snake.positions[0] in snake.positions[1:]:
                snake.game_over = True
                snake.end_time = time.time()

        screen.fill(COLORS['background'])
        snake.draw()
        apple.draw()
        golden_apple.draw()

        elapsed_time = snake.get_elapsed_time()
        draw_text(screen, f'Apples: {snake.score}', 20, 10, 10)
        draw_text(screen, f'Time: {elapsed_time}s', 20, 10, 40)

        if golden_apple.active:
            remaining_time = 6 - (time.time() - golden_apple.spawn_time)
            if remaining_time > 0:
                draw_text(
                    screen, f'Golden: {int(remaining_time)}s', 20, 10, 70
                )

        if snake.game_over:
            if snake.victory:
                message = [
                    'Congratulations! You passed the game!',
                    f'Apples: {snake.score}',
                    f'Time: {elapsed_time} seconds'
                ]
                color = COLORS['snake']
            else:
                message = [
                    'Game over, try again!',
                    f'Apples: {snake.score}',
                    f'Time: {elapsed_time} seconds'
                ]
                color = COLORS['apple']

            for i, line in enumerate(message):
                draw_text(
                    screen, line, 30,
                    SCREEN_SIZE[0] // 2 - 250,
                    SCREEN_SIZE[1] // 2 - 40 + i * 40, color
                )

            draw_text(
                screen, 'Press R to restart', 20,
                SCREEN_SIZE[0] // 2 - 100,
                SCREEN_SIZE[1] // 2 + 80
            )

        pg.display.update()


if __name__ == '__main__':
    main()
