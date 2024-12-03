import random
import functions as fns
import json
import os
import hashlib
import pickle


class ReinforcementLearningAgent():
    def __init__(self, board, board_ref, starting_troops, player_index, alpha=0.5, gamma=0.9, epsilon=0.3, q_table_path="q_table.pkl"):
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}
        self.q_table_path = q_table_path  # Path to save/load Q-table
        self.numUpdated = 0

        # Attempt to load the Q-table from a file
        self.load_q_table()

    def save_q_table(self):
        """Save the Q-table to a file using pickle."""
        try:
            with open(self.q_table_path, "wb") as f:
                pickle.dump(self.q_table, f)
            print(f"Q-table saved to {self.q_table_path}")
        except Exception as e:
            print(f"Failed to save Q-table: {e}")

    def flatten_key(self, key):
        """Flatten a tuple or complex key into a JSON-compatible string."""
        if isinstance(key, tuple):
            return "|".join(self.flatten_key(sub_key) for sub_key in key)  # Recursively flatten nested tuples
        elif isinstance(key, list):
            return "|".join(self.flatten_key(sub_key) for sub_key in key)  # Handle lists, if present
        return str(key)  # Convert other types to string

    def hash_key(self, key):
        """Convert a tuple or other complex structure into a unique hashable string."""
        key_str = repr(key)  # Represent the key as a string
        return hashlib.md5(key_str.encode()).hexdigest()  # Create an MD5 hash of the string

    def load_q_table(self):
        """Load the Q-table from a file using pickle."""
        if os.path.exists(self.q_table_path):
            try:
                with open(self.q_table_path, "rb") as f:
                    self.q_table = pickle.load(f)
                print(f"Q-table loaded from {self.q_table_path}")
            except Exception as e:
                print(f"Failed to load Q-table: {e}. Starting fresh.")
                self.q_table = {}
        else:
            print(f"No Q-table found at {self.q_table_path}. Starting fresh.")

    def unflatten_key(self, key):
        """Rebuild the original key structure from the flattened string."""
        if "|" in key:
            return tuple(key.split("|"))  # Split the string back into a tuple
        return key  # Return the key as-is if no delimiter is found

    def unhash_key(self, hashed_key):
        """Reverse the hashing to regenerate the original key (if needed)."""
        # Note: Storing the original keys elsewhere is recommended if reverse mapping is required.
        raise NotImplementedError("Key hashing is one-way. Use consistent keys.")

    def get_available_troops(self):
        return self.available_troops

    def place_troop_init(self, global_board):
        while self.available_troops > 0:
            my_territories = fns.get_my_territories(global_board, self.player_index)
            if not my_territories:
                territory = random.choice(list(global_board.keys()))
            else:
                territory = random.choice(my_territories)

            print(f"Placing troop on {territory}. Available troops: {self.available_troops}")  # Debugging
            fns.add_troops_to_territory(global_board, territory, self.player_index, 1)
            self.available_troops -= 1
        return global_board

    def choose_action(self, state, actions):
        if random.uniform(0, 1) < self.epsilon:
            # Explore
            return random.choice(actions)
        else:
            # use known highest Q
            if state in self.q_table:
                return max(actions, key=lambda a: self.q_table[state].get(a, 0))
            else:
                # if the state is not in the Q-table, pick randomly
                return random.choice(actions)

    def play(self, global_board, players):
        self.board = global_board
        state = self.flatten_key((
            tuple(fns.get_my_territories(self.board, self.player_index)),
            tuple(fns.get_blank_board(len(players), self.board_ref).keys())
        ))
        # deploy
        self.available_troops = fns.give_player_available_troops(global_board, self.player_index)
        while self.available_troops > 0:
            my_territories = fns.get_my_territories(global_board, self.player_index)
            if not my_territories:
                break
            action = self.choose_action(state, my_territories)
            fns.add_troops_to_territory(global_board, action, self.player_index, 1)
            self.available_troops -= 1
        # Attack
        player_can_attack, attack_options = fns.player_can_attack(global_board, self.board_ref, self.player_index)
        while player_can_attack:
            action = self.choose_action(state, attack_options)
            reward = self.attack(global_board, action, players)
            next_state = self.flatten_key((
                tuple(fns.get_my_territories(global_board, self.player_index)),
                tuple(fns.get_blank_board(len(players), self.board_ref).keys())
            ))
            self.update_q_value(state, action, reward, next_state)
            state = next_state
            player_can_attack, attack_options = fns.player_can_attack(global_board, self.board_ref, self.player_index)
        # Move
        player_can_move, movement_options = fns.player_can_move(global_board, self.board_ref, self.player_index)
        if player_can_move:
            action = self.choose_action(state, movement_options)
            self.move(global_board, action)
        return global_board


    def attack(self, global_board, attack_direction, players):
        from_territory, to_territory = attack_direction
        my_troops = fns.get_my_troops_here(global_board, from_territory, self.player_index)
        their_index, their_troops = fns.get_enemy_troops_here(global_board, to_territory, self.player_index)

        reward = -1  # penalty for attacking
        if my_troops > 1:
            if their_troops > 0:
                # Attack successful but not captured
                fns.remove_troops_from_territory(global_board, to_territory, their_index, their_troops)
                reward = 1
            else:
                # Captured
                fns.add_troops_to_territory(global_board, to_territory, self.player_index, my_troops - 1)
                reward = 2
        return reward

    def move(self, global_board, movement_direction):
        from_territory, to_territory = movement_direction
        troops_to_move = fns.get_my_troops_here(global_board, from_territory, self.player_index) - 1
        if troops_to_move > 0:
            fns.add_troops_to_territory(global_board, to_territory, self.player_index, troops_to_move)
            fns.remove_troops_from_territory(global_board, from_territory, self.player_index, troops_to_move)

    def defend(self, num_dice):
        return random.choice([i for i in range(1, num_dice+1)])

    def update_q_value(self, state, action, reward, next_state):
        """Update the Q-value for a given state-action pair."""
        state = self.flatten_key(state)  # Flatten state
        next_state = self.flatten_key(next_state)  # Flatten next_state

        print(f"State: {state} (type: {type(state)})")
        print(f"Next State: {next_state} (type: {type(next_state)})")

        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0
        max_next_q = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q - self.q_table[state][action])







