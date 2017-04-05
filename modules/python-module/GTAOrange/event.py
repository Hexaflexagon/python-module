"""Core class of GTA Orange Python wrapper
"""

__pool = {}
_current = 0


class Event():
    """Event class

    Attributes:
        id (int): event id
    """
    id = None

    _cb = None

    def __init__(self, cb):
        """Initializes a new event object.

        Args:
            cb (function): callback function
        """
        global _current

        self._cb = cb
        self.id = _current

        _current += 1

    def getCallback(self):
        """Returns callback function.

        Returns:
            function: callback function
        """
        return self._cb

    def cancel(self):
        """Cancels an event.

        TODO: UNIMPLEMENTED!
        """
        pass
