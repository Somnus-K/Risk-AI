import random
import functions as fns


class ReinforcementLearningAgent:
    def __init__(self, board, board_ref, starting_troops, player_index, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}

    def get_available_troops(self):
        """Returns the number of available troops."""
        return self.available_troops

    def place_troop_init(self, global_board):
        """Place troops during the initialization phase."""
        while self.available_troops > 0:
            territory = random.choice(fns.get_my_territories(global_board, self.player_index))
            fns.add_troops_to_territory(global_board, territory, self.player_index, 1)
            self.available_troops -= 1
        return global_board

    def place_troop(self, global_board):
        """Place troops during regular turns."""
        while self.available_troops > 0:
            territory = random.choice(fns.get_my_territories(global_board, self.player_index))
            fns.add_troops_to_territory(global_board, territory, self.player_index, 1)
            self.available_troops -= 1
        return global_board

    def play(self, global_board, players):
        """Main logic for the RL agent's turn."""
        self.board = global_board

        # Troop placement
        self.available_troops = fns.give_player_available_troops(global_board, self.player_index)
        global_board = self.place_troop(global_board)

        # Attacking logic
        player_can_attack, attack_options = fns.player_can_attack(global_board, self.board_ref, self.player_index)
        while player_can_attack:
            attack_direction = random.choice(attack_options)
            self.attack(global_board, attack_direction, players)
            player_can_attack, attack_options = fns.player_can_attack(global_board, self.board_ref, self.player_index)

        # Movement logic
        player_can_move, movement_options = fns.player_can_move(global_board, self.board_ref, self.player_index)
        if player_can_move:
            movement_direction = random.choice(movement_options)
            self.move(global_board, movement_direction)

        return global_board

    def attack(self, global_board, attack_direction, players):
        """Executes an attack."""
        from_territory, to_territory = attack_direction
        my_troops = fns.get_my_troops_here(global_board, from_territory, self.player_index)
        their_index, their_troops = fns.get_enemy_troops_here(global_board, to_territory, self.player_index)

        # Simulate attack
        if my_troops > 1:
            # Apply troops loss/gain
            fns.remove_troops_from_territory(global_board, to_territory, their_index, their_troops)
            fns.add_troops_to_territory(global_board, to_territory, self.player_index, my_troops - 1)

    def move(self, global_board, movement_direction):
        """Moves troops between territories."""
        from_territory, to_territory = movement_direction
        troops_to_move = fns.get_my_troops_here(global_board, from_territory, self.player_index) - 1
        if troops_to_move > 0:
            fns.add_troops_to_territory(global_board, to_territory, self.player_index, troops_to_move)
            fns.remove_troops_from_territory(global_board, from_territory, self.player_index, troops_to_move)
