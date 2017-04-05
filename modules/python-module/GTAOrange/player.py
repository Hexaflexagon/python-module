"""Python wrapper for GTA Orange's player functions

Subscribable built-in events:
+============+========================+===================================+
|    name    | player-local arguments |         global arguments          |
+============+========================+===================================+
| connect    | ip (string)            | player (Player), ip (string)      |
+------------+------------------------+-----------------------------------+
| disconnect | reason (int)           | player (Player), reason (int)     |
+------------+------------------------+-----------------------------------+
| command    | arguments (list)       | player (Player), arguments (list) |
+------------+------------------------+-----------------------------------+

Subscribable events from other core libraries:
+================+========================+====================================+
|      name      | player-local arguments |          global arguments          |
+================+========================+====================================+
| enteredvehicle | vehicle (Vehicle)      | player (Player), vehicle (Vehicle) |
+----------------+------------------------+------------------------------------+
| leftvehicle    | vehicle (Vehicle)      | player (Player), vehicle (Vehicle) |
+----------------+------------------------+------------------------------------+
| enteredmarker  | marker (Marker)        | player (Player), marker (Marker)   |
+----------------+------------------------+------------------------------------+
| leftmarker     | marker (Marker)        | player (Player), marker (Marker)   |
+----------------+------------------------+------------------------------------+
"""
import __orange__
from GTAOrange import world as _world
from GTAOrange import event as _event

__pool = {}
__ehandlers = {}

# attachOwnBlip


