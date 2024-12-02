import matplotlib.pyplot as plt
from Agent import ReinforcementLearningAgent
from main import play_game

def monitor_agent(agent, iterations=1000):
    win_rate = []
    avg_rewards = []
    window = 50

    for episode in range(1, iterations + 1):
        rewards, winner = play_game(agent)
        win_rate.append(winner == agent)
        avg_rewards.append(sum(rewards) / len(rewards))

        if episode % window == 0:
            print(f"Episode {episode}: Avg Reward = {sum(avg_rewards[-window:]) / window}, Win Rate = {sum(win_rate[-window:]) / window}")

    # Plotting metrics
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(range(1, iterations + 1), avg_rewards, label='Avg Reward')
    plt.title("Average Reward Over Time")
    plt.xlabel("Episodes")
    plt.ylabel("Average Reward")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(range(1, iterations + 1), [sum(win_rate[:i]) / i for i in range(1, iterations + 1)], label='Win Rate')
    plt.title("Cumulative Win Rate")
    plt.xlabel("Episodes")
    plt.ylabel("Win Rate")
    plt.legend()

    plt.tight_layout()
    plt.show()
