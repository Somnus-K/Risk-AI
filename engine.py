import functions as fns

def init_board_place_troops(board, board_ref, players, player_turn):
    """
        This function is responsible for controlling to placement of troops onto the board. It needs to be flexible in that it should allow 
        an AI Agent or player to make the decision.
    """
    while(not fns.are_all_available_troops_deployed(players)):
        current_player = players[player_turn]
        print(f"Player {player_turn+1}'s Turn")
        board = current_player.place_troop_not_restricted(board)
        player_turn = fns.increment_turn(len(players), player_turn)
    
    return board