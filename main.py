import copy
import functions as fns
from Players import HumanPlayer, AIPlayer
import engine 
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from WorldMap import WorldMap
import networkx as nx
# How do we start the script? We need a way to systematically play the game.
colors= ['red', 'blue', 'green', 'orange']
num_players = 4
player_turn = 0
starting_troop_count = [40,35,30,25,20,15,10,5]
# Get Board reference dictionary
board_ref = fns.get_board_adj_dict() # Holds the territories and their adjacent territories
board = fns.get_blank_board(num_players=num_players, board_ref=board_ref)
board_states = [] # Used for animation
players_troops_ratio = [] # Statistics
players_total_territories = [] # Statistics
players_troop_territory_ratios = [] # Statistics
players_frontline_exposure = [] # Statistics
players_frontline_troops = [] # Statistics

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
               random_move=True,
               random_rolls=True,
               push_frontline=False,
               aggresive_targeting=False,
               random_targeting=True)
ai2 = AIPlayer(board=board, 
               board_ref=board_ref, 
               starting_troops=num_player_troops, 
               player_index=1, 
               random_troop_deployment=True,
               random_attack=True,
               random_move=True,
               random_rolls=True,
               push_frontline=False,
               aggresive_targeting=False,
               random_targeting=True)
ai3 = AIPlayer(board=board, 
               board_ref=board_ref, 
               starting_troops=num_player_troops, 
               player_index=2, 
               random_troop_deployment=True,
               random_attack=True,
               random_move=True,
               random_rolls=True,
               push_frontline=False,
               aggresive_targeting=True,
               random_targeting=False)
ai4 = AIPlayer(board=board, 
               board_ref=board_ref, 
               starting_troops=num_player_troops, 
               player_index=3, 
               random_troop_deployment=False,
               random_attack=True,
               random_move=False,
               random_rolls=True,
               push_frontline=True,
               aggresive_targeting=True,
               random_targeting=False)
players = [ai1, ai2, ai3, ai4]

# Init board
board = engine.init_board_place_troops(board=board, board_ref=board_ref, players=players, player_turn=player_turn)
fns.print_board(board)
board_map = WorldMap(board, board_ref, colors)
# Save INIT State
board_states.append(copy.deepcopy(board))
players_troops_ratio.append(copy.deepcopy(engine.calculate_player_troops(board, len(players))))
players_total_territories.append(copy.deepcopy(engine.calculate_players_num_territories(board, len(players))))
players_troop_territory_ratios.append(copy.deepcopy(engine.calculate_players_troop_territory_ratio(board, len(players))))
players_frontline_exposure.append(copy.deepcopy(engine.calculate_number_of_edges_in_frontline(board, board_ref, len(players))))
players_frontline_troops.append(copy.deepcopy(engine.calculate_number_of_edges_in_frontline(board, board_ref, len(players))))

# Increment Turn?
player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)

# Game loop - 
game_over, troop_state = engine.game_over(board, len(players))
turn = 1
while not game_over:
    print(f'__Turn {turn}__________________________________________')
    # Select Player
    current_player = players[player_turn]
    # TODO: This might need to change. should both players be given the opportunity to place troops before each player attacks?
    if fns.can_player_play(board, player_turn):
        # Make Choice
        board = current_player.play(board, players)
        # Increment turn
        game_over, troop_state = engine.game_over(board, len(players))
        player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)
        if turn % 1 == 0:
            board_states.append(copy.deepcopy(board))
        if turn == 500: # Takes too long to save animations
            break
        turn+=1
        # Calculate Win chances
        players_troops_ratio.append(copy.deepcopy(engine.calculate_player_troops(board, len(players))))
        players_total_territories.append(copy.deepcopy(engine.calculate_players_num_territories(board, len(players))))
        players_troop_territory_ratios.append(copy.deepcopy(engine.calculate_players_troop_territory_ratio(board, len(players))))
        players_frontline_exposure.append(copy.deepcopy(engine.calculate_number_of_edges_in_frontline(board, board_ref, len(players))))
        players_frontline_troops.append(copy.deepcopy(engine.calculate_number_of_troops_on_frontline(board, board_ref, len(players))))
    else:
        player_turn = fns.increment_turn(num_players=len(players), turn=player_turn)
