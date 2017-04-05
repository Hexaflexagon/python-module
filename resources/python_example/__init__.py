from threading import Thread

import __orange__ as API
import GTAOrange.player as Player
import GTAOrange.vehicle as Vehicle
import GTAOrange.blip as Blip
import GTAOrange.text as Text
import GTAOrange.marker as Marker
import GTAOrange.object as Object

def onPlayerConnect(player, ip):
    print('Player:connect | ' + str(player.getName()) + ' | ' + ip)

    return True
    
Player.on("connect", onPlayerConnect)