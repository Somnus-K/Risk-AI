def get_board_adj_dict():
    """
        This function loads in FullBoard.csv and builds a adjacency List. Returns a dictionary where the keys are the territory strings and the values are a list of tuples (column index, Territory String)
    """
    import pandas as pd
    board_df = pd.read_csv('FullBoard.csv')
    board_al = {}
    for col_index, column in enumerate(board_df.columns):
        board_al[column] = []
        for row_index, row in enumerate(board_df[column]):
            if row == 1:
                board_al[column].append((row_index, board_df.columns[row_index]))
    return board_al

def get_blank_board(num_players, board_ref):
    """
        Returns a dictionary of territorys as keys and array of ints representing the # of troops (counted as infantry) each player has
    """
    board = {}
    for territory in board_ref:
        board[territory] = [0 for player in range(0,num_players)]
    return board

def increment_turn(num_players, turn):
    return (turn + 1) % num_players

def are_all_available_troops_deployed(players: list):
    are_they = True
    for player in players:
        if player.get_available_troops() > 0:
            are_they = False
            break
    return are_they

def print_board(board: dict):
    for index, territory in enumerate(board):
        troop_str = ""
        player_index = 0
        for territory_troops in board[territory]:
            troop_str = f"{troop_str}Player {player_index+1}:\t{territory_troops}|\t"
            player_index += 1
            territory_str = f"{index}: {territory}"
            while len(territory_str) < 20:
                territory_str = f"{territory_str} "
        print(f"{territory_str}|\t{troop_str}")