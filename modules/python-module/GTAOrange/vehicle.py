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

    @attr   id      int     vehicle id
    @attr   meta    dict    for future releases
    @attr   texts   dict    texts added to the vehicle
    """
    id = None
    model = None
    meta = {}
    texts = {}

    _ehandlers = {}

    def __init__(self, id, model=None):
        """Initializes a new Vehicle object.

        @param  id      int     vehicle id
        """
        self.id = id
        self.model = model

    def attachBlip(self, name="Vehicle", scale=0.6, color=None, sprite=None):
        """Creates and attaches a blip to the vehicle.

        @param  name    str                     blip name #optional
        @param  scale   float                   blip scale #optional
        @param  color   GTAOrange.blip.Color    blip color (see blip library -> classes at the eof) #optional
        @param  sprite  GTAOrange.blip.Sprite   blip sprite (see blip library -> classes at the eof) #optional

        @returns    GTAOrange.blip.Blip     generated blip
        """
        from GTAOrange import blip as _blip

        blip = _blip.create(name, 0, 0, 0, scale, color if color is not None else _blip.Color.ORANGE,
                            sprite if sprite is not None else _blip.Sprite.STANDARD)
        blip.attachTo(self)
        return blip

    def attachText(self, text, x=0, y=0, z=0, tcolor=0xFFFFFFFF, ocolor=0xFFFFFFFF, size=20):
        """Creates and attaches a 3d text to the vehicle.

        @param  text    str     text which will be added
        @param  x       int     x-coord #optional
        @param  y       int     y-coord #optional
        @param  z       int     z-coord #optional
        @param  tcolor  int     text color #optional
        @param  ocolor  int     outline color #optional
        @param  size    int     font size #optional

        @returns    GTAOrange.text.Text     text object
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

        @param  x       float   x-coord
        @param  y       float   y-coord
        @param  z       float   z-coord #optional

        @returns    float   distance between vehicle and given coordinates
        """
        if z is not None:
            x1, y1, z1 = self.getPosition()
            return _world.getDistance(x1, y1, z1, x, y, z)
        else:
            x1, y1 = self.getPosition()
            return _world.getDistance(x1, y1, x, y)

    def equals(self, veh):
        """Checks if given object IS this object.

        @param  veh     GTAOrange.vehicle.Vehicle   vehicle object

        @returns    bool    True if it is the object, False if it isn't the object
        """
        if isinstance(veh, Vehicle):
            return self.id == veh.id
        else:
            return False

    def getColors(self):
        """Returns a tuple with the vehicle colors.

        @returns    tuple   color tuple with 2 GTAOrange.hash.VehicleColor objects
        """
        return __orange__.GetVehicleColours(self.id)

    def getDriver(self):
        """Returns driver's player id.

        @returns    int OR None     player id of driver (or None on failure)
        """
        driver = __orange__.GetVehicleDriver(self.id)

        if driver is not None:
            return getByID(driver)

        return driver

    def getID(self):
        """Returns vehicle id.

        @returns    int     vehicle id
        """
        return self.id

    def getModel(self):
        """Returns model string.

        @returns    str     model string (e.g. "Burrito") (returns None, when the vehicle wasn't created in Python!)
        """
        return self.model

    def getOccupants(self):
        """Returns a list of the occupants currently sitting in the vehicle, including the driver.

        @returns    list    list with all the passengers
        """
        occupant_list = __orange__.GetVehiclePassengers(self.id)

        # check first if this is an int, because most of the time only the driver is in the car
        if isinstance(occupant_list, int):
            return [getByID(occupant_list)]
        else:
            occupants = []

            for occupant in occupant_list:
                occupants.append(getByID(occupant))

            return occupants

    def getPassengers(self):
        """Returns a list of passengers currently sitting in the vehicle, NOT including the driver (since passengers are defined as not taking any responsibility for the car, actually).

        @returns    list    list with all the passengers
        """
        passengers = self.getOccupants()
        driver = self.getDriver()

        if driver in passengers:
            passengers.remove(driver)

        return passengers

    def getPosition(self):
        """Returns current vehicle position.

        @returns    tuple   position tuple with 3 float values
        """
        return __orange__.GetVehiclePosition(self.id)

    def getRotation(self):
        """Returns current vehicle rotation.

        @returns    tuple   rotation tuple with 3 float values
        """
        return __orange__.GetVehicleRotation(self.id)

    def on(self, event, cb):
        """Subscribes for an event only for this vehicle.

        @param  event   string      event name
        @param  cb      function    callback function
        """
        if event in self._ehandlers.keys():
            self._ehandlers[event].append(_event.Event(cb))
        else:
            self._ehandlers[event] = []
            self._ehandlers[event].append(_event.Event(cb))

    def setColors(self, color1, color2):
        """Sets vehicle colors.

        @param  color1  GTAOrange.hash.VehicleColor     first color
        @param  color2  GTAOrange.hash.VehicleColor     second color
        """
        return __orange__.SetVehicleColours(self.id, color1, color2)

    def setPosition(self, x, y, z):
        """Sets position.

        @param  x   float   x-coord
        @param  y   float   y-coord
        @param  z   float   z-coord
        """
        return __orange__.SetVehiclePosition(self.id, x, y, z)

    def setRotation(self, rx, ry, rz):
        """Sets rotation.

        @param  rx  float   rotation in x direction
        @param  ry  float   rotation in y direction
        @param  rz  float   rotation in z direction
        """
        return __orange__.SetVehicleRotation(self.id, rx, ry, rz)

    def trigger(self, event, *args):
        """Triggers an event for the event handlers subscribing to this specific vehicle.

        @param  event   string  event name
        @param  *args   *args   arguments
        """
        if event in self._ehandlers.keys():
            for handler in self._ehandlers[event]:
                handler.getCallback()(self, *args)


def create(model, x, y, z, h):
    """Creates a new vehicle.

    This is the right way to spawn a new vehicle.

    @param  model   str OR int  model name OR hash
    @param  x       float       x-coord
    @param  y       float       y-coord
    @param  z       float       z-coord
    @param  h       float       heading

    @returns    GTAOrange.vehicle.Vehicle   vehicle object
    """
    veh = Vehicle(__orange__.CreateVehicle(model, x, y, z, h), model)
    __pool[veh.id] = veh

    trigger("creation", veh)
    return veh


def deleteByID(id):
    """Deletes a vehicle object by the given id.

    @param  id      int     vehicle id

    @returns    bool    True on success, False on failure

    @raises     TypeError   raises if vehicle id is not int
    """
    global __pool

    if isinstance(id, int):
        if _exists(id):
            if id in __pool.keys():
                trigger("deletion", __pool[id])
                del __pool[id]

            return __orange__.DeleteVehicle(id)
        return False
    else:
        raise TypeError('Vehicle ID must be an integer')


def getByID(id):
    """Returns vehicle object by given id.

    @param  id      int     vehicle id

    @returns    GTAOrange.vehicle.Vehicle   vehicle object (False on failure)

    @raises     TypeError   raises if vehicle id is not int
    """
    global __pool

    if isinstance(id, int):
        if _exists(id):
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

    @returns    dict    vehicle dictionary
    """
    return __pool


def on(event, cb):
    """Subscribes for an event for all vehicles.

    @param  event   string      event name
    @param  cb      function    callback function
    """
    if event in __ehandlers.keys():
        __ehandlers[event].append(_event.Event(cb))
    else:
        __ehandlers[event] = []
        __ehandlers[event].append(_event.Event(cb))


def trigger(event, *args):
    """Triggers an event for all vehicles.

    @param  event   string  event name
    @param  *args   *args   arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def _exists(id):
    # return __orange__.VehicleExists(id)
    return True

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
