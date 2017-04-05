"""Python wrapper for GTA Orange's marker functions

Subscribable built-in events:
+================+=========================+====================================+
|      name      | vehicle-local arguments |          global arguments          |
+================+=========================+====================================+
| playerentered  | player (Player)         | marker (Marker), player (Player)   |
+----------------+-------------------------+------------------------------------+
| playerleft     | player (Player)         | marker (Marker), player (Player)   |
+----------------+-------------------------+------------------------------------+
| vehicleentered | vehicle (Vehicle)       | marker (Marker), vehicle (Vehicle) |
+----------------+-------------------------+------------------------------------+
| vehicleleft    | vehicle (Vehicle)       | marker (Marker), vehicle (Vehicle) |
+----------------+-------------------------+------------------------------------+
| creation       | ---                     | marker (Marker)                    |
+----------------+-------------------------+------------------------------------+
| deletion       | ---                     | marker (Marker)                    |
+----------------+-------------------------+------------------------------------+
"""
import __orange__
from GTAOrange import world as _world
from GTAOrange import event as _event
from GTAOrange import vehicle as _vehicle
from GTAOrange import player as _player

__pool = {}
__ehandlers = {}


class Marker():
    """Marker class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    Attributes:
        id (int): marker id
        x (float): x-coord
        y (float): y-coord
        z (float): z-coord
        h (float): marker height
        r (float): marker radius
    """
    id = None
    x = None
    y = None
    z = None
    h = None
    r = None

    _ehandlers = {}
    _players = {}

    def __init__(self, id, x, y, z, h, r):
        """Initializes a new Marker object.

        Args:
            id (int): marker id
            x (float): x-coord
            y (float): y-coord
            z (float): z-coord
            h (float): marker height
            r (float): marker radius
        """
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.r = r

    def delete(self):
        """Deletes the marker.
        """
        deleteByID(self.id)

    def distanceTo(self, x, y, z=None):
        """Returns the distance from marker to the given coordinates.

        Args:
            x (float): x-coord
            y (float): y-coord
            z (float, optional): z-coord

        Returns:
            float: distance between marker and given coordinates
        """
        if z is not None:
            x1, y1, z1 = self.getPosition()
            return _world.getDistance(x1, y1, z1, x, y, z)
        else:
            x1, y1 = self.getPosition()
            return _world.getDistance(x1, y1, x, y)

    def getID(self):
        """Returns marker id.

        Returns:
            int: marker id
        """
        return self.id

    def getPosition(self):
        """Returns current marker position.

        Returns:
            tuple: position tuple with 3 values
        """
        return (self.x, self.y, self.z)

    def on(self, event, cb):
        """Subscribes for an event only for this marker.

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
        """Triggers an event for the event handlers subscribing to this specific marker.

        Args:
            event (string): event name
            *args: arguments
        """
        if event in self._ehandlers.keys():
            for handler in self._ehandlers[event]:
                handler.getCallback()(self, *args)


def create(x, y, z, h=1, r=1, blip=False):
    """Creates a new marker.

    This is the right way to spawn a new marker.

    Args:
        x (float): x-coord
        y (float): y-coord
        z (float): z-coord
        h (float, optional): marker height
        r (float, optional): marker height
        blip (bool, optional): True if a blip should be created at the marker position, False if not

    Returns:
        GTAOrange.marker.Marker: marker object
    """
    from GTAOrange import blip as _blip
    global __pool

    marker = Marker(__orange__.CreateMarkerForAll(
        x, y, z, h, r), x, y, z, h, r)
    __pool[marker.id] = marker

    if blip is not False:
        marker.blip = _blip.create("Marker", x, y, z)

    trigger("creation", marker)
    return marker


def deleteByID(id):
    """Deletes a marker object by the given id.

    Args:
        id (int): marker id

    Returns:
        bool: True on success, False on failure

    Raises:
        TypeError: raises if marker id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            trigger("deletion", __pool[id])
            del __pool[id]
            return __orange__.DeleteMarker(id)
        else:
            return False
    else:
        raise TypeError('Marker ID must be an integer')


def getByID(id):
    """Returns marker object by given id.

    Args:
        id (int): marker id

    Returns:
        GTAOrange.marker.Marker: marker object (False on failure)

    Raises:
        TypeError: raises if marker id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            return __pool[id]
        return False
    else:
        raise TypeError('Marker ID must be an integer')


def getAll():
    """Returns dictionary with all marker objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    Returns:
        dict: marker dictionary
    """
    return __pool


def on(event, cb):
    """Subscribes for an event for all markers.

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
    """Triggers an event for all markers.

    Args:
        event (string): event name
        *args: arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def _onPlayerEnteredMarker(player_id, marker_id):
    player = _player.getByID(player_id)
    marker = getByID(marker_id)

    trigger("playerentered", marker, player)
    marker.trigger("playerentered", player)
    _player.trigger("enteredmarker", player, marker)
    player.trigger("enteredmarker", marker)


def _onPlayerLeftMarker(player_id, marker_id):
    player = _player.getByID(player_id)
    marker = getByID(marker_id)

    trigger("playerleft", marker, player)
    marker.trigger("playerleft", player)
    _player.trigger("leftmarker", player, marker)
    player.trigger("leftmarker", marker)


def _onVehicleEnteredMarker(vehicle_id, marker_id):
    vehicle = _vehicle.getByID(vehicle_id)
    marker = getByID(marker_id)

    trigger("vehicleentered", marker, vehicle)
    marker.trigger("vehicleentered", vehicle)
    _vehicle.trigger("enteredmarker", vehicle, marker)
    vehicle.trigger("enteredmarker", marker)


def _onVehicleLeftMarker(vehicle_id, marker_id):
    vehicle = _vehicle.getByID(vehicle_id)
    marker = getByID(marker_id)

    trigger("vehicleleft", marker, vehicle)
    marker.trigger("vehicleleft", vehicle)
    _vehicle.trigger("leftmarker", vehicle, marker)
    vehicle.trigger("leftmarker", marker)


__orange__.AddServerEvent(_onPlayerEnteredMarker, "EnterMarker")
__orange__.AddServerEvent(_onPlayerLeftMarker, "LeftMarker")
__orange__.AddServerEvent(_onVehicleEnteredMarker, "VehEnterMarker")
__orange__.AddServerEvent(_onVehicleLeftMarker, "VehLeftMarker")
