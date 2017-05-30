"""Hash-to-string & string-to-hash conversion classes. Very useful to not get confused with all the ingame items!
"""
class HashContainer():
    """Skeleton class for hash-string conversion of ingame GTA5 objects
    """
    loaded = False
    objects = {}

    @classmethod
    def load(cls, file_name, dict_key=None, as_attr=True):
        with open(file_name) as file:
            import json

            cls.objects = json.load(file)

            if dict_key is not None:
                cls.objects = cls.objects[dict_key]

            if as_attr:
                for key, obj in cls.objects.items():
                    setattr(cls, key, obj)

            cls.loaded = True

    @classmethod
    def getHashByString(cls, string):
        if cls.loaded:
            string = string.upper()

            if string in cls.objects.keys():
                return cls.objects[string]
            else:
                return None
        else:
            return False

    @classmethod
    def getStringByHash(cls, hash_):
        if cls.loaded:
            for key, obj in cls.objects:
                if hash_ == obj:
                    return key
            return None
        else:
            return False


class Key():
    """Enum-like class with attributes representing all buttons/keys which on which GTA Orange reacts

    Please note that this is no sub class of `HashContainer`, so you can't use the otherwise inherited class methods of it.
    But that shouldn't be needed at all, anyway.
    """
    ESCAPE = 0x1B
    SPACE = 0x20
    LEFT = 0x25
    UP = 0x26
    RIGHT = 0x27
    DOWN = 0x28
    DELETE = 0x2E

    NUM_0 = 0x30
    NUM_1 = 0x31
    NUM_2 = 0x32
    NUM_3 = 0x33
    NUM_4 = 0x34
    NUM_5 = 0x35
    NUM_6 = 0x36
    NUM_7 = 0x37
    NUM_8 = 0x38
    NUM_9 = 0x39

    A = 0x41
    B = 0x42
    C = 0x43
    D = 0x44
    E = 0x45
    F = 0x46
    G = 0x47
    H = 0x48
    I = 0x49
    J = 0x4A
    K = 0x4B
    L = 0x4C
    M = 0x4D
    N = 0x4E
    O = 0x4F
    P = 0x50
    Q = 0x51
    R = 0x52
    S = 0x53
    T = 0x54
    U = 0x55
    V = 0x56
    W = 0x57
    X = 0x58
    Y = 0x59
    Z = 0x5A

    NUMPAD0 = 0x60
    NUMPAD1 = 0x61
    NUMPAD2 = 0x62
    NUMPAD3 = 0x63
    NUMPAD4 = 0x64
    NUMPAD5 = 0x65
    NUMPAD6 = 0x66
    NUMPAD7 = 0x67
    NUMPAD8 = 0x68
    NUMPAD9 = 0x69

    MULTIPLY = 0x6A
    ADD = 0x6B
    SEPARATOR = 0x6C
    SUBTRACT = 0x6D
    DECIMAL = 0x6E
    DIVIDE = 0x6F

    F1 = 0x70
    F2 = 0x71
    F3 = 0x72
    F4 = 0x73
    F5 = 0x74
    F6 = 0x75
    F7 = 0x76
    F8 = 0x77
    F9 = 0x78
    F10 = 0x79
    F11 = 0x7A
    F12 = 0x7B
    F13 = 0x7C
    F14 = 0x7D
    F15 = 0x7E
    F16 = 0x7F
    F17 = 0x80
    F18 = 0x81
    F19 = 0x82
    F20 = 0x83
    F21 = 0x84
    F22 = 0x85
    F23 = 0x86
    F24 = 0x87

class VehicleColor(HashContainer):
    """Enum-like class with attributes representing all available vehicle colors.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.
    """
    pass

class Weapon(HashContainer):
    """Enum-like class with attributes representing all ingame weapons.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.
    """
    pass


class Gadget(HashContainer):
    """Enum-like class with attributes representing all ingame gadgets.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.
    """
    pass


class VehicleWeapon(HashContainer):
    """Enum-like class with attributes representing all ingame vehicle weapons.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.
    """
    pass


class Explosive(HashContainer):
    """Enum-like class with attributes representing all ingame explosives.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.
    """
    pass


class Object(HashContainer):
    """With this class you can convert object name strings to hashes and vice versa.
    You can use the methods of the `HashContainer` class on this one as well.
    See the docs for more info.

    Please note that you've to call `loadHashContainer("Object")` before you can use it properly.
    """
    pass


def loadHashContainer(container):
    if container == "Object":
        Object.load(
            "./modules/python-module/GTAOrange/objects.json", as_attr=False)
        return Object


# autoloaded hash databases
VehicleColor.load("./modules/python-module/GTAOrange/colors.json", "vehicle_colors")
Weapon.load("./modules/python-module/GTAOrange/weapons.json", "weapons")
Gadget.load("./modules/python-module/GTAOrange/weapons.json", "gadgets")
VehicleWeapon.load(
    "./modules/python-module/GTAOrange/weapons.json", "vehicle_weapons")
Explosive.load("./modules/python-module/GTAOrange/weapons.json", "explosives")
