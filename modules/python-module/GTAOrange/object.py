"""Python wrapper for GTA Orange's object functions
"""
import __orange__

__pool = {}
__ehandlers = {}


class Object():
    """Object class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    @param  id      int     object id
    """
    id = None

    _ehandlers = {}

    def __init__(self, id):
        """Initializes a new Object object.

        @param  id      int     object id
        """
        self.id = id

    def delete(self):
        """Deletes the object.
        """
        deleteByID(self.id)

    def getID(self):
        """Returns object id.

        @returns    int     object id
        """
        return self.id

    def equals(self, obj):
        """Checks if given object IS this object.

        @param  obj     GTAOrange.object.Object     object object

        @returns    bool    True if it is the object, False if it isn't the object
        """
        if isinstance(obj, Object):
            return self.id == obj.id
        else:
            return False


def create(model, x, y, z, pitch, yaw, roll):
    """Creates a new object.

    This is the right way to spawn a new object.

    @param  model   str OR int  model name OR hash
    @param  x       float       x-coord
    @param  y       float       y-coord
    @param  z       float       z-coord
    @param  pitch   float       pitch angle (y rotation)
    @param  yaw     float       yaw angle (z rotation, heading)
    @param  roll    float       roll angle (x rotation)

    @returns    GTAOrange.object.Object     object object
    """
    global __pool

    object = Object(__orange__.CreateObject(model, x, y, z, pitch, yaw, roll))
    __pool[object.id] = object
    return object


def deleteByID(id):
    """Deletes a object object by the given id.

    @param  id      int     object id

    @returns    bool    True on success, False on failure

    @raises     TypeError   raises if object id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            del __pool[id]
            return __orange__.DeleteObject(id)
        else:
            return False
    else:
        raise TypeError('Object ID must be an integer')


def getByID(id):
    """Returns object object by given id.

    @param  id      int     object id

    @returns    GTAOrange.object.Object     object object (False on failure)

    @raises     TypeError   raises if object id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            return __pool[id]
        return False
    else:
        raise TypeError('Object ID must be an integer')


def getAll():
    """Returns dictionary with all object objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    @returns    dict    object dictionary
    """
    return __pool
