import socketio
import json
import getpass

# Where is the website being hosted right now?
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

    def on(self, event):
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

    ###################################################################################
    ##              END OF PUBLIC API, DONT CALL ANY OF THESE FUNCTIONS!             ##
    ###################################################################################

    # The on_* functions are automatically called by sockerio in response to the corresponding event.
    # If you want to register a callback you should use the Player.on("call back name") decorator

    def on_connect(self):
        """ Callback for when the game connects to the server. use Player.on("gameStart") to register a callback for it. """

        # If a gameStart callback is registed then call it.
        if "gameStart" in self.callbacks:
            self.callbacks["gameStart"]()

    def on_turn(self, msg):
        """ Callback for when its your turn. use Player.on("turn") to register a callback for it. """

        # Decode the message
        data = json.loads(msg)

        # Call the on turn callback and send the users move back to the server as a json.
        # We dont have to check if a turn callback is registed beacause it must have on to be initated.
        self.emit("turn", json.dumps(
            self.callbacks["turn"](data)
        ))

    def on_end(self, msg):
        """ Callback for when its your turn. use Player.on("turn") to register a callback for it. """

        # Decode the message
        data = json.loads(msg)
        
        # If a gameOver callback is registed then call it.
        if "gameOver" in self.callbacks:
            self.callbacks["gameOver"](data)

    def on_login_failed(self, msg):
        """ Called if your authentication was incorrect. """

        # if you fail to login just print out the error
        print(msg)
