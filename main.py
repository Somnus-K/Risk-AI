import functions as fns
from Players import HumanPlayer, AIPlayer
import engine 
# How do we start the script? We need a way to systematically play the game.
num_players = 2
player_turn = 0
starting_troop_count = [40,35,30,25,20,15,10,5]
# Get Board reference dictionary
board_ref = fns.get_board_adj_dict() # Holds the territories and their adjacent territories
board = fns.get_blank_board(num_players=num_players, board_ref=board_ref)

# Initialize Game State. Players inject troops onto the board. Needs to Happen Systemmatically to allow the AI to make decision in the future?
num_player_troops = starting_troop_count[num_players-2]
player1 = HumanPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=0)
player2 = HumanPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=1)
ai1 = AIPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=0, random_troop_deployment=True)
ai2 = AIPlayer(board=board, board_ref=board_ref, starting_troops=num_player_troops, player_index=1, random_troop_deployment=True)
players = [ai1, ai2]

# Init board
board = engine.init_board_place_troops(board=board, board_ref=board_ref, players=players, player_turn=player_turn)
fns.print_board(board)




