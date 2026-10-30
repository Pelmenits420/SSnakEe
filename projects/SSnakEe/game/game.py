"""SsnakEe loģika. Šeit NAV pygame atkarību."""

import random

from game.constants import (
    FOOD_POINTS, SECOND_POINTS, MULTI_FOOD_COUNT,
    DIFFICULTY_INTERVAL, DIFFICULTY_FACTOR, MIN_MOVE_INTERVAL,
    MAGNET_CHECK_EVERY, MAGNET_MIN_ELAPSED, MAGNET_SPAWN_CHANCE,
    MAGNET_MAX_PER_GAME, MAGNET_LIFETIME,
    SPEED_OPTIONS,
    P1_BODY, P1_HEAD, P2_BODY, P2_HEAD,
)


class Snake:
    """Viens spēlētājs."""

    def __init__(self, start_x, start_y, direction, name, body_color, head_color):
        self.name = name
        self.body_color = body_color
        self.head_color = head_color
        self.direction = direction
        self.body = [
            (start_x, start_y),
            (start_x - direction[0], start_y - direction[1]),
            (start_x - 2 * direction[0], start_y - 2 * direction[1]),
        ]
        self.next_directions = []
        self.alive = True
        self.score = 0
        self.pending_growth = 0

    @property
    def head(self):
        return self.body[0]

    def change_direction(self, new_dir):
        if not self.alive:
            return
        last = self.next_directions[-1] if self.next_directions else self.direction
        if new_dir == (-last[0], -last[1]):
            return
        if new_dir == last:
            return
        if len(self.next_directions) < 2:
            self.next_directions.append(new_dir)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Magnet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.time_alive = 0.0


