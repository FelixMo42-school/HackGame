import socketio
import json
import getpass

PLAYER_DEFAULT_URL = "https://berkeley-hackclub-game.herokuapp.com"

class Player(socketio.ClientNamespace):
    """ A socket.io client for playing berkeley hackclub games. """

    def __init__(self, username="", password="", url=PLAYER_DEFAULT_URL):
        super().__init__("/2048")

        if username == "":
            self.username = input("enter username: ")
        else:
            self.username = username

        if password == "":
            self.password = getpass.getpass(prompt="Enter password (it will not show up):")
        else:
            self.password = password

        self.url = url

        self.callbacks = {}

    def on_connect(self):
        """ Callback for when the game connects to the server. use Player.on("gameStart") to register a callback for it. """

        if "gameStart" in self.callbacks:
            self.callbacks["gameStart"]()

    def on_turn(self, msg):
        """ Callback for when its your turn. use Player.on("turn") to register a callback for it. """

        data = json.loads(msg)

        self.emit("turn", json.dumps(
            self.callbacks["turn"](data)
        ))

    def on_end(self, msg):
        """ Callback for when its your turn. use Player.on("turn") to register a callback for it. """

        data = json.loads(msg)
        
        if "gameOver" in self.callbacks:
            self.callbacks["gameOver"](data)

    def on_login_failed(self, msg):
        """ Called if your authentication was incorrect. """

        print(msg)


        
    def on(self, event: str):
        """ Registers a callback for a game events. Use ither gameStart, turn or gameEnd. """

        def decorator(func):
            self.callbacks[event] = func
            return func

        return decorator

    def startGame(self, name=""):
        """ Plays a full game. You must have registered a on turn calback to play. """

        if "turn" in self.callbacks:
            sio=socketio.Client(reconnection=False)
            sio.register_namespace(self)

            sio.connect(self.url, {
                "username": self.username,
                "password": self.password,
                "name": name
            })

            sio.wait()
        else:
            print("Must have an turn callback to play game.")
