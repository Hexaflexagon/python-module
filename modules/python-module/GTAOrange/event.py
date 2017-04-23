"""Core class of GTA Orange Python wrapper
"""

__pool = {}
_current = 0


class Event():
    """Event class

    @param  id      int     event id
    """
    id = None

    _cb = None

    def __init__(self, cb):
        """Initializes a new event object.

        @param  cb      function    callback function
        """
        global _current

        self._cb = cb
        self.id = _current

        _current += 1

    def getCallback(self):
        """Returns callback function.

        @returns    function    callback function
        """
        return self._cb

    def cancel(self):
        """Cancels an event.

        @todo   UNIMPLEMENTED!
        """
        pass
