from __future__ import print_function
import builtins
import __orange__

__author__ = "Jon-Mailes Graeffe"
__copyright__ = "Copyright 2017, Jon-Mailes Graeffe"
__credits__ = ["GTA Orange team", "Hexaflexagon"]
__license__ = "MIT License"
__maintainer__ = "Jon-Mailes Graeffe"


def print(message):
    __orange__.Print(message)


builtins.print = print
