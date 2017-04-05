"""Python wrapper for GTA Orange's 3d text functions
"""
import __orange__
__pool = {}


class Text():
    """Text class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    Attributes:
        id (int): text id
        ocolor (GTAOrange.color.Color): outline color
        size (float): font size
        tcolor (GTAOrange.color.Color): text color
        x (float): x-coord
        y (float): y-coord
        z (float): z-coord
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

        Args:
            id (int): text id
            text (str): message string
            x (float): x-coord
            y (float): y-coord
            z (float): z-coord
            tcolor (GTAOrange.color.Color, optional): text color
            ocolor (GTAOrange.color.Color, optional): outline color
            size (float, optional): font size
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

        Returns:
            int: text id
        """
        return self.id

    def getPosition(self):
        """Returns current position.

        Returns:
            tuple: position tuple with 3 values
        """
        return (self.x, self.y, self.z)

    def getColors(self):
        """Returns current colors.

        Returns:
            tuple: two elements, first is text color, second is outline color
        """
        return (self.tcolor, self.ocolor)

    def getSize(self):
        """Returns current size.

        Returns:
            float: size
        """
        return self.size

    def getText(self):
        """Returns current text.

        Returns:
            str: message string
        """
        return self.text


def create(text, x, y, z, tcolor=0xFFFFFFFF, ocolor=0xFFFFFFFF, size=20):
    """Creates a new 3d text.

    This is the right way to spawn a new text.

    Args:
        text (str): message string
        x (float): x-coord
        y (float): y-coord
        z (float): z-coord
        tcolor (GTAOrange.color.Color, optional): text color
        ocolor (GTAOrange.color.Color, optional): outline color
        size (float, optional): font size

    Returns:
        GTAOrange.text.Text: text object
    """
    global __pool

    text = Text(__orange__.Create3DTextForAll(text, x, y, z, tcolor,
                                              ocolor, size), text, x, y, z, tcolor, ocolor, size)
    __pool[text.id] = text
    return text


def deleteByID(id):
    """Deletes a text object by the given id.

    Args:
        id (int): text id

    Returns:
        bool: True on success, False on failure

    Raises:
        TypeError: raises if text id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            del __pool[id]
            return __orange__.Delete3DText(id)
        else:
            return False
    else:
        raise TypeError('3DText ID must be an integer')


def getByID(id):
    """Returns text object by given id.

    Args:
        id (int): text id

    Returns:
        GTAOrange.text.Text: text object (False on failure)

    Raises:
        TypeError: raises if text id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            return __pool[id]
        return False
    else:
        raise TypeError('3DText ID must be an integer')


def getAll():
    """Returns dictionary with all text objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    Returns:
        dict: text dictionary
    """
    return __pool
