import functions as fns

def init_board_place_troops(board, board_ref, players, player_turn):
    """
        This function is responsible for controlling to placement of troops onto the board. It needs to be flexible in that it should allow 
        an AI Agent or player to make the decision.
    """
    while(not fns.are_all_available_troops_deployed(players)):
        current_player = players[player_turn]
        print(f"Player {player_turn+1}'s Turn")
        board = current_player.place_troop_init(board)
        player_turn = fns.increment_turn(len(players), player_turn)
    
    return board

def game_over(board, num_players):
    troop_count = [0 for player in range(0, num_players)]
    for territory in board:
        for player, troops in enumerate(board[territory]):
            troop_count[player]+=troops

    first_troops_seen = True
    multiple_troops = False
    for player_troops in troop_count:
        if player_troops > 0 and first_troops_seen:
            first_troops_seen = False
        elif player_troops > 0 and not first_troops_seen:
            multiple_troops = True

    return not multiple_troops, troop_count # World Domination
