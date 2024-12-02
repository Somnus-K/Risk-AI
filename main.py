import copy
import functions as fns
from Players import HumanPlayer, AIPlayer
from Agent import ReinforcementLearningAgent
import engine
from matplotlib import pyplot as plt
from WorldMap import WorldMap

# Colors for players
colors = ['red', 'blue', 'green', 'orange']
num_players = 4
player_turn = 0
starting_troop_count = [40, 35, 30, 25, 20, 15, 10, 5]

# RL Agent hyperparameters
ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.1


# Get Board reference dictionary
board_ref = fns.get_board_adj_dict()
board = fns.get_blank_board(num_players=num_players, board_ref=board_ref)

# Initialize other players
ai2 = AIPlayer(board=board, board_ref=board_ref, starting_troops=starting_troop_count[num_players-2], player_index=1,
               random_troop_deployment=True, random_attack=True, random_move=True, random_rolls=True, push_frontline=False, aggresive_targeting=False, random_targeting=True)
ai3 = AIPlayer(board=board, board_ref=board_ref, starting_troops=starting_troop_count[num_players-2], player_index=2,
               random_troop_deployment=True, random_attack=True, random_move=True, random_rolls=True, push_frontline=False, aggresive_targeting=True, random_targeting=False)
ai4 = AIPlayer(board=board, board_ref=board_ref, starting_troops=starting_troop_count[num_players-2], player_index=3,
               random_troop_deployment=False, random_attack=True, random_move=False, random_rolls=True, push_frontline=True, aggresive_targeting=True, random_targeting=False)
# Initialize the RL agent
rl_agent = ReinforcementLearningAgent(
    board=board,
    board_ref=board_ref,
    starting_troops=starting_troop_count[num_players-2],
    player_index=0
)

players = [rl_agent, ai2, ai3, ai4]

# Initialize the game board
board = engine.init_board_place_troops(board=board, board_ref=board_ref, players=players, player_turn=player_turn)
fns.print_board(board)

# Initialize stats
board_states = [copy.deepcopy(board)]
rewards = [0] * num_players
win_counts = [0] * num_players

# Game loop
game_over, troop_state = engine.game_over(board, len(players))
turn = 1

while not game_over:
    print(f'__Turn {turn}__________________________________________')
    current_player = players[player_turn]

    if fns.can_player_play(board, player_turn):
        # RL agent-specific logic
        if player_turn == 0:  # RL agent's turn
            state = (tuple(engine.calculate_player_troops(board, len(players))),
                     tuple(engine.calculate_players_num_territories(board, len(players))))
            board = current_player.play(board, players)
            next_state = (tuple(engine.calculate_player_troops(board, len(players))),
                          tuple(engine.calculate_players_num_territories(board, len(players))))
            reward = engine.calculate_player_troops(board, len(players))[0] - rewards[player_turn]
            rl_agent.update_q_value(state, None, reward, next_state)
            rewards[player_turn] = engine.calculate_player_troops(board, len(players))[0]
        else:
            board = current_player.play(board, players)

        # Check game over condition
        game_over, troop_state = engine.game_over(board, len(players))
        player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)
        turn += 1

        # Save board states
        board_states.append(copy.deepcopy(board))

    else:
        player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)

# Determine winner
winner = troop_state.index(max(troop_state))
win_counts[winner] += 1

# Print final board
fns.print_board(board)

# Display results
print(f"Winner: Player {winner + 1}")