class Player():
    """Player class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    Attributes:
        id (int): player id
        meta (dict): for future releases
    """
    id = None
    meta = {}

    _ehandlers = {}

    def __init__(self, id):
        """Initializes a new Player object.

        Args:
            id (id): player id
        """
        self.id = id

    def attachBlip(self, name="Player", scale=1, color=None, sprite=None):
        """Creates a blip and attaches it to the player afterwards.

        Args:
            name (str, optional): blip name
            scale (int, optional): blip scale
            color (GTAOrange.blip.Color, optional): blip color (see blip library -> classes at the eof)
            sprite (GTAOrange.blip.Sprite, optional): blip sprite (see blip library -> classes at the eof)

        Returns:
            Blip: generated blip
        """
        from GTAOrange import blip as _blip

        blip = _blip.create(name, 0, 0, 0, scale, color if color is not None else _blip.Color.ORANGE,
                            sprite if sprite is not None else _blip.Sprite.STANDARD)
        blip.attachTo(self)
        return blip

    def createBlip(self, name, x, y, z, scale=1, color=None, sprite=None):
        """Creates a blip which only the player can see.

        TODO: Needs rewrite, when the blip lib is able to handle player-local blips.

        Args:
            name (string): blip name
            x (float): x-coord of blip
            y (float): y-coord of blip
            z (float): z-coord of blip
            scale (int, optional): blip scale
            color (GTAOrange.blip.Color, optional): blip color (see blip library -> classes at the eof)
            sprite (GTAOrange.blip.Sprite, optional): blip sprite (see blip library -> classes at the eof)

        Returns:
            int: blip id
        """
        from GTAOrange import blip as _blip
        return __orange__.CreateBlipForPlayer(self.id, name, x, y, z, scale, color if color is not None else _blip.Color.ORANGE, sprite if sprite is not None else _blip.Sprite.STANDARD)

    def distanceTo(self, x, y, z=None):
        """Returns the distance from player to the given coordinates.

        Args:
            x (float): x-coord
            y (float): y-coord
            z (float, optional): z-coord

        Returns:
            float: distance between player and given coordinates
        """
        if z is None:
            x1, y1, z1 = self.getPosition()
            return _world.getDistance(x1, y1, z1, x, y, z)
        else:
            x1, y1 = self.getPosition()
            return _world.getDistance(x1, y1, x, y)

    def getHeading(self):
        """Returns player heading.

        Returns:
            float: player heading
        """
        return __orange__.GetPlayerHeading(self.id)

    def getID(self):
        """Returns player id.

        Returns:
            int: player id
        """
        return self.id

    def getModel(self):
        """Returns current model.

        Returns:
            int: model hash
        """
        return __orange__.GetPlayerModel(self.id)

    def getName(self):
        """Returns current name.

        Returns:
            string: current name
        """
        return __orange__.GetPlayerName(self.id)

    def getPosition(self):
        """Returns current position.

        Returns:
            tuple: position tuple with 3 values
        """
        return __orange__.GetPlayerPosition(self.id)

    def getMoney(self):
        """Returns current money value the player is having.

        Returns:
            int: money value
        """
        return __orange__.GetPlayerMoney(self.id)

    def getHealth(self):
        """Returns current health.

        Returns:
            float: current health
        """
        return __orange__.GetPlayerHealth(self.id)

    def giveWeapon(self, weapon, ammo=None):
        """Gives weapon to player.

        Args:
            weapon (int): weapon hash
            ammo (int, optional): ammo amount
        """
        if ammo is None:
            __orange__.GivePlayerWeapon(self.id, weapon, 100)
        else:
            __orange__.GivePlayerWeapon(self.id, weapon, ammo)

    def isInMarker(self, marker):
        """Checks if a player is in a marker.

        Args:
            marker (GTAOrange.marker.Marker): marker

        Returns:
            bool: True for yes, False for no
        """
        x1, y1, z1 = self.getPosition()
        x2, y2, z2 = marker.getPosition()

        return _world.getDistance(x1, y1, x2, y2) < 0.5 and (z1 - z2) * (z1 - z2) < (0.5 * 0.5)

    def removeWeapons(self):
        """Removes all weapons from a player.
        """
        __orange__.RemovePlayerWeapons(self.id)

    def on(self, event, cb):
        """Subscribes for an event only for this player.

        Args:
            event (string): event name
            cb (function): callback function
        """
        if event in self._ehandlers.keys():
            self._ehandlers[event].append(_event.Event(cb))
        else:
            self._ehandlers[event] = []
            self._ehandlers[event].append(_event.Event(cb))

    def sendNotification(self, msg):
        """Sends a notification to the player.

        Args:
            msg (string): message string
        """
        __orange__.SendPlayerNotification(self.id, msg)

    def chatMsg(self, msg):
        """Sends a chat message to the player.

        Args:
            msg (string): message string
        """
        __orange__.SendClientMessage(self.id, "{FFFFFF}" + msg, 255)

    def setArmour(self, armour):
        """Sets armour.

        Args:
            armour (float): armour value
        """
        __orange__.SetPlayerArmour(self.id, armour)

    def setHeading(self, heading):
        """Sets heading (direction where the player is looking)

        Args:
            heading (float): heading
        """
        __orange__.SetPlayerHeading(self.id, heading)

    def setHealth(self, health):
        """Sets health.

        Args:
            health (float): health value
        """
        __orange__.SetPlayerHealth(self.id, health)

    def setName(self, name):
        """Sets current name.

        Args:
            name (string): name string
        """
        __orange__.SetPlayerName(self.id, name)

    def setInfoMsg(self, msg=None):
        """Sets info message for player.

        Args:
            msg (string, optional): message string
        """
        if msg is None:
            __orange__.UnsetInfoMsg(self.id)
        else:
            __orange__.SetInfoMsg(self.id, msg)

    def setIntoVeh(self, veh, seat=None):
        """Sets player into given vehicle.

        Args:
            veh (GTAOrange.vehicle.Vehicle): vehicle object
            seat (int, optional): seat number
        """
        if seat is None:
            __orange__.SetPlayerIntoVehicle(self.id, veh.id, -1)
        else:
            __orange__.SetPlayerIntoVehicle(self.id, veh.id, seat)

    def setModel(self, model):
        """Sets current model.

        Args:
            model (int): model hash
        """
        __orange__.SetPlayerModel(self.id, model)

    def setPosition(self, x, y, z):
        """Sets position.

        Args:
            x (float): x-coord
            y (float): y-coord
            z (float): z-coord
        """
        __orange__.SetPlayerPosition(self.id, x, y, z)

    def setMoney(self, money):
        """Sets current money the player is having.

        Args:
            money (int): money value
        """
        __orange__.SetPlayerMoney(self.id, money)

    def resetMoney(self):
        """Resets money to zero.
        """
        __orange__.ResetPlayerMoney(self.id)

    def giveMoney(self, money):
        """Gives specific amount of money (addition).

        Args:
            money (int): money value
        """
        __orange__.GivePlayerMoney(self.id, money)

    def giveAmmo(self, weapon, ammo):
        """Gives ammo to player.

        Args:
            weapon (int): weapon hash
            ammo (int): ammo amount
        """
        __orange__.GivePlayerAmmo(self.id, weapon, ammo)

    def broadcast(self, msg, color):
        """Broadcasts a message to the player.

        Args:
            msg (string): message string
            color (GTAOrange.color.Color): message color
        """
        broadcast(msg, color)

    def disableHUD(self):
        """Disables the HUD of the player.
        """
        __orange__.DisablePlayerHud(self.id, True)

    def enableHUD(self):
        """Enables the HUD of the player.
        """
        __orange__.DisablePlayerHud(self.id, False)

    def trigger(self, event, *args):
        """Triggers an event for the event handlers subscribing to this specific player.

        Args:
            event (string): event name
            *args: arguments
        """
        if event in self._ehandlers.keys():
            for handler in self._ehandlers[event]:
                handler.getCallback()(self, *args)

    def triggerClient(self, event, *args):
        """Triggers a client event for the player.

        Args:
            event (string): event name
            *args: arguments
        """
        __orange__.TriggerClientEvent(self.id, event, list(args))


