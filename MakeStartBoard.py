import random
from pprint import pprint

startTroops = [40,35,30,25,20,15,10,5] # Number of troops each player starts with in a 2,3,4,5,6,7,8,9 player game
gameState = [[0 for _ in range(2)] for _ in range(42)]
numbers = list(range(0, 42))

# Get number of players
players = int(input("Enter the number of players: "))

playerTroops = [startTroops[players-2] for _ in range(players)]
listOfPlayers = [i for i in range(1, players+1)]
listOfPlayers.reverse()

# Distribute land to the players
while numbers:
    while listOfPlayers:
        if numbers != []:
            randomValue = random.choice(numbers)
            numbers.remove(randomValue)
            gameState[randomValue][0] = listOfPlayers[0]
            listOfPlayers.pop(0)
        else:
            break
    listOfPlayers = [i for i in range(1, players + 1)]
    listOfPlayers.reverse()

# Distribute one troop to each land that a player owns
for state in gameState:
    playerID = state[0]
    if playerID != 0:
        state[1] = 1
        playerTroops[playerID - 1] = playerTroops[playerID - 1] - 1

# Distribute the remaining troops randomly to the lands owned by each player
for playerID in range(1, players + 1):
    while playerTroops[playerID - 1] > 0:
        playerLands = [index for index, state in enumerate(gameState) if state[0] == playerID]
        if playerLands:
            chosenLand = random.choice(playerLands)
            gameState[chosenLand][1] += 1
            playerTroops[playerID - 1] = playerTroops[playerID - 1] - 1

# Count the number of lands each player owns
landCount = {i: 0 for i in range(1, players + 1)}
for state in gameState:
    playerID = state[0]
    if playerID in landCount:
        landCount[playerID] = landCount[playerID] + 1

pprint(gameState)
print("Land count per player:", landCount)