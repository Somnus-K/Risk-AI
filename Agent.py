import random
import functions as fns


class ReinforcementLearningAgent():
    def __init__(self, board, board_ref, starting_troops, player_index, alpha=0.5, gamma=0.9, epsilon=0.3):
        self.board = board
        self.board_ref = board_ref
        self.available_troops = starting_troops
        self.player_index = player_index
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration rate
        self.q_table = {}

    def get_available_troops(self):
        return self.available_troops

    def place_troop_init(self, global_board):
        while self.available_troops > 0:
            my_territories = fns.get_my_territories(global_board, self.player_index)
            if not my_territories:
                territory = random.choice(list(global_board.keys()))
            else:
                territory = random.choice(my_territories)
            
            # Add troop to the chosen territory
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
        state = (tuple(fns.get_my_territories(self.board, self.player_index)),
                 tuple(fns.get_blank_board(len(players), self.board_ref).keys()))
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
            next_state = (tuple(fns.get_my_territories(global_board, self.player_index)),
                          tuple(fns.get_blank_board(len(players), self.board_ref).keys()))
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
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0

        # Get the maximum Q-value for the next state
        next_max = max(self.q_table.get(next_state, {}).values(), default=0)

        # Update the Q-value using the Q-learning formula
        self.q_table[state][action] += self.alpha * (reward + self.gamma * next_max - self.q_table[state][action])