class Game:
    """Visu noteikumu pārvaldnieks."""

    def __init__(self, grid_size, multi_food, speed_index, player_count=1):
        self.grid_size = grid_size
        self.multi_food = multi_food
        self.speed_index = speed_index
        self.player_count = player_count
        self.base_interval = SPEED_OPTIONS[speed_index][1]
        self.reset()

    def reset(self):
        cx = self.grid_size // 2
        cy = self.grid_size // 2

        if self.player_count == 1:
            p1 = Snake(cx, cy, (1, 0), "P1", P1_BODY, P1_HEAD)
            self.snakes = [p1]
        else:
            p1x = max(3, self.grid_size // 4)
            p2x = min(self.grid_size - 4, 3 * self.grid_size // 4)
            p1 = Snake(p1x, cy, (1, 0), "P1", P1_BODY, P1_HEAD)
            p2 = Snake(p2x, cy, (-1, 0), "P2", P2_BODY, P2_HEAD)
            self.snakes = [p1, p2]

        self.foods = []
        self.magnets = []
        self.elapsed = 0.0
        self.difficulty_timer = 0.0
        self.score_timer = 0.0
        self.move_timer = 0.0
        self.magnet_check_timer = 0.0
        self.magnet_spawns = 0
        self.current_interval = self.base_interval
        self.game_over = False
        self.winner = None
        self.won_by_fill = False

        self._maintain_food()

    def level(self):
        return 1 + int(self.elapsed // DIFFICULTY_INTERVAL)

    def _max_food(self):
        return MULTI_FOOD_COUNT if self.multi_food else 1

    def _is_occupied(self, x, y):
        for s in self.snakes:
            if (x, y) in s.body:
                return True
        for f in self.foods:
            if f.x == x and f.y == y:
                return True
        for m in self.magnets:
            if m.x == x and m.y == y:
                return True
        return False

    def _random_cell(self):
        cells = [
            (x, y)
            for x in range(self.grid_size)
            for y in range(self.grid_size)
            if not self._is_occupied(x, y)
        ]
        return random.choice(cells) if cells else None

    def _maintain_food(self):
        while len(self.foods) < self._max_food():
            pos = self._random_cell()
            if pos is None:
                break
            self.foods.append(Food(pos[0], pos[1]))

    def set_direction(self, player_index, direction):
        if player_index < len(self.snakes):
            self.snakes[player_index].change_direction(direction)

    def update(self, dt):
        if self.game_over:
            return

        self.elapsed += dt

        self.score_timer += dt
        while self.score_timer >= 1.0:
            self.score_timer -= 1.0
            for s in self.snakes:
                if s.alive:
                    s.score += SECOND_POINTS

        self.difficulty_timer += dt
        if self.difficulty_timer >= DIFFICULTY_INTERVAL:
            self.difficulty_timer -= DIFFICULTY_INTERVAL
            self.current_interval = max(
                MIN_MOVE_INTERVAL,
                self.current_interval * DIFFICULTY_FACTOR,
            )

        for m in list(self.magnets):
            m.time_alive += dt
            if m.time_alive >= MAGNET_LIFETIME:
                self.magnets.remove(m)

        self.magnet_check_timer += dt
        if self.magnet_check_timer >= MAGNET_CHECK_EVERY:
            self.magnet_check_timer = 0.0
            self._try_spawn_magnet()

        self.move_timer += dt
        steps = 0
        while self.move_timer >= self.current_interval and steps < 3:
            self.move_timer -= self.current_interval
            if not self._step():
                break
            steps += 1

    def _try_spawn_magnet(self):
        if not self.multi_food:
            return
        if self.magnet_spawns >= MAGNET_MAX_PER_GAME:
            return
        if self.elapsed < MAGNET_MIN_ELAPSED:
            return
        if self.magnets:
            return
        if random.random() > MAGNET_SPAWN_CHANCE:
            return
        pos = self._random_cell()
        if pos:
            self.magnets.append(Magnet(pos[0], pos[1]))
            self.magnet_spawns += 1

    def _step(self):
        for s in self.snakes:
            if s.alive and s.next_directions:
                s.direction = s.next_directions.pop(0)

        new_heads = {}
        for s in self.snakes:
            if not s.alive:
                continue
            hx, hy = s.head
            dx, dy = s.direction
            new_heads[s.name] = (hx + dx, hy + dy)

        for s in self.snakes:
            if not s.alive:
                continue
            nx, ny = new_heads[s.name]
            if not (0 <= nx < self.grid_size and 0 <= ny < self.grid_size):
                s.alive = False

        pos_map = {}
        for s in self.snakes:
            if not s.alive:
                continue
            pos = new_heads[s.name]
            if pos in pos_map:
                other = pos_map[pos]
                s.alive = False
                other.alive = False
            else:
                pos_map[pos] = s

        for s in self.snakes:
            if not s.alive:
                continue
            nx, ny = new_heads[s.name]
            for other in self.snakes:
                if not other.alive:
                    continue
                if other.pending_growth > 0:
                    segments = other.body
                else:
                    segments = other.body[:-1]
                if (nx, ny) in segments:
                    s.alive = False
                    break

        for s in self.snakes:
            if not s.alive:
                continue
            nx, ny = new_heads[s.name]
            s.body.insert(0, (nx, ny))

            for f in list(self.foods):
                if f.x == nx and f.y == ny:
                    self.foods.remove(f)
                    s.score += FOOD_POINTS
                    s.pending_growth += 1

            for m in list(self.magnets):
                if m.x == nx and m.y == ny:
                    self.magnets.remove(m)
                    count = len(self.foods)
                    s.score += count * FOOD_POINTS
                    s.pending_growth += count
                    self.foods.clear()

            if s.pending_growth > 0:
                s.pending_growth -= 1
            elif len(s.body) > 1:
                s.body.pop()

        self._maintain_food()

        total_cells = self.grid_size * self.grid_size
        for s in self.snakes:
            if s.alive and len(s.body) >= total_cells:
                self.game_over = True
                self.winner = s
                self.won_by_fill = True
                return False

        alive = [s for s in self.snakes if s.alive]
        if not alive:
            self.game_over = True
            return False

        if self.player_count == 2 and len(alive) == 1:
            self.game_over = True
            self.winner = alive[0]
            return False

        return True