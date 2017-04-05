"""Python wrapper for GTA Orange's blip functions
"""
import __orange__
from GTAOrange import world as _world
from GTAOrange import vehicle as _vehicle
from GTAOrange import player as _player

__pool = {}


class Blip():
    """Blip class

    DO NOT GENERATE NEW OBJECTS DIRECTLY! Please use the create() function instead.

    Attributes:
        id (id): blip id
        is_global (bool): boolean which says if this blip is displayed to all players or not
    """
    id = None
    is_global = None

    _ehandlers = {}

    def __init__(self, id, is_global):
        """Initializes a new Blip object.

        Args:
            id (TYPE): Description
            is_global (TYPE): Description
        """
        self.id = id
        self.is_global = is_global

    def attachTo(self, dest):
        """Attaches the blip to the vehicle represented by the given vehicle object, or to the player represented by the given player object.

        Args:
            dest (GTAOrange.player.Player OR GTAOrange.vehicle.Vehicle): player or vehicle object

        Returns:
            bool: True for success, False for failure
        """
        if isinstance(dest, _player.Player):
            __orange__.AttachBlipToPlayer(self.id, dest.id)
            return True
        elif isinstance(dest, _vehicle.Vehicle):
            __orange__.AttachBlipToVehicle(self.id, dest.id)
            return True
        else:
            return False

    def delete(self):
        """Deletes the blip.
        """
        deleteByID(self.id)

    def distanceTo(self, x, y, z=None):
        """Returns the distance from the blip to the given coordinates.

        Args:
            x (float): x-coord
            y (float): y-coord
            z (float, optional): z-coord

        Returns:
            float: distance between blip and given coordinates
        """
        if z is not None:
            x1, y1, z1 = self.getPosition()
            return _world.getDistance(x1, y1, z1, x, y, z)
        else:
            x1, y1 = self.getPosition()
            return _world.getDistance(x1, y1, x, y)

    def getID(self):
        """Returns blip id.

        Returns:
            int: blip id
        """
        return self.id

    def getPosition(self):
        """Returns current position.

        Returns:
            tuple: position tuple with 3 values
        """
        return __orange__.GetBlipCoords(self.id)

    def setColor(self, color):
        """Sets color of the blip.

        Args:
            color (GTAOrange.blip.Color): blip color
        """
        __orange__.SetBlipColor(self.id, color)

    def setRoute(self, route):
        """Enables/disables routing to blip.

        Args:
            route (bool): True for routing, False for not
        """
        __orange__.SetBlipRoute(self.id, route)

    def setScale(self, scale):
        """Sets scale of blip.

        Args:
            scale (float): blip scale
        """
        __orange__.SetBlipScale(self.id, scale)

    def setSprite(self, sprite):
        """Sets sprite (texture, icon) of blip.

        Args:
            sprite (GTAOrange.blip.Sprite): blip sprite
        """
        __orange__.SetBlipSprite(self.id, sprite)

    def setShortRange(self, toggle):
        """Sets that blip can be seen only on the short distance.

        Args:
            toggle (bool): True for yes, False for no
        """
        __orange__.SetBlipShortRange(self.id, toggle)


def create(name, x, y, z, scale=1.0, color=None, sprite=None):
    """Creates a new blip.

    This is the right way to spawn a new blip.

    Args:
        name (string): name (displayed in the map legend)
        x (float): x-coord of blip
        y (float): y-coord of blip
        z (float): z-coord of blip
        scale (float, optional): blip scale
        color (GTAOrange.blip.Color, optional): blip color
        sprite (GTAOrange.blip.Sprite, optional): blip sprite (texture, icon)

    Returns:
        GTAOrange.blip.Blip: blip object
    """
    global __pool

    blip = Blip(__orange__.CreateBlipForAll(name, x, y, z, scale,
                                            color if color is not None else Color.ORANGE, sprite if sprite is not None else Sprite.STANDARD), True)
    __pool[blip.id] = blip
    return blip


def deleteByID(id):
    """Deletes a blip object by the given id.

    Args:
        id (int): blip id

    Returns:
        bool: True on success, False on failure

    Raises:
        TypeError: raises if blip id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            del __pool[id]
            return __orange__.DeleteBlip(id)
        else:
            return False
    else:
        raise TypeError('Blip ID must be an integer')


def getByID(id):
    """Returns blip object by given id.

    Args:
        id (int): blip id

    Returns:
        bool: True on success, False on failure

    Raises:
        TypeError: raises if blip id is not int
    """
    global __pool

    if isinstance(id, int):
        if id in __pool.keys():
            return __pool[id]
        return False
    else:
        raise TypeError('Blip ID must be an integer')


def getAll():
    """Returns dictionary with all blip objects.

    WARNING! Can cause heavy load on some servers. If you can avoid using it, don't use it!

    Returns:
        dict: blip dictionary
    """
    return __pool


class Color():
    """Enum-like class with attributes representing all colors which can be used for blips
    """
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    ORANGE = 17
    PURPLE = 19
    GREY = 20
    BROWN = 21
    PINK = 23
    DARKGREEN = 25
    DARKPURPLE = 27
    DARKBLUE = 29
    MICHAELBLUE = 42
    FRANKLINGREEN = 43
    TREVORORANGE = 44
    YELLOW = 66


class Sprite():
    """Enum-like class with attributes representing all sprites which can be used for blips
    """
    STANDARD = 1
    BIGBLIP = 2
    POLICEOFFICER = 3
    POLICEAREA = 4
    SQUARE = 5
    PLAYER = 6
    NORTH = 7
    WAYPOINT = 8
    BIGCIRCLE = 9
    BIGCIRCLEOUTLINE = 10
    ARROWUPOUTLINED = 11
    ARROWDOWNOUTLINED = 12
    ARROWUP = 13
    ARROWDOWN = 14
    POLICEHELICOPTERANIMATED = 15
    JET = 16
    NUMBER1 = 17
    NUMBER2 = 18
    NUMBER3 = 19
    NUMBER4 = 20
    NUMBER5 = 21
    NUMBER6 = 22
    NUMBER7 = 23
    NUMBER8 = 24
    NUMBER9 = 25
    NUMBER10 = 26
    GTAOCREW = 27
    GTAOFRIENDLY = 28
    LIFT = 36
    RACEFINISH = 38
    SAFEHOUSE = 40
    POLICEOFFICER2 = 41
    POLICECARDOT = 42
    POLICEHELICOPTER = 43
    CHATBUBBLE = 47
    GARAGE2 = 50
    DRUGS = 51
    STORE = 52
    POLICECAR = 56
    POLICEPLAYER = 58
    POLICESTATION = 60
    HOSPITAL = 61
    HELICOPTER = 64
    STRANGERSANDFREAKS = 65
    ARMOREDTRUCK = 66
    TOWTRUCK = 68
    BARBER = 71
    LOSSANTOSCUSTOMS = 72
    CLOTHES = 73
    TATTOOPARLOR = 75
    SIMEON = 76
    LESTER = 77
    MICHAEL = 78
    TREVOR = 79
    RAMPAGE = 84
    VINEWOODTOURS = 85
    LAMAR = 86
    FRANKLIN = 88
    CHINESE = 89
    AIRPORT = 90
    BAR = 93
    BASEJUMP = 94
    CARWASH = 100
    COMEDYCLUB = 102
    DART = 103
    FIB = 106
    DOLLARSIGN = 108
    GOLF = 109
    AMMUNATION = 110
    EXILE = 112
    SHOOTINGRANGE = 119
    SOLOMON = 120
    STRIPCLUB = 121
    TENNIS = 122
    TRIATHLON = 126
    OFFROADRACEFINISH = 127
    KEY = 134
    MOVIETHEATER = 135
    MUSIC = 136
    MARIJUANA = 140
    HUNTING = 141
    ARMSTRAFFICKINGGROUND = 147
    NIGEL = 149
    ASSAULTRIFLE = 150
    BAT = 151
    GRENADE = 152
    HEALTH = 153
    KNIFE = 154
    MOLOTOV = 155
    PISTOL = 156
    RPG = 157
    SHOTGUN = 158
    SMG = 159
    SNIPER = 160
    SONICWAVE = 161
    POINTOFINTEREST = 162
    GTAOPASSIVE = 163
    GTAOUSINGMENU = 164
    LINK = 171
    MINIGUN = 173
    GRENADELAUNCHER = 174
    ARMOR = 175
    CASTLE = 176
    CAMERA = 184
    HANDCUFFS = 188
    YOGA = 197
    CAB = 198
    NUMBER11 = 199
    NUMBER12 = 200
    NUMBER13 = 201
    NUMBER14 = 202
    NUMBER15 = 203
    NUMBER16 = 204
    SHRINK = 205
    EPSILON = 206
    PERSONALVEHICLECAR = 225
    PERSONALVEHICLEBIKE = 226
    CUSTODY = 237
    ARMSTRAFFICKINGAIR = 251
    FAIRGROUND = 266
    PROPERTYMANAGEMENT = 267
    ALTRUIST = 269
    ENEMY = 270
    CHOP = 273
    DEAD = 274
    HOOKER = 279
    FRIEND = 280
    BOUNTYHIT = 303
    GTAOMISSION = 304
    GTAOSURVIVAL = 305
    CRATEDROP = 306
    PLANEDROP = 307
    SUB = 308
    RACE = 309
    DEATHMATCH = 310
    ARMWRESTLING = 311
    AMMUNATIONSHOOTINGRANGE = 313
    RACEAIR = 314
    RACECAR = 315
    RACESEA = 316
    GARBAGETRUCK = 318
    SAFEHOUSEFORSALE = 350
    PACKAGE = 351
    MARTINMADRAZO = 352
    ENEMYHELICOPTER = 353
    BOOST = 354
    DEVIN = 355
    MARINA = 356
    GARAGE = 357
    GOLFFLAG = 358
    HANGAR = 359
    HELIPAD = 360
    JERRYCAN = 361
    MASKS = 362
    HEISTSETUP = 363
    INCAPACITATED = 364
    PICKUPSPAWN = 365
    BOILERSUIT = 366
    COMPLETED = 367
    ROCKETS = 368
    GARAGEFORSALE = 369
    HELIPADFORSALE = 370
    MARINAFORSALE = 371
    HANGARFORSALE = 372
    BUSINESS = 374
    BUSINESSFORSALE = 375
    RACEBIKE = 376
    PARACHUTE = 377
    TEAMDEATHMATCH = 378
    RACEFOOT = 379
    VEHICLEDEATHMATCH = 380
    BARRY = 381
    DOM = 382
    MARYANN = 383
    CLETUS = 384
    JOSH = 385
    MINUTE = 386
    OMEGA = 387
    TONYA = 388
    PAPARAZZO = 389
    CROSSHAIR = 390
    CREATOR = 398
    CREATORDIRECTION = 399
    ABIGAIL = 400
    BLIMP = 401
    REPAIR = 402
    TESTOSTERONE = 403
    DINGHY = 404
    FANATIC = 405
    INFORMATION = 407
    CAPTUREBRIEFCASE = 408
    LASTTEAMSTANDING = 409
    BOAT = 410
    CAPTUREHOUSE = 411
    JERRYCAN2 = 415
    RP = 416
    GTAOPLAYERSAFEHOUSE = 417
    GTAOPLAYERSAFEHOUSEDEAD = 418
    CAPTUREAMERICANFLAG = 419
    CAPTUREFLAG = 420
    TANK = 421
    HELICOPTERANIMATED = 422
    PLANE = 423
    PLAYERNOCOLOR = 425
    GUNCAR = 426
    SPEEDBOAT = 427
    HEIST = 428
    STOPWATCH = 430
    DOLLARSIGNCIRCLED = 431
    CROSSHAIR2 = 432
    DOLLARSIGNSQUARED = 434
