"""Python wrapper for GTA Orange's vehicle functions

Subscribable built-in events:
+===============+=========================+====================================+
|     name      | vehicle-local arguments |          global arguments          |
+===============+=========================+====================================+
| playerentered | player (Player)         | vehicle (Vehicle), player (Player) |
+---------------+-------------------------+------------------------------------+
| playerleft    | player (Player)         | vehicle (Vehicle), player (Player) |
+---------------+-------------------------+------------------------------------+
| creation      | ---                     | vehicle (Vehicle)                  |
+---------------+-------------------------+------------------------------------+
| deletion      | ---                     | vehicle (Vehicle)                  |
+---------------+-------------------------+------------------------------------+

Subscribable events from other core libraries:
+===============+=========================+====================================+
|     name      | vehicle-local arguments |          global arguments          |
+===============+=========================+====================================+
| enteredmarker | marker (Marker)         | vehicle (Vehicle), marker (Marker) |
+---------------+-------------------------+------------------------------------+
| leftmarker    | marker (Marker)         | vehicle (Vehicle), marker (Marker) |
+---------------+-------------------------+------------------------------------+
"""
import __orange__
from GTAOrange import world as _world
from GTAOrange import text as _text
from GTAOrange import player as _player
from GTAOrange import event as _event

__pool = {}
__ehandlers = {}

# attachOwnText
# attachOwnBlip


class Vehicle():
    """Vehicle class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    Attributes:
        id (int): vehicle id
        meta (dict): for future releases
        texts (dict): texts added to the vehicle
    """
    id = None
    model = None
    meta = {}
    texts = {}

    _ehandlers = {}

    def __init__(self, id, model=None):
        """Initializes a new Vehicle object.

        Args:
            id (int): vehicle id
        """
        self.id = id
        self.model = model

    def attachBlip(self, name="Vehicle", scale=0.6, color=None, sprite=None):
        """Creates and attaches a blip to the vehicle.

        Args:
            name (str, optional): blip name
            scale (float, optional): blip scale
            color (GTAOrange.blip.Color, optional): blip color (see blip library -> classes at the eof)
            sprite (GTAOrange.blip.Sprite, optional): blip sprite (see blip library -> classes at the eof)

        Returns:
            GTAOrange.blip.Blip: generated blip
        """
        from GTAOrange import blip as _blip

        blip = _blip.create(name, 0, 0, 0, scale, color if color is not None else _blip.Color.ORANGE,
                            sprite if sprite is not None else _blip.Sprite.STANDARD)
        blip.attachTo(self)
        return blip

    def attachText(self, text, x=0, y=0, z=0, tcolor=0xFFFFFFFF, ocolor=0xFFFFFFFF, size=20):
        """Creates and attaches a 3d text to the vehicle.

        Args:
            text (str): text which will be added
            x (int, optional): x-coord
            y (int, optional): y-coord
            z (int, optional): z-coord
            tcolor (int, optional): text color
            ocolor (int, optional): outline color
            size (int, optional): font size

        Returns:
            GTAOrange.text.Text: Description
        """
        txt = _text.create(text, 0, 0, 72, tcolor, ocolor, size)
        txt.attachToVeh(self, x, y, z)
        self.texts[txt.id] = txt

        return txt

    def delete(self):
        """Deletes the vehicle.
        """
        deleteByID(self.id)

    def distanceTo(self, x, y, z=None):
        """Returns the distance from vehicle to the given coordinates.

        Args:
            x (float): x-coord
            y (float): y-coord
            z (float, optional): z-coord

        Returns:
            float: distance between vehicle and given coordinates
        """
        if z is not None:
            x1, y1, z1 = self.getPosition()
            return _world.getDistance(x1, y1, z1, x, y, z)
        else:
            x1, y1 = self.getPosition()
            return _world.getDistance(x1, y1, x, y)

    def getID(self):
        """Returns vehicle id.

        Returns:
            int: vehicle id
        """
        return self.id

    def getModel(self):
        """Returns model string.

        Returns:
            str: model string (e.g. "Burrito") (returns None, when the vehicle wasn't created in Python!)
        """
        return self.model

    def getPosition(self):
        """Returns current vehicle position.

        Returns:
            tuple: position tuple with 3 values
        """
        return __orange__.GetVehiclePosition(self.id)

    def equals(self, veh):
        """Checks if given object IS this object.

        Args:
            veh (GTAOrange.vehicle.Vehicle): vehicle object

        Returns:
            bool: True if it is the object, False if it isn't the object
        """
        if isinstance(veh, Vehicle):
            return self.id == veh.id
        else:
            return False

    def on(self, event, cb):
        """Subscribes for an event only for this vehicle.

        Args:
            event (string): event name
            cb (function): callback function
        """
        if event in self._ehandlers.keys():
            self._ehandlers[event].append(_event.Event(cb))
        else:
            self._ehandlers[event] = []
            self._ehandlers[event].append(_event.Event(cb))

    def trigger(self, event, *args):
        """Triggers an event for the event handlers subscribing to this specific vehicle.

        Args:
            event (string): event name
            *args: arguments
        """
        if event in self._ehandlers.keys():
            for handler in self._ehandlers[event]:
                handler.getCallback()(self, *args)


