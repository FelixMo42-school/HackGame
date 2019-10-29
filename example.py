from player import Player

player = Player()

@player.on("gameStart")
def start():
    print("game is starting")

@player.on("turn")
def turn(data):
    # print("board ", data["board"])
    # print("score ", data["score"])
    # print("successfulMove ", data["successfulMove"])

    return {
        "direction": random.choice([
            "left", "right", "up", "down"
        ])
    }

@player.on("gameOver")
def end(data):
    print("final score ", data["score"])

player.startGame()
