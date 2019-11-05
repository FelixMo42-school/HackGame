# HackGame
A client for games hosted on https://berkeley-hackclub-game.herokuapp.com

## Getting Started
### Installing

To download the project either press the Download button and dowloading the zip and unpack it,
or you can clone it from git hub using, 
```
git clone https://github.com/berkeleyhackclub/HackGame.git
```

Once youve installed it add the requirments by running:
```
pip3 install -r requirements.txt --user
```
Note: to do this you must `cd` into the project.

### Running

Now that youve got it downloaded you can run it!

Simple run  `python3 example.py` from the directory. If it has an error make sure your using the same version pip as python.

### Making your own bot

Allright, now your ready to start making your own bots!

If you open up example.py you will see a fairly well commented example of how to make a simple bot.
You can also have a look at Player.py for some more detail

To create a player:
```python
from Player import Player

player = Player()
    # or
player = Player(
    username: "your username",
    password: "your password"
)
    # or
player = Player("your username", "your password")
```

Once youve create a player you can add callbacks for various events.
* startGame
    * Called when the game starts
* turn
    * Called on your turn
    * Passed an object as a paramater containing
        * board - a 2d array with the value of each tile (0 is empty)
        * score - your current score
        * successfulMove - whether the last move made things move
* endGame
    * Called when the game ends
    * Also passed a data paramater, it contains
        * board
        * score

```python
@player.on("startGame")
def this_function_can_be_called_anything():
    print("the game is a foor")

@player.on("turn")
def each_on_shoul_have_a_diffrent_name(data):
    print("Its my turn")

    data.board
    data.score
    data.successfulMove

    # Return an object with what dirrection you want to swipe in.
    return {"direction": direction}

@player.on("endGame")
def you_know_the_drill_by_now(data):
    data.board
    data.score

    print("the game is over")
```