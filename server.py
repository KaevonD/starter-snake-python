import os
import copy
import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Snakinator",
            "color": "#999999",
            "head": "pixel",
            "tail": "pixel",
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):

        data = cherrypy.request.json
        allMoves = ["up", "right", "down", "left"]
        foodX = data['board']['food'][0]['x']
        foodY = data['board']['food'][0]['y']

        headX = data['you']['head']['x']
        headY = data['you']['head']['y']

        # take in data, returns impossible moves
        surrounding = []
        cantMove = []
        for i in range(4):
            temp = copy.copy(data['you']['head'])
            if (i == 1):
                temp['y'] -= 1
                if (temp['y'] < 0):
                    cantMove.append("up")
            elif (i == 2):
                temp['x'] += 1
                if (temp['x'] > 10):
                    cantMove.append("right")
            elif (i == 3):
                temp['y'] += 1
                if (temp['y'] > 10):
                    cantMove.append("down")
            else:
                temp['x'] -= 1
                if (temp['x'] < 0):
                    cantMove.append("left")

            surrounding.append(temp)

        for snake in data['board']['snakes']:
            for i in range(4):
                if (surrounding[i] in snake['body']):
                    if (i == 1):
                        if ("up" not in cantMove):
                            cantMove.append("up")
                    elif (i == 2):
                        if ("right" not in cantMove):
                            cantMove.append("right")
                    elif (i == 3):
                        if ("down" not in cantMove):
                            cantMove.append("down")
                    else:
                        if ("left" not in cantMove):
                            cantMove.append("left")

        if (headX <= foodX and headY <= foodY):
            if (headX == foodX):
                move = "down"
            else:
                move = "right"
        elif (headX <= foodX and headY >= foodY):
            if (headX == foodX):
                move = "up"
            else:
                move = "right"
        elif (headX >= foodX and headY >= foodY):
            if (headX == foodX):
                move = "up"
            else:
                move = "left"
        else:
            if (headX == foodX):
                move = "down"
            else:
                move = "left"

        if (move in cantMove):
            for i in allMoves:
                if (i not in cantMove):
                    move = i
                    break

        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
