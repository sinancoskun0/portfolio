import numpy as np
import matplotlib.pyplot as plt
from snake_game import SnakeGame
from agent import QLearningAgent

def train (
    episodes=20000,      # wie viele trainingsepisoden
    max_steps_per_episode=3000, # wie viele steps pro episode
    render_every=None,        # render every 100th episode
    plot_stats=True
):
    # initialisiere spielumgebung
    game = SnakeGame(width=15, height=15, cell_size=30, render_mode=False)

    agent = QLearningAgent (    # initiailisere agent mit daten (evtl willst du andere als geplant?)
        learning_rate=0.1,
        discount_factor=0.9,
        epsilon=1.0,
        epsilon_min=0.01,
        epsilon_decay=0.9993
    )

    scores = [] # scores tracken
    epsilon_history = [] # track deine Randomness

    scores_window = [] # für durchschnittswerte capturen
    avg_scores  = []

    converged_scores = []
    converged_avg_scores = []
    has_converged = False

    for episode in range(episodes):
        state = game.reset()
        total_reward = 0
        steps = 0

        if render_every and episode % render_every == 0 and episode > 0:
        # spielinstanz für visualisierte episode
            visual_game = SnakeGame(width=15, height=15, cell_size=30, render_mode=True)
            visual_game.reset()
            visual_game.snake = game.snake.copy()
            visual_game.food = game.food
            visual_game.direction = game.direction
        else:
            visual_game = None

        for step in range(max_steps_per_episode):
            action = agent.choose_action(state) # agent muss action wählen aufgrund von state
            next_state, reward, done, score = game.step(action) # environment aktualisieren aufgrund von action
            agent.learn(state, action, reward, next_state, done) # lern davon

            if visual_game:
                visual_game.snake = game.snake.copy()
                visual_game.food = game.food
                visual_game.direction = game.direction
                import pygame
                visual_game.screen.fill((0, 0, 0))
                for i, segment in enumerate(visual_game.snake):
                    x, y = segment
                    rect = pygame.Rect(x * visual_game.cell_size, y * visual_game.cell_size,
                                       visual_game.cell_size - 1, visual_game.cell_size - 1)
                    color = (0, 200, 0) if i == 0 else (0, 150, 0)
                    pygame.draw.rect(visual_game.screen, color, rect)
                food_rect = pygame.Rect(visual_game.food[0] * visual_game.cell_size,
                                        visual_game.food[1] * visual_game.cell_size,
                                        visual_game.cell_size - 1, visual_game.cell_size - 1)
                pygame.draw.rect(visual_game.screen, (200, 0, 0), food_rect)
                pygame.display.flip()
                visual_game.clock.tick(15)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        visual_game.close()
                        visual_game = None
                        break

            total_reward += reward
            state = next_state
            steps += 1

            if done:
                break

        if visual_game:
            visual_game.close()

        agent.decay_epsilon() # passe epsilon neu an
        scores.append(score) # score annehmen
        epsilon_history.append(agent.epsilon) # epsilon annehmen

        scores_window.append(score)
        if len(scores_window) > 100:
            scores_window.pop(0)
        avg_score = np.mean(scores_window)
        avg_scores.append(avg_score)

        if agent.epsilon <= agent.epsilon_min + 0.001:  # wir wollen für avg nur bei epsilon min mitzählen
            if not has_converged:
                has_converged = True
                converged_episode = episode # hier hat es konvergiert
                print(f"\n*** Epsilon converged at episode {episode + 1} ***\n")
            converged_scores.append(score)

        # für graph
        if has_converged:
            converged_avg_scores.append(np.mean(converged_scores))
        else:
            converged_avg_scores.append(None)

        if (episode + 1) % 100 == 0:
            converged_str = f"Avg (converged): {np.mean(converged_scores):.2f}" if converged_scores else "Not converged"
            print(f"Episode {episode + 1}/{episodes} | "
                  f"Avg Score (last 100): {avg_score:.2f} | "
                  f"{converged_str} | "
                  f"Epsilon: {agent.epsilon:.3f} | "
                  f"Q-table states: {len(agent.q_table)}")

    print("-" * 50)
    print("Training complete!")
    print(f"Final average score (last 100): {avg_score:.2f}")
    if converged_scores:
        print(f"Converged average ({len(converged_scores)} episodes): {np.mean(converged_scores):.2f}")
    print(f"Best score achieved: {max(scores)}")
    print(f"Q-table contains {len(agent.q_table)} states")

    agent.save("q_table.pkl")

    if plot_stats:
        plot_training_stats(scores, avg_scores, epsilon_history, converged_avg_scores)

    return agent, scores

def plot_training_stats(scores, avg_scores, epsilon_history, converged_avg_scores):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Q-Learning Snake Training Results", fontsize=14)

    axes[0, 0].plot(scores, alpha=0.6, linewidth=0.5)
    axes[0, 0].set_title("Score per Episode")
    axes[0, 0].set_xlabel("Episode")
    axes[0, 0].set_ylabel("Score")

    axes[0, 1].plot(avg_scores, color="orange", linewidth=2)
    converged_x = [i for i, v in enumerate(converged_avg_scores) if v is not None]
    converged_y = [v for v in converged_avg_scores if v is not None]
    if converged_y:
        axes[0, 1].plot(converged_x, converged_y, color="blue", linewidth=2, label="Converged avg")
    axes[0, 1].set_title("Average Score (Rolling 100 Episodes)")
    axes[0, 1].set_xlabel("Episode")
    axes[0, 1].set_ylabel("Avg Score")
    axes[0, 1].legend()

    axes[1, 0].plot(epsilon_history, color="green")
    axes[1, 0].set_title("Exploration Rate (Epsilon) Decay")
    axes[1, 0].set_xlabel("Episode")
    axes[1, 0].set_ylabel("Epsilon")

    axes[1, 1].hist(scores, bins=range(0, max(scores) + 2), edgecolor="black", alpha=0.7)
    axes[1, 1].set_title("Score Distribution")
    axes[1, 1].set_xlabel("Score")
    axes[1, 1].set_ylabel("Frequency")

    plt.tight_layout()
    plt.savefig("training_results.png", dpi=150)
    plt.show()
    print("Training plot saved to training_results.png")

if __name__=="__main__":
    agent, scores = train(
        episodes = 20000,
        render_every=None,
        plot_stats=True
    )


