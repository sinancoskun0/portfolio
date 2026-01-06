import pygame
from snake_game import SnakeGame
from agent import QLearningAgent


def play(
        q_table_path="q_table.pkl",
        games=5,
        fps=10,
        grid_size=15
):

    agent = QLearningAgent()
    agent.load(q_table_path)
    agent.epsilon = 0    # 0 Randomness gewünscht - nur korrekte Moves wählen

    game = SnakeGame(width=grid_size, height=grid_size, cell_size=30, render_mode=True)

    print(f"Watching trained agent play {games} games...")
    print("Close window or press Q to quit")
    print("-" * 40)

    all_scores = []

    for game_num in range(games):
        state = game.reset()
        done = False
        steps = 0

        while not done:
            # Handle quit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.close()
                    return all_scores
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    game.close()
                    return all_scores

            action = agent.choose_action(state)

            # Agent wählt Aktionen
            state, reward, done, score = game.step(action)
            steps += 1

            # Rendering
            game.screen.fill((0, 0, 0))
            for i, segment in enumerate(game.snake):
                x, y = segment
                rect = pygame.Rect(x * game.cell_size, y * game.cell_size,
                                   game.cell_size - 1, game.cell_size - 1)
                color = (0, 200, 0) if i == 0 else (0, 150, 0)
                pygame.draw.rect(game.screen, color, rect)

            food_rect = pygame.Rect(game.food[0] * game.cell_size,
                                    game.food[1] * game.cell_size,
                                    game.cell_size - 1, game.cell_size - 1)
            pygame.draw.rect(game.screen, (200, 0, 0), food_rect)

            # Score während Spielen anzeigen
            pygame.display.set_caption(f"Snake RL | Game {game_num + 1}/{games} | Score: {score}")
            pygame.display.flip()
            game.clock.tick(fps)

        all_scores.append(score)
        print(f"Game {game_num + 1}: Score = {score}, Steps = {steps}")

        # Kurze Pause zw Games
        pygame.time.wait(500)

    print("-" * 40)
    print(f"Average score: {sum(all_scores) / len(all_scores):.2f}")
    print(f"Best: {max(all_scores)}, Worst: {min(all_scores)}")

    game.close()
    return all_scores


if __name__ == "__main__":
    play(games=5, fps=12)