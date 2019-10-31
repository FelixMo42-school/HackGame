import socketio
import json
import random

class Player(socketio.ClientNamespace):
    def __init__(self, username=input("enter username: "), password=input("enter password: ")):
        super().__init__("/2048")

        self.username = username
        self.password = password

        self.callbacks = {}

    def on_connect(self):
        if "gameStart" in self.callbacks:
            self.callbacks["gameStart"]()

    def on_turn(self, msg):
        data = json.loads(msg)

        self.emit("turn", json.dumps(
            self.callbacks["turn"](data)
        ))

    def on_end(self, msg):
        data = json.loads(msg)
        
        if "gameOver" in self.callbacks:
            self.callbacks["gameOver"](data)
        
    def on(self, event):
        def decorator(func):
            self.callbacks[event] = func
            return func

        return decorator

    def startGame(self):
        if "turn" in self.callbacks:
            sio=socketio.Client(reconnection=False)
            sio.register_namespace(self)

            sio.connect("https://berkeley-hackclub-game.herokuapp.com", {
                "username": self.username,
                "password": self.password,
                
            }, ['websocket'])

            sio.wait()
        else:
            print("Must have an turn callback to play game.")