def broadcast(msg, color):
    """Broadcasts a message to all players.

    Args:
        msg (string): message string
        color (GTAOrange.color.Color): message color
    """
    __orange__.BroadcastClientMessage(msg, color)


def exists(id):
    """Checks if a player with the given id exists internally.

    TODO: Unimplemented atm.

    Args:
        id (int): player id

    Returns:
        bool: True on yes, False on no
    """
    # return __orange__.PlayerExists(id)
    return True


def getByID(id):
    """Returns player object by given id.

    Args:
        id (int): player id

    Returns:
        GTAOrange.player.Player: player object (False on failure)

    Raises:
        TypeError: raises if player id is not int
    """
    global __pool

    if isinstance(id, int):
        if exists(id):
            if id not in __pool.keys():
                __pool[id] = Player(id)
            return __pool[id]
        else:
            return False
    else:
        raise TypeError('Player ID must be an integer')


def getByName(name):
    """Returns player object by its name.

    Args:
        name (string): player name

    Returns:
        GTAOrange.player.Player: player object (False on failure)
    """
    for player in __pool.values():
        if player.getName() == name:
            return player
    return False


def getAll():
    """Returns dictionary with all player objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    Returns:
        dict: player dictionary
    """
    return __pool


def on(event, cb):
    """Subscribes for an event for all players.

    Args:
        event (string): event name
        cb (function): callback function
    """
    if event in __ehandlers.keys():
        __ehandlers[event].append(_event.Event(cb))
    else:
        __ehandlers[event] = []
        __ehandlers[event].append(_event.Event(cb))


def trigger(event, *args):
    """Triggers an event for all players.

    Args:
        event (string): event name
        *args: arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def triggerClient(event, *args):
    """Triggers a client event for all players.

    Args:
        event (string): event name
        *args: arguments
    """
    __orange__.TriggerClientEvent(-1, event, list(args))


def _onConnect(player_id, ip):
    player = getByID(player_id)

    trigger("connect", player, ip)
    player.trigger("connect", ip)


def _onDisconnect(player_id, reason):
    global __pool
    player = getByID(player_id)

    trigger("disconnect", player, reason)
    player.trigger("connect", reason)

    del __pool[player_id]


def _onCommand(*args):
    # replace first arg (player id) with player obj
    args = list(args)
    player = getByID(args[0])
    del args[0]

    trigger("command", player, *args)
    player.trigger("connect", *args)


__orange__.AddServerEvent(_onConnect, "PlayerConnect")
__orange__.AddServerEvent(_onDisconnect, "PlayerDisconnect")
__orange__.AddServerEvent(_onCommand, "PlayerCommand")
