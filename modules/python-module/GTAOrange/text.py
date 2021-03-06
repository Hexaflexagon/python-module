"""Python wrapper for GTA Orange's 3d text functions

Subscribable built-in events:
+===============+======================+====================================+
|     name      | text-local arguments |          global arguments          |
+===============+======================+====================================+
| creation      | ---                  | text (Text)                        |
+---------------+----------------------+------------------------------------+
| deletion      | ---                  | text (Text)                        |
+---------------+----------------------+------------------------------------+
"""
import __orange__
from GTAOrange import event as _event

__pool = {}
__ehandlers = {}


class Text():
    """Text class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    @attr   id      int                     text id
    @attr   ocolor  GTAOrange.color.Color   outline color
    @attr   size    float                   font size
    @attr   tcolor  GTAOrange.color.Color   text color
    @attr   x       float                   x-coord
    @attr   y       float                   y-coord
    @attr   z       float                   z-coord
    """
    id = None
    x = None
    y = None
    z = None
    tcolor = None
    ocolor = None
    size = None

    _ehandlers = {}

    def __init__(self, id, text, x, y, z, tcolor=0xFFFFFFFF, ocolor=0xFFFFFFFF, size=20):
        """Initializes a new Text object.

        @param  id      int                     text id
        @param  text    str                     message string
        @param  x       float                   x-coord
        @param  y       float                   y-coord
        @param  z       float                   z-coord
        @param  tcolor  GTAOrange.color.Color   text color #optional
        @param  ocolor  GTAOrange.color.Color   outline color #optional
        @param  size    float                   font size #optional
        """
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.tcolor = tcolor
        self.ocolor = ocolor
        self.size = size
        self.text = text

    def delete(self):
        """Deletes the text.
        """
        deleteByID(self.id)

    def getID(self):
        """Returns text id.

        @returns    int     text id
        """
        return self.id

    def getPosition(self):
        """Returns current position.

        @returns    tuple   position tuple with 3 values
        """
        return (self.x, self.y, self.z)

    def getColors(self):
        """Returns current colors.

        @returns    tuple   two elements, first is text color, second is outline color
        """
        return (self.tcolor, self.ocolor)

    def getSize(self):
        """Returns current size.

        @returns    float   size
        """
        return self.size

    def getText(self):
        """Returns current text.

        @returns    str     message string
        """
        return self.text


def create(text, x, y, z, tcolor=0xFFFFFFFF, ocolor=0xFFFFFFFF, size=20):
    """Creates a new 3d text.

    This is the right way to spawn a new text.

    @param  text    str                     message string
    @param  x       float                   x-coord
    @param  y       float                   y-coord
    @param  z       float                   z-coord
    @param  tcolor  GTAOrange.color.Color   text color #optional
    @param  ocolor  GTAOrange.color.Color   outline color #optional
    @param  size    float                   font size #optional

    @returns    GTAOrange.text.Text     text object
    """
    global __pool

    text = Text(__orange__.Create3DTextForAll(text, x, y, z, tcolor,
                                              ocolor, size), text, x, y, z, tcolor, ocolor, size)
    __pool[text.id] = text

    trigger("creation", text)
    return text


def deleteByID(id):
    """Deletes a text object by the given id.

    @param  id      int     text id

    @returns    bool    True on success, False on failure

    @raises     TypeError   raises if text id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            trigger("deletion", __pool[id])
            del __pool[id]
        return __orange__.Delete3DText(id)
    else:
        raise TypeError('3DText ID must be an integer')


def getByID(id):
    """Returns text object by given id.

    @param  id      int     text id

    @returns    GTAOrange.text.Text     text object (False on failure)

    @raises     TypeError   raises if text id is not int
    """
    global __pool

    if isinstance(id, int):
        if _exists(id):
            if id not in __pool.keys():
                __pool[id] = Text(id)
                trigger("creation", __pool[id])
            return __pool[id]
        else:
            return False
    else:
        raise TypeError('Text ID must be an integer')


def getAll():
    """Returns dictionary with all text objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    @returns    dict    text dictionary
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
