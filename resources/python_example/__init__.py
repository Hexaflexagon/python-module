# NATIVE IMPORTS

import time
from threading import Thread

# GTAORANGE IMPORTS

import GTAOrange.player as Player
import GTAOrange.vehicle as Vehicle

# PRIVATE FUNCTIONS

def _sendPlayerList(target):
    players = Player.getAll()
    target.chatMsg("Players:")

    for player in players.values():
        target.chatMsg(player.getName())


def _threadTest():
    i = 0

    while True:

        print(i)
        i += 1

        time.sleep(1000)

# EVENT HANDLERS

def _onPlayerConnect(player, ip):
    print('Player:connect | ' + str(player.getName()) + ' | ' + ip)

    # on first spawn
    player.setPosition(100.0, -1940.0, 21.0)

    # ofc you can define own attributes, as long as they don't replace each other
    player.testveh = None

def _onPlayerDisconnect(player, reason):
    print('Player:disconnect | ' + str(player.getID()) + ' | ' + str(reason))

def _onPlayerCommand(player, command):
    print("command")
    command = command.split()

    # player commands

    if command[0] == "/setpos":
        player.setPosition(float(command[1]), float(
            command[2]), float(command[3]))

    elif command[0] == "/players":
        _sendPlayerList(player)

    elif command[0] == "/getpos":
        # chat
        x, y, z = player.getPosition()
        player.chatMsg("{:.9f}".format(x) + "|" +
                       "{:.9f}".format(y) + "|" + "{:.9f}".format(z))

        # server console
        coords = player.getPosition()
        print(coords)

    # thread example

    elif command[0] == "/thread":
        t = Thread(target=_threadTest)
        t.daemon = True
        t.start()

    # vehicle commands

    elif command[0] == "/veh":

        # spawns a Burrito at your position
        if command[1] == "create":
            if player.testveh is None:
                x, y, z = player.getPosition()

                player.testveh = Vehicle.create(
                    "Burrito", x, y, z, player.getHeading())
                player.setIntoVeh(player.testveh)

                player.chatMsg("Created a Burrito! :-) | ID: " +
                               str(player.testveh.id))
            else:
                player.chatMsg("Please delete your car before!")

        # deletes the Burrito you've spawned
        elif command[1] == "delete":
            if player.testveh is not None:
                player.testveh.delete()
                player.testveh = None
            else:
                player.chatMsg("Please create a car before!")

        # sends position of Burrito to chat and server console
        elif command[1] == "getpos":
            if player.testveh is not None:
                # chat
                x, y, z = player.testveh.getPosition()
                player.chatMsg("{:.9f}".format(x) + "|" + "{:.9f}".format(y) + "|" + "{:.9f}".format(z))

                # server console
                val = player.testveh.getPosition()
                print(val)
            else:
                player.chatMsg("Please create a car before!")

    else:
        print(' '.join(command))

    return True


def _onPlayerEnteredVehicle(player, veh):
    print('Vehicle:playerentered | ' +
          str(player.getID()) + ' | ' + str(veh.getID()))


def _onPlayerLeftVehicle(player, veh):
    print('Vehicle:playerleft | ' + str(player.getID()) + ' | ' + str(veh.getID()))


# REGISTER EVENT HANDLERS

Player.on("connect", _onPlayerConnect)
Player.on("disconnect", _onPlayerDisconnect)
Player.on("command", _onPlayerCommand)

Vehicle.on("playerentered", _onPlayerEnteredVehicle)
Vehicle.on("playerleft", _onPlayerLeftVehicle)
