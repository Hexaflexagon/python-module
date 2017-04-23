"""Python wrapper for GTA Orange's object functions

Subscribable built-in events:
+===============+========================+====================================+
|     name      | object-local arguments |          global arguments          |
+===============+========================+====================================+
| creation      | ---                    | object (Object)                    |
+---------------+------------------------+------------------------------------+
| deletion      | ---                    | object (Object)                    |
+---------------+------------------------+------------------------------------+
"""
import __orange__
from GTAOrange import event as _event

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

    object_ = Object(__orange__.CreateObject(model, x, y, z, pitch, yaw, roll))
    __pool[object_.id] = object_

    trigger("creation", object_)
    return object_


def deleteByID(id):
    """Deletes a object object by the given id.

    @param  id      int     object id

    @returns    bool    True on success, False on failure

    @raises     TypeError   raises if object id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            trigger("deletion", __pool[id])
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
        if _exists(id):
            if id not in __pool.keys():
                __pool[id] = Object(id)
                trigger("creation", __pool[id])
            return __pool[id]
        else:
            return False
    else:
        raise TypeError('Object ID must be an integer')


def getAll():
    """Returns dictionary with all object objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    @returns    dict    object dictionary
    """
    return __pool


def on(event, cb):
    """Subscribes for an event for all markers.

    @param  event   string      event name
    @param  cb      function    callback function
    """
    if event in __ehandlers.keys():
        __ehandlers[event].append(_event.Event(cb))
    else:
        __ehandlers[event] = []
        __ehandlers[event].append(_event.Event(cb))


def trigger(event, *args):
    """Triggers an event for all markers.

    @param  event   string  event name
    @param  *args   *args   arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def _exists(id):
    return True
