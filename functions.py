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

def is_territory_available(global_board, territory, player_index):
    is_it = True
    for index, troop_count in enumerate(global_board[territory]):
        if index != player_index:
            if troop_count > 0:
                is_it = False
                break
    return is_it

def give_player_available_troops(global_board: dict, player_index: int):
    import math
    num_territories = 0
    min_troops = 3
    for territory in global_board:
        num_territories += 1 if global_board[territory][player_index] > 0 else 0
    num_troops = math.floor(num_territories/3)
    return max(min_troops, num_troops)

def get_territory_troops(global_board: dict, territory: str):
    return global_board[territory]

def there_are_enemy_troops_here(global_board: dict, territory: str, player_index: int):
    are_there = False
    for index, troops in enumerate(global_board[territory]):
        if index != player_index:
            if troops > 0:
                are_there = True
                break
    return are_there
                
def get_my_troops_here(global_board: dict, territory: str, player_index: int):
    return global_board[territory][player_index]

def get_enemy_troops_here(global_board: dict, territory: str, player_index: int):
    their_troops = 0
    their_index = 0
    for index, troops in enumerate(global_board[territory]):
        if index != player_index and troops > 0:
            their_troops = troops
            their_index = index
            break
    return their_index, their_troops

def remove_troops_from_territory(global_board: dict, territory: str, player_index: int, loses: int):
    global_board[territory][player_index] -= loses
    if global_board[territory][player_index] < 0:
        global_board[territory][player_index] = 0
    return global_board

def add_troops_to_territory(global_board: dict, territory: str, player_index: int, gains: int):
    global_board[territory][player_index] += gains
    return global_board

def player_can_attack(global_board: dict, board_ref: dict, player_index: int):
    # QOL Build Territories list
    territory_list = get_my_territories(global_board, player_index)
    attack_options = []
    for territory in territory_list:
        # Do i have atleast 2 troops here
        if get_my_troops_here(global_board, territory, player_index) > 1:
            # Check if adjacent territories have enemy troops
            for column_index, neighboring_territory in board_ref[territory]:
                if there_are_enemy_troops_here(global_board, neighboring_territory, player_index):
                    attack_options.append((territory, neighboring_territory))
    return len(attack_options) > 0, attack_options

def player_can_move(global_board: dict, board_ref: dict, player_index: int):
    # QOL Build Territories list
    territory_list = get_my_territories(global_board, player_index)
    movement_options = []
    for territory in territory_list:
        if get_my_troops_here(global_board, territory, player_index) > 1:
            for col, neighboring_territory in board_ref[territory]:
                if not there_are_enemy_troops_here(global_board, neighboring_territory, player_index):
                    movement_options.append((territory, neighboring_territory))
    return len(movement_options) > 0, movement_options

def get_my_territories(global_board: dict, player_index: int):
    territories = []
    for territory in global_board:
        troops = global_board[territory][player_index]
        if troops > 0:
            territories.append(territory)
    return territories

def get_the_territories_on_the_front_line(global_board: dict, board_ref: dict, player_index: int):
    my_territories = get_my_territories(global_board, player_index)
    front_line = []
    for territory in my_territories:
        # Check the boarder territories
        for col_index, neighbor_territory in board_ref[territory]:
            if there_are_enemy_troops_here(global_board, neighbor_territory, player_index):
                front_line.append(territory)
    return front_line

def get_neighboring_open_territories(global_board: dict, board_ref: dict, player_index: int): 
    my_territories = get_my_territories(global_board, player_index)
    frontier = []
    for territory in my_territories:
        # Check the boarder territories
        for col_index, neighbor_territory in board_ref[territory]:
            if not there_are_enemy_troops_here(global_board, neighbor_territory, player_index) and not (neighbor_territory in my_territories):
                frontier.append(neighbor_territory)
    return frontier

def can_move_to_front_line(global_board: dict, board_ref: dict, player_index: int):
    my_territories = get_my_territories(global_board, player_index)
    front_line = get_the_territories_on_the_front_line(global_board, board_ref, player_index)
    movement_options = []
    for territory in my_territories:
        if get_my_troops_here(global_board, territory, player_index) > 1:
            for col_index, neighbor_territory in board_ref[territory]:
                if neighbor_territory in front_line or is_territory_available(global_board, neighbor_territory, player_index): # EXPAND THE BOUNDARY
                    movement_options.append((territory, neighbor_territory))
    return len(movement_options)>0, movement_options

def get_troop_ratio(global_board: dict, attack_direction: tuple, player_index: int):
    my_troops = get_my_troops_here(global_board, attack_direction[0], player_index)
    their_troops = get_enemy_troops_here(global_board, attack_direction[1], player_index)[1]
    ratio = -1
    if their_troops > 0:
        ratio = my_troops / their_troops
    return ratio

def can_player_play(global_board: dict, player_index: int):
    """Basically just check if they have troops"""
    can_they = False
    for territory in global_board:
        if global_board[territory][player_index]>0:
            can_they = True
            break
    return can_they

def get_player_here(global_board: dict, territory: str):
    index = -1
    for player_index, troops in enumerate(global_board[territory]):
        if troops > 0:
            index = player_index
            break
    return index

def get_troops_here(global_board: dict, territory: str):
    troops = 0
    for player_index, troops in enumerate(global_board[territory]):
        if troops > 0:
            troops = troops
            break
    return troops