def create(model, x, y, z, h):
    """Creates a new vehicle.

    This is the right way to spawn a new vehicle.

    Args:
        model (str OR int): model name OR hash
        x (float): x-coord
        y (float): y-coord
        z (float): z-coord
        h (float): heading

    Returns:
        GTAOrange.vehicle.Vehicle: vehicle object
    """
    veh = Vehicle(__orange__.CreateVehicle(model, x, y, z, h), model)
    __pool[veh.id] = veh

    trigger("creation", veh)
    return veh


def deleteByID(id):
    """Deletes a vehicle object by the given id.

    Args:
        id (int): vehicle id

    Returns:
        bool: True on success, False on failure

    Raises:
        TypeError: raises if vehicle id is not int
    """
    global __pool

    if isinstance(id, int):
        if exists(id):
            if id in __pool.keys():
                trigger("deletion", __pool[id])
                del __pool[id]

            return __orange__.DeleteVehicle(id)
        return False
    else:
        raise TypeError('Vehicle ID must be an integer')


def exists(id):
    """Checks if a vehicle with the given id exists internally.

    TODO: Unimplemented atm.

    Args:
        id (int): vehicle id

    Returns:
        bool: True on yes, False on no
    """
    # return __orange__.VehicleExists(id)
    return True


def getByID(id):
    """Returns vehicle object by given id.

    Args:
        id (int): vehicle id

    Returns:
        GTAOrange.vehicle.Vehicle: vehicle object (False on failure)

    Raises:
        TypeError: raises if vehicle id is not int
    """
    global __pool

    if isinstance(id, int):
        if exists(id):
            if id not in __pool.keys():
                __pool[id] = Vehicle(id)

                # TODO: this is a dirty workaround
                trigger("creation", __pool[id])
            return __pool[id]
        return False
    else:
        raise TypeError('Vehicle ID must be an integer')


def getAll():
    """Returns dictionary with all vehicle objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    Returns:
        dict: vehicle dictionary
    """
    return __pool


def on(event, cb):
    """Subscribes for an event for all vehicles.

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
    """Triggers an event for all vehicles.

    Args:
        event (string): event name
        *args: arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def _onPlayerEntered(player_id, vehicle_id):
    player = _player.getByID(player_id)
    vehicle = getByID(vehicle_id)

    trigger("playerentered", vehicle, player)
    vehicle.trigger("playerentered", player)
    _player.trigger("enteredvehicle", player, vehicle)
    player.trigger("enteredvehicle", vehicle)


def _onPlayerLeft(player_id, vehicle_id):
    player = _player.getByID(player_id)
    vehicle = getByID(vehicle_id)

    trigger("playerleft", vehicle, player)
    vehicle.trigger("playerleft", player)
    _player.trigger("leftvehicle", player, vehicle)
    player.trigger("leftvehicle", vehicle)


__orange__.AddServerEvent(_onPlayerEntered, "EnterVehicle")
__orange__.AddServerEvent(_onPlayerLeft, "LeftVehicle")
