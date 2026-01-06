import pygame
import random
import numpy as np

#region possible actions = directions
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
#endregion

class SnakeGame:
    def __init__(self, width=20, height=20, cell_size=20, render_mode=True):    # self definiert Objektinstanz, setzt Größen, render = Visualisierung
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.render_mode = render_mode

        if self.render_mode:        # falls Visualisiert werden soll
            pygame.init()           # werf Visualisierungsumgebung an
            self.screen = pygame.display.set_mode(      # setzt Window und seine Größe in Pixeln
                (width * cell_size, height * cell_size)
            )
            pygame.display.set_caption("Snake für MLDM")    # Titelname am Fenster
            self.clock = pygame.time.Clock()                # instanziiert ne Uhr

        self.reset()

    def reset(self):    # deifniere was genau ein Reset ist

        start_x = self.width // 2       # starte in der Mitte
        start_y = self.height // 2      # starte in der Mitte

        self.snake = [                  # zum Start - Definition der Snake
            (start_x, start_y),         # Kopf quasi
            (start_x -1, start_y),      # ein Pixel lang
            (start_x -2, start_y)       # 2 Pixel lang
        ]
        self.direction = RIGHT          # du fängst nach rechts gerichtet an
        self.score = 0                  # du hast keinen score
        self.steps_since_food = 0       # du hast quasi gerade gegessen (neu ans Leben)
        self._place_food()              # initialisiere Essen

        return self._get_state()

    def _place_food(self):              # platzierung von essen
        while True:
            self.food = (
                random.randint(0, self.width - 1),      # spawne innerhalb der Grenzen des Feldes
                random.randint(0, self.height -1)
            )
            if self.food not in self.snake:                 # wenn Essen im Feld und nicht in der Snake ist, ...
                break                                       # dann break, passt
                                                            # sonst bist noch in Loop, platzier nochmal Essen

    def step(self, action):

        self.steps_since_food += 1      # wenn du einen Schritt machst (der nicht auf Essen ist), dann +1 seit du gegessen hast

        # relativ von deiner aktuellen POS kannst du nur weiter gerade, oder links, oder recht

        if action == 1:                 # wenn du nach RECHTS gehst
            self.direction = (self.direction + 1) % 4
        elif action == 2:                # wenn du nach LINKS gehst
            self.direction = (self.direction - 1) % 4

        # action == 0: (weiter so wie du bist)

        # jetzt neue Kopfposition bestimmen
        head_x, head_y = self.snake[0]  # neue Kopfkoordinaten sind je nach Direction
        if self.direction == UP:
            head_y -= 1
        elif self.direction == DOWN:
            head_y += 1
        elif self.direction == LEFT:
            head_x -= 1
        elif self.direction == RIGHT:
            head_x += 1

        new_head = (head_x, head_y)

        # Kollisionen

        done = False        # bis auf weiteres bist du einfach nicht fertig
        reward = 0          # Reward initialisieren

        # check ob du gegen Wand f#hrst
        if (head_x < 0 or head_x >= self.width or
        head_y < 0 or head_y >= self.height):
            done = True     # du bist gegen Wand - verloren
            reward = -10            # REWARD -10
            return self._get_state(), reward, done, self.score      # WENN DU GEGEN WAND BIST - return deinen Zustand, deinen Reward, dass du fertig bist, deinen Score

        # check ob du gegen dich selber fährst (außer dein Schwanz, weil der bewegt sich)
        if new_head in self.snake[:-1]: # wenn dein neuer Kopf in deinem Körper (außer Schwanz) ist
            done = True     # verloren
            reward = -10    # REWARD -10
            return self._get_state(), reward, done, self.score

        # wenn du nicht gegen dich selbst gekracht bist
        self.snake.insert(0, new_head)  # dann beweg dich

        # schau wo essen ist
        if new_head == self.food:
            self.score += 1     # SCORE: WENN DU ESSEN HAST
            reward = 10         # REWARD: +10
            self.steps_since_food = 0   # hast grad gegessen
            self._place_food()  # platzier neu essen
            # SCHWANZ WIRD NICHT GESCHOBEN, HEIßT DU WIRST GRÖßER
        else:
            self.snake.pop()    # wir SCHIEBEN dich - du bleibst gleich groß
            #reward = self._direction_reward()   # wenn du dich richtung essen bewegst: reward

        if self.steps_since_food > self.width * self.height:    # irgendeine hohe Zahl dass der nicht im Kreis chillst
            done = True
            reward = -10

        return self._get_state(), reward, done, self.score

    def _direction_reward(self):
        """"
        head = self.snake[0]

        distance_now = abs(head[0] - self.food[0]) + abs(head[1] - self.food[1])    # x-y-Distanz zwischen Kopf und Essen

        previous_head = self.snake[1]   # davor war dein Kopf an dem vorherigen Pixel
        distance_before = abs(previous_head[0] - self.food[0]) + abs(previous_head[1] - self.food[1])   # davor war das deine Distanz zu essen

        if distance_now < distance_before:
            return 0.5    # du bist näher zu essen
        elif distance_now > distance_before:
            return -1.5       # du bist weg von essen
        return -0.5        # frag Yankoba
        """
        return 0

    def _get_state(self):

        head_x, head_y = self.snake[0]  # kopf ist da wo du bist

        # zeiger in jede richtung definieren
        point_up = (head_x, head_y -1)
        point_down = (head_x, head_y +1)
        point_left = (head_x -1, head_y)
        point_right = (head_x +1, head_y)

        # aktuelle richtungen definieren
        direction_up = self.direction == UP
        direction_down = self.direction == DOWN
        direction_left = self.direction == LEFT
        direction_right = self.direction == RIGHT

        if self.direction == UP:
            point_straight = point_up
            point_straight_2 = (head_x, head_y - 2)
        elif self.direction == DOWN:
            point_straight = point_down
            point_straight_2 = (head_x, head_y + 2)
        elif self.direction == LEFT:
            point_straight = point_left
            point_straight_2 = (head_x - 2, head_y)
        else:
            point_straight = point_right
            point_straight_2 = (head_x + 2, head_y)

        state = (
            # Kollision wenn du gerade gehst
            (direction_up and self._is_collision(point_up)) or
            (direction_down and self._is_collision(point_down)) or
            (direction_left and self._is_collision(point_left)) or
            (direction_right and self._is_collision(point_right)),

            # Kollision wenn du rechts gehst (relativ zu dir selbst)
            (direction_up and self._is_collision(point_right)) or
            (direction_down and self._is_collision(point_left)) or
            (direction_left and self._is_collision(point_up)) or
            (direction_right and self._is_collision(point_down)),

            # Kollision wenn du links relativ zu dir selbst gehst
            (direction_up and self._is_collision(point_left)) or
            (direction_down and self._is_collision(point_right)) or
            (direction_left and self._is_collision(point_down)) or
            (direction_right and self._is_collision(point_up)),

            self._is_collision(point_straight_2),   # kollision in 2 steps

            # Wo ist essen?
            self.food[0] < head_x,  # links
            self.food[0] > head_x,  # rechts
            self.food[1] < head_y,  # oben
            self.food[1] > head_y,  # unten

            point_straight == self.food,
        )

        return state

    def _is_collision(self, point):
        x, y = point

        # wo sind die wände?
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return True
        if point in self.snake[:-1]:    # wo bist du selbst?
            return True
        return False # falls keine Kollision

    def render(self, fps=5):           # visualisiere
        if not self.render_mode:
            return

        for event in pygame.event.get():        # wenn irgendwas im game passiert
            if event.type == pygame.QUIT:
                pygame.quit()       # wenn quit dann quit
                return False

        # FARBEN
        BLACK = (0, 0, 0)
        GREEN = (0, 200, 0)
        DARK_GREEN = (0, 150, 0)
        RED = (200, 0, 0)

        self.screen.fill(BLACK)     # farbe des screens

        # zeichne die Schlange
        for i, segment in enumerate(self.snake):
            x, y = segment      # jeder pixel der snake ist ein segmnent
            rectangle = pygame.Rect(    # jedes segment ist ein viereck
                x * self.cell_size, # so groß
                y * self.cell_size,
                self.cell_size - 1,
                self.cell_size -1
            )
            color = GREEN if i == 0 else DARK_GREEN     # kopf grün rest dunkelgrün
            pygame.draw.rect(self.screen, color, rectangle)

        food_rectangle = pygame.Rect(
            self.food[0] * self.cell_size,
            self.food[1] * self.cell_size,
            self.cell_size - 1,
            self.cell_size - 1
        )
        pygame.draw.rect(self.screen, RED, food_rectangle)

        pygame.display.flip()
        self.clock.tick(fps)
        return True

    def close(self):
            if self.render_mode:
                pygame.quit()

if __name__ == "__main__":
        game = SnakeGame(width=15, height=15, cell_size=30, render_mode=True)
        game.reset()

        running = True
        while running:
            action = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        action = 2
                    elif event.key == pygame.K_RIGHT:
                        action = 1

            state, reward, done, score = game.step(action)

            if not game.render(fps=4):
                break

            if done:
                print(f"OVER SCORE {score}")
                game.reset()

        game.close()