# Print Final Board
fns.print_board(board)

# ANIMATING / GRAPHING RESULTS __________________________
x = input("Y: make movie, N: exit\n")
if x.upper() == "Y":
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
    ani.save('troop distribution bar chart.mp4', writer='ffmpeg', dpi=300)
else:
    pass
x = input("Y: make map movie, N: exit\n")
if x.upper() == "Y": 
    G = nx.Graph()
    board_map.build_graph(board_states[0], board_ref, colors)
    G.add_nodes_from(board_map.nodes)
    G.add_edges_from(board_map.edges)
    # Set up figure and layout
    fig = plt.figure()
    pos = nx.spring_layout(G, seed=42)
    plt.title("Risk")
    
    def update_graph(frame):
        board_map.build_graph(board_states[frame], board_ref, colors)
        plt.clf()
        nx.draw(G, pos, with_labels=True, node_size=3000, labels=board_map.node_labels, node_color=board_map.node_colors, font_size=8, font_weight="bold", edge_color="gray")
    
    ani = FuncAnimation(fig, update_graph, frames=len(board_states), interval=100)
    ani.save('Board.mp4', writer='ffmpeg', dpi=300)
    fig.clf()
    plt.close('all')
else:
    pass
# Figures 1-3-------------------------------------------------------------
plt.clf()
fig, axs = plt.subplots(2, 3, figsize=(15, 5))
# Plot change in chance to win over time
X = range(0, len(players_troops_ratio))
ys_win = []
ys_territory = []
ys_tt_ratio = []
ys_flexposure = []
ys_frontline_troops = []
# Extract the Y's
for player_index, player in enumerate(players):
    y_win_partial = []
    y_ter_partial = []
    y_tt_ratio = []
    y_flexposure = []
    y_frontline_troops = []

    for player_percentages in players_troops_ratio:
        y_win_partial.append(player_percentages[player_index])

    for player_territories in players_total_territories:
        y_ter_partial.append(player_territories[player_index])
    
    for player_tt in players_troop_territory_ratios:
        y_tt_ratio.append(player_tt[player_index])
    
    for player_exposure in players_frontline_exposure:
        y_flexposure.append(player_exposure[player_index])

    for player_troops in players_frontline_troops:
        y_frontline_troops.append(player_troops[player_index])

    ys_flexposure.append(copy.deepcopy(y_flexposure))
    ys_frontline_troops.append(copy.deepcopy(y_frontline_troops))

    ys_win.append(copy.deepcopy(y_win_partial))
    ys_territory.append(copy.deepcopy(y_ter_partial))
    ys_tt_ratio.append(copy.deepcopy(y_tt_ratio))

for player_index, y in enumerate(ys_win):
    axs[0,0].plot(X,y, color=colors[player_index], label=f"Player {player_index+1}")

for player_index, y in enumerate(ys_territory):
    axs[0,1].plot(X,y, color=colors[player_index], label=f"Player {player_index+1}")

for player_index, y in enumerate(ys_tt_ratio):
    axs[0,2].plot(X,y, color=colors[player_index], label=f"Player {player_index+1}")


for player_index, y in enumerate(ys_flexposure):
    axs[1,0].plot(X,y, color=colors[player_index], label=f"Player {player_index+1}")


for player_index, y in enumerate(ys_frontline_troops):
    axs[1,1].plot(X,y, color=colors[player_index], label=f"Player {player_index+1}")

# Add a legend to describe each line
axs[0,0].set_xlabel("Turn #")
axs[0,0].set_ylabel("# Troops on Board")
axs[0,0].set_title("Troops Deployed Timeline")
axs[0,1].set_xlabel("Turn #")
axs[0,1].set_ylabel("# Territories")
axs[0,1].set_title("Territories Conquered Timeline")
axs[0,2].set_xlabel("Turn #")
axs[0,2].set_ylabel("Troops to Territories")
axs[0,2].set_title("Ratio Troops to Territories")
axs[1,0].set_xlabel("Turn #")
axs[1,0].set_ylabel("# of Adjacent Enemies")
axs[1,0].set_title("Frontline Exposure")
axs[1,1].set_xlabel("Turn #")
axs[1,1].set_ylabel("# of Troops on Frontline")
axs[1,1].set_title("Frontline Deployment")
plt.show()





