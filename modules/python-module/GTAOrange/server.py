"""Python wrapper for GTA Orange's server functions

Subscribable built-in events:
+========+=========================+==================+
|  name  | vehicle-local arguments | global arguments |
+========+=========================+==================+
| unload | ???                     | ???              |
+--------+-------------------------+------------------+
"""
import __orange__
from GTAOrange import event as _event

__ehandlers = {}
__forbidden_event_names = ['serverunload']


def on(event, cb):
    """Subscribes for an event.

    @param  event   string      event name
    @param  cb      function    callback function
    """
    if event in __ehandlers.keys():
        __ehandlers[event].append(_event.Event(cb))
    else:
        __ehandlers[event] = []
        __ehandlers[event].append(_event.Event(cb))


def trigger(event, *args):
    """Triggers an event.

    @param  event   string  event name
    @param  *args   *args   arguments
    """
    if event in __ehandlers.keys():
        for handler in __ehandlers[event]:
            handler.getCallback()(*args)


def _onServerUnload(p0):
    trigger("unload", p0)


def _onClientTriggeredEvent(event, player_id, *args):
    if event.lower() not in __forbidden_event_names:
        from GTAOrange import player as _player

        player = _player.getByID(player_id)
        trigger(event, player, *args)


__orange__.AddServerEvent(_onServerUnload, "ServerUnload")
__orange__.AddServerEvent(_onClientTriggeredEvent, "serverEvent")
