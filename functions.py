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

