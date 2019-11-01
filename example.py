from Player import Player
import random

player = Player(
    username="admin",
    password="12345",
    url="http://localhost:3000/"
)

# Register a callback that will be called when the game starts.
@player.on("gameStart")
def start():
    print("game is starting")

# Register a callback that will be called when you need to make a move
# return which direction you would like to swip in: left, right, up, down
@player.on("turn")
def turn(data):
    # data is a object containing the board, the score and weather your last move was successful
    # 
    # print("board ", data["board"])
    #
    # print("score ", data["score"])
    #
    # print("successfulMove ", data["successfulMove"])

    return {
        "direction": random.choice([
            "left", "right", "up", "down"
        ])
    }

# Register a callback that will be called when the game ends.
@player.on("gameOver")
def end(data):
    print("final score ", data["score"])

# This will make it play a game. 
# The name is just for your own purposes so that you can identify which algorithm this is.
player.startGame("random1")
