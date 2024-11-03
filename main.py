import copy
import functions as fns
from Players import HumanPlayer, AIPlayer
import engine 
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
# How do we start the script? We need a way to systematically play the game.
num_players = 2
player_turn = 0
starting_troop_count = [40,35,30,25,20,15,10,5]
# Get Board reference dictionary
board_ref = fns.get_board_adj_dict() # Holds the territories and their adjacent territories
board = fns.get_blank_board(num_players=num_players, board_ref=board_ref)
board_states = [] # Used for animation

# Initialize Game State. Players inject troops onto the board. Needs to Happen Systemmatically to allow the AI to make decision in the future?
num_player_troops = starting_troop_count[num_players-2]
player1 = HumanPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=0)
player2 = HumanPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=1)
ai1 = AIPlayer(board=board, 
               board_ref=board_ref, 
               starting_troops=num_player_troops, 
               player_index=0, 
               random_troop_deployment=True,
               random_attack=True,
               random_move=False,
               random_rolls=True,
               push_frontline=True)
ai2 = AIPlayer(board=board, 
               board_ref=board_ref, 
               starting_troops=num_player_troops, 
               player_index=1, 
               random_troop_deployment=True,
               random_attack=True,
               random_move=False,
               random_rolls=True,
               push_frontline=True)
players = [ai1, ai2]

# Init board
board = engine.init_board_place_troops(board=board, board_ref=board_ref, players=players, player_turn=player_turn)
fns.print_board(board)
board_states.append(board.copy())

# Increment Turn?
player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)

# Game loop - 
game_over, troop_state = engine.game_over(board, len(players))
turn = 1
while not game_over:
    print(f'__Turn {turn}__________________________________________')
    # Select Player
    current_player = players[player_turn]
    # Make Choice
    board = current_player.play(board, players)
    # Increment turn
    game_over, troop_state = engine.game_over(board, len(players))
    player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)
    if turn % 10 == 0:
        board_states.append(copy.deepcopy(board))
    if turn == 1000:
        break
    turn+=1
# Print Final Board
fns.print_board(board)

# ANIMATING / GRAPHING RESULTS __________________________

# Extract x labels and number of bars per group
x_labels = list(board_states[0].keys())
num_groups = len(x_labels)
num_bars = len(board_states[0][x_labels[0]])
# Set up the figure and axis
fig, ax = plt.subplots()
x = np.arange(num_groups)  # label locations
width = 0.2  # width of each bar

# Initialize bars and store references in a list
bars = []
for i in range(num_bars):
    bar = ax.bar(x + i * width, [board_states[0][group][i] for group in x_labels], width, label=f'Player {i + 1}')
    bars.append(bar)

# Add labels and title
ax.set_xlabel('Territories')
ax.set_ylabel('Troops')
ax.set_title('Troop Distribution')
ax.set_xticks(x + width * (num_bars - 1) / 2)
ax.set_xticklabels(x_labels)
ax.legend()
plt.xticks(rotation=45)
colors= ['red', 'blue', 'green', 'yellow']

# Update function that takes the current frame index and applies the corresponding snapshot
def update(frame):
    snapshot = board_states[frame]  # Get the snapshot for the current frame

    # Update each bar's height based on the current snapshot
    for i, bar_group in enumerate(bars):
        for j, bar in enumerate(bar_group):
            bar.set_height(snapshot[x_labels[j]][i])  # Set the height of each bar

    return [bar for bar_group in bars for bar in bar_group]

# Create the animation, using the number of snapshots as the total frames
ani = FuncAnimation(fig, update, frames=len(board_states), blit=True, interval=100)
ani.save('game_board_animation.mp4', writer='ffmpeg', dpi=300)




