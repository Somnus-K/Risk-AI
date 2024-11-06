import functions as fns
'''
    TODO:
    Things to investigate as metrics:

    Frontline Exposure: How many edges does a player share with an enemy
    * Per enemy player Exposure
    * Total Exposure

    Per territory troop allocation line graph
    * Each player has a line
    * Plots the number of troops each player has on the specifc territory (one player has troops on it at a time)
    * Identify sought after territories

    Cluster count (Forgot how to do this help )
    * Number of clusters of territrories a player has
    * Consolidated versus fragmented forces
    * Consolidated forces allows reinforcements to travel to frontlines

    # of troops on frontline versus inside and the ration between the two 
    * Measure of reinforcements (Troops not on the frontline)
    * Could be interesting to compare this with the Frontline Exposure
    * I would bet that the Aggresive bot has a high frontline count and exposure rating

    Ratio of frontline troops to total troops 
    * How much risk are we exposing our army too?
    * Interesting with The frontline exposure... I think of Australia, low exposure - Funnel, with the ability to fortify reinforcements behind it to fuel that frontline

    The Troop Aquisition Rate
    * # of troops gained per turn. 
    * Derived from the number of territories
    * Or we can just look at the Delta on the total number of troops a player has turn to turn

'''
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

def calculate_player_troops(board, num_players):
    player_total_troops = [0 for player in range(0, num_players)]
    for territory in board:
        for player_index, player_troops in enumerate(board[territory]):
            player_total_troops[player_index]+=player_troops
    return player_total_troops

def calculate_player_troops_ratio(board, num_players):
    # TODO: Combine the above ... refactor
    total_num_troops = 0
    player_total_troops = [0 for player in range(0, num_players)]
    for territory in board:
        for player_index, player_troops in enumerate(board[territory]):
            total_num_troops+=player_troops
            player_total_troops[player_index]+=player_troops
    player_odds = [(player_troops/total_num_troops) for player_troops in player_total_troops]
    return player_odds

def calculate_players_num_territories(board, num_players):
    player_total_territories = [0 for player in range(0, num_players)]
    for territory in board:
        for player_index, player_troops in enumerate(board[territory]):
            if player_troops > 0:
                player_total_territories[player_index]+=1
                break
    return player_total_territories

def calculate_players_troop_territory_ratio(board, num_players):
    player_troops = calculate_player_troops(board, num_players)
    player_territories = calculate_players_num_territories(board, num_players)
    res= []
    for player_index in range(0, num_players):
        if player_territories[player_index] > 0:
            res.append((player_troops[player_index]/player_territories[player_index]))
        else:
            res.append(0)
    return res
