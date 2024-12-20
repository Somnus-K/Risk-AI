import functions as fns

class AIPlayer():
    """
        Incredibly Important -> KEEP AI and Human Player Classes in SYNC i.e. matching function signatures!!! 
        Only way we will be able to keep them interchangeable (Game engine functions treat them both as "Player") 

        push_frontline: True => random_move == False, random_troop_deployment == False
        aggresive_attack: True => random_attack == False
    """
    territory_names: list
    available_troops: int = 0
    board: dict
    board_ref: dict
    player_index: int
    random_troop_deployment: bool
    random_attack: bool
    random_move: bool
    random_rolls: bool
    push_frontline: bool
    random_targeting: bool
    aggresive_targeting: bool

    def __init__(self, board: dict, board_ref: dict, starting_troops: int, player_index: int, random_troop_deployment: bool, random_attack: bool, random_move: bool, random_rolls: bool, push_frontline: bool, aggresive_targeting: bool, random_targeting: bool) -> None:
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.random_troop_deployment = random_troop_deployment
        self.random_attack = random_attack
        self.random_rolls = random_rolls
        self.random_move = random_move
        self.territory_names = [territory for territory in board]
        self.push_frontline = push_frontline
        self.random_targeting = random_targeting
        self.aggresive_targeting = aggresive_targeting
    
    def place_troop_init(self, global_board: dict):
        """
            Game Initial picking of territory
        """
        import random
        if self.random_troop_deployment or True:
            while True:
                territory = random.choice(self.territory_names)
                if (fns.is_territory_available(global_board=global_board, territory=territory, player_index=self.player_index)):
                    global_board[territory][self.player_index]+=1
                    break
            self.available_troops-=1
            self.board = global_board
            return global_board 
        elif self.push_frontline: # TODO: Define this route
            front_line = fns.get_the_territories_on_the_front_line(self.board, self.board_ref, self.player_index)
            territory = random.choice(front_line)
            self.board[territory][self.player_index]+=1
            self.available_troops-=1
            return self.board
    
    def place_troop(self, global_board: dict):
        import random
        # TODO: Refactor so that you only place troops on the territories that you own
        if self.random_troop_deployment:
            while self.available_troops > 0:
                territory = random.choice(fns.get_my_territories(self.board, self.player_index))
                global_board[territory][self.player_index]+=1
                self.available_troops-=1
                self.board = global_board
            return global_board 
        elif self.push_frontline:
            while self.available_troops > 0:
                front_line = fns.get_the_territories_on_the_front_line(self.board, self.board_ref, self.player_index)
                if len(front_line) > 0:
                    territory = random.choice(front_line)
                    self.board[territory][self.player_index]+=1
                    self.available_troops-=1
                else: 
                    print('No Front line?')
                    # TODO: How to handle this - Place troops on territories that are next to open territories?
                    my_territories = fns.get_my_territories(self.board, self.player_index)
                    if len(my_territories) > 0:
                        territory = random.choice(my_territories)
                        self.board[territory][self.player_index]+=1
                        self.available_troops-=1
                    else:
                        print('help')
            return self.board
    
    def get_available_troops(self):
        return self.available_troops
    
    def attack(self, attack_direction, players):
        import random
        # TODO: Refactor this. The Num Dice and losing of players is all wrong. rules say you immediately capture a teritory if you eliminate all enemy troops
        from_territory = attack_direction[0]
        to_territory = attack_direction[1]
        my_troops = fns.get_my_troops_here(self.board, from_territory, self.player_index)
        their_index, their_troops = fns.get_enemy_troops_here(self.board, to_territory, self.player_index)
        # TODO: Remember, you must have atleast 1 more troop than the # of dice you roll
        my_max_dice = 3 if my_troops > 3 else (2 if my_troops > 2 else 1)
        # TODO: Number of dice should equal number of troops up to 2 dice
        their_max_dice = 2 if their_troops > 2 else 1 # TODO: This should be a function player.get_defend_dice 
        # Refactor rolls - we compare dice based on desc order (my highest versus your highest, so on and so forth)
        # This is done. TODO: verify this code
        if self.random_rolls:
            my_num_rolls = random.choice([i for i in range(1, my_max_dice+1)])
            # Get Player Dice
            # TODO: Pass this players version of the board to the defending player using this defend method so both players are in sync
            their_num_rolls = players[their_index].defend(their_max_dice)
            # get winner
            my_rolls = []
            their_rolls = []
            i = 0
            my_losses = 0
            their_losses = 0
            while i < max(my_num_rolls, their_num_rolls):
                if i < my_num_rolls:
                    my_rolls.append(random.choice([1,2,3,4,5,6]))
                if i < their_num_rolls:
                    their_rolls.append(random.choice([1,2,3,4,5,6]))
                i+=1
            # Compare Highest Rolls
            while len(my_rolls) > 0 and len(their_rolls) > 0:
                my_heightest = max(my_rolls)
                their_highest = max(their_rolls)
                if my_heightest > their_highest:
                    their_losses += 1
                else:
                    my_losses +=1
                # Remove the dice
                my_rolls.remove(max(my_rolls))
                their_rolls.remove(max(their_rolls))
            # Apply Troop loses to each player
            self.board = fns.remove_troops_from_territory(self.board, to_territory, their_index, their_losses)
            # Advance if we can
            if fns.get_enemy_troops_here(self.board, to_territory, self.player_index)[1] == 0:
                advancing_troops = my_num_rolls - my_losses
                # Someone has to stay behind NOTE: This shouldnt happen because of the dice rules above
                if fns.get_my_troops_here(self.board, to_territory, self.player_index) == advancing_troops:
                    # TODO: Put an assert here to alert us of error
                    advancing_troops -= 1
                self.board = fns.add_troops_to_territory(self.board, to_territory, self.player_index, advancing_troops)
                self.board = fns.remove_troops_from_territory(self.board, from_territory, self.player_index, advancing_troops)
            else:
                # Enemy is still there, subtract my losses from my troops
                self.board = fns.remove_troops_from_territory(self.board, from_territory, self.player_index, my_losses)
        pass # END ATTACK

    def defend(self, num_dice):
        import random
        if self.random_rolls:
            return random.choice([i for i in range(1, num_dice+1)]) 
        
    def move(self, movement_direction):
        import random
        from_territory = movement_direction[0]
        to_territory = movement_direction[1]
        # Assume that if we are random moving we are moving a random amount too
        if self.random_move:
            sent_troops = random.choice([i for i in range(1, self.board[from_territory][self.player_index])])
            self.board = fns.add_troops_to_territory(self.board, to_territory, self.player_index, sent_troops)
            self.board = fns.remove_troops_from_territory(self.board, from_territory, self.player_index, sent_troops)
        elif self.push_frontline:
            # Aggressively push the front line
            sent_troops = self.board[from_territory][self.player_index] - 1
            self.board = fns.add_troops_to_territory(self.board, to_territory, self.player_index, sent_troops)
            self.board = fns.remove_troops_from_territory(self.board, from_territory, self.player_index, sent_troops)
        pass
    
    def pick_target(self, attack_options: list):
        import random
        if self.random_targeting: 
            return random.choice(attack_options)
        elif self.aggresive_targeting:
            # Push frontline with greatest ratio of Troops to enemies 
            max_ratio = 0
            best_move_index = 0
            for move_index, move in enumerate(attack_options):
                ratio = fns.get_troop_ratio(self.board, move, self.player_index)
                if ratio > max_ratio:
                    max_ratio = ratio
                    best_move_index = move_index
            return attack_options[best_move_index]
    
    def pick_move(self, movement_options: list):
        import random
        if self.random_move: 
            return random.choice(movement_options)
        elif self.push_frontline:
            # Push frontline with Lowest ratio of Troops to enemies 
            # Kind of nice because it favors open land (ratio = 0) and if there is none, fortify our losing chances (their troops > our troops)
            min_ratio = 999999999999
            open_lands = []
            conflict_land = 0
            best_move_index = -1
            for move_index, move in enumerate(movement_options):
                ratio = fns.get_troop_ratio(self.board, move, self.player_index)
                if 0 < ratio < min_ratio:
                    min_ratio = ratio
                    conflict_land = move_index
                elif ratio == -1:
                    # THIS SHOULD NEVER HAPPEN
                    open_lands.append(move_index)
            # Decide to expand or fight
            # TODO: OPEN LANDS SHOULD NEVER HAPPEN
            if random.choice([0]) == 0:
                # Attack
                best_move_index = conflict_land
            else:
                # Randomly choose an open land to capture
                best_move_index = random.choice(open_lands)
            return movement_options[best_move_index]

    def play(self, global_board: dict, players):
        import random
        self.board = global_board
        self.available_troops = fns.give_player_available_troops(global_board=self.board, player_index=self.player_index)
        # Place Troops
        self.board = self.place_troop(global_board=self.board) # Sync boards
        
        playing = True
        # TODO: The player has 2 options - Attack or pass, and optionally you can choose to move/fortify one pair of territories
        while playing:
            # Attack or stay idle
            player_can_attack, attack_options = fns.player_can_attack(global_board=self.board, board_ref=self.board_ref, player_index=self.player_index)
            while player_can_attack:
                if self.random_attack:     
                    # Coin Toss... maybe not
                    if random.choice([0]) == 0:
                        # TODO: The player can continue to attack the same territory if they want... 
                        # kind of implemented here if they choose the same target
                        # Attack
                        target = self.pick_target(attack_options) 
                        # TODO: The player can continue to attack the same territory if they want... kind of implemented here if they choose the same target
                        self.attack(target, players) # Board is updated
                        # Update our attack options
                        player_can_attack, attack_options = fns.player_can_attack(global_board=self.board, board_ref=self.board_ref, player_index=self.player_index)
                    else:
                        break
                else:
                    # AI Attack
                    break
            player_can_move, movement_options = fns.player_can_move(global_board=self.board, board_ref=self.board_ref, player_index=self.player_index)
            player_can_move_fl, movement_options_fl = fns.can_move_to_front_line(global_board=self.board, board_ref=self.board_ref, player_index=self.player_index)
            if self.random_move and player_can_move:
                # Coin Toss
                if random.choice([0,1]) == 1:
                    # Move 
                    while True:
                        target = self.pick_move(movement_options)
                        # We should never have to do this check
                        if fns.get_my_troops_here(self.board, target[0], self.player_index) > 1: # We check this already in player_can_move
                            self.move(target)
                            break
            elif self.push_frontline and player_can_move_fl:
                # ALWAYS fortify in this mode
                # Move 
                while True:
                    target = self.pick_move(movement_options_fl)
                    if fns.get_my_troops_here(self.board, target[0], self.player_index) > 1: # We check this already in player_can_move
                        self.move(target)
                        break
            else:
                # AI Move
                pass
            # Player can only attack and then optionally fortify
            playing = False

        # Upgrade Troops?
        # End Turn?
        return self.board

class HumanPlayer():
    """
        Incredibly Important -> KEEP AI and Human Player Classes in SYNC i.e. matching function signatures!!! 
        Only way we will be able to keep them interchangeable (Game engine functions treat them both as "Player") 
    """
    available_troops: int = 0
    board: dict
    board_ref: dict
    player_index: int
    territory_names: list
    def __init__(self, board: dict, board_ref: dict, starting_troops: int, player_index: int) -> None:
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.territory_names = [territory for territory in board]

    def get_input(self):
        response = input("Your Move:\n")
        return response.lower()
    
    def place_troop_not_restricted(self, global_board: dict):
        while True:
            print('Board:')
            fns.print_board(global_board)
            try:
                move = input(f'Where would you like to place one troop ({self.available_troops} Remaining):\n')
                territory = self.territory_names[int(move)]
                assert fns.is_territory_available(global_board=global_board, territory=territory, player_index=self.player_index), "Invalid Move"
                global_board[territory][self.player_index]+=1
                self.available_troops-=1
                self.board = global_board
                return global_board
            except:
                print("Invalid Input")
    
    def get_available_troops(self):
        return self.available_troops

