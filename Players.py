import functions as fns

class AIPlayer():
    """
        Incredibly Important -> KEEP AI and Human Player Classes in SYNC i.e. matching function signatures!!! 
        Only way we will be able to keep them interchangeable (Game engine functions treat them both as "Player") 
    """
    available_troops: int = 0
    board: dict
    board_ref: dict
    player_index: int
    random_troop_deployment: bool
    def __init__(self, board: dict, board_ref: dict, starting_troops: int, player_index: int, random_troop_deployment: bool) -> None:
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.random_troop_deployment = random_troop_deployment
    
    def place_troop_not_restricted(self, global_board: dict):
        import random
        if self.random_troop_deployment:
            move = random.choice(range(0, len(self.board)))
            for index, territory in enumerate(global_board):
                if index == move:
                    global_board[territory][self.player_index]+=1
                    break
            self.available_troops-=1
            self.board = global_board
            return global_board 
    
    def get_available_troops(self):
        return self.available_troops

class HumanPlayer():
    """
        Incredibly Important -> KEEP AI and Human Player Classes in SYNC i.e. matching function signatures!!! 
        Only way we will be able to keep them interchangeable (Game engine functions treat them both as "Player") 
    """
    available_troops: int = 0
    board: dict
    board_ref: dict
    player_index: int
    def __init__(self, board: dict, board_ref: dict, starting_troops: int, player_index: int) -> None:
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
    def get_input(self):
        response = input("Your Move:\n")
        return response.lower()
    
    def place_troop_not_restricted(self, global_board: dict):
        while True:
            print('Board:')
            fns.print_board(global_board)
            try:
                move = input(f'Where would you like to place one troop ({self.available_troops} Remaining):\n')
                territory_index = int(move)
                for index, territory in enumerate(global_board):
                    if index == territory_index:
                        global_board[territory][self.player_index]+=1
                        break
                self.available_troops-=1
                self.board = global_board
                return global_board
            except:
                print("Invalid Input")
    
    def get_available_troops(self):
        return self.available_troops

