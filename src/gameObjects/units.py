# -*- coding: utf-8 -*-
"""
Created on Fri May 23 20:59:29 2025

@author: ndagg
"""
import logging
from abc import ABC
from dataclasses import dataclass

from src.codeUtils.helpers import loc_2_gloc, gloc_2_loc
from src.codeUtils.engineExceptions import EngineValueException

logger = logging.getLogger("mainlogger.units")

# =============================================================================
# Weapons
# =============================================================================
# @dataclass
# class Weapon(ABC):
#     """
#     Represents a weapon on a unit
#     """
#     targets: list
    
#     @abstractmethod
#     def set_attack(self, unit_id):
#         ...
        


# @dataclass
# class PrimaryDirectWeapon(Weapon):
#     """
#     Represents a primary direct weapon on a unit
#     """
#     ammo: int
    
#     def set_attack(self, unit_id):
#         self.attack = PRIMARY_ATTACK[unit_id]
    
    
# @dataclass
# class PrimaryIndirectWeapon(Weapon):   
#     """
#     Represents a primary indirect weapon on a unit
#     """
#     min_range: int
#     max_range: int
    
#     ammo: int
    
#     def set_attack(self, unit_id):
#         self.attack = PRIMARY_ATTACK[unit_id]
    

# @dataclass
# class SecondaryWeapon(Weapon):
#     """
#     Represents a secondary weapon on a unit
#     """
#     min_range = 0
#     max_range = 1
    
#     def set_attack(self, unit_id):
#         self.attack = SECONDARY_ATTACK[unit_id]
    
    
# =============================================================================
# Transport
# =============================================================================
@dataclass
class Transport():
    """
    Represents the possible transport capability of a unit

    Attributes:
        transportable: list
            list of unit ids that can be transported
        capacity: int
            number of units that can be transported
        carrying: list
            list of units currently being transported
    """
    transportable: list
    capacity: int
    carrying: list


# =============================================================================
# Units
# =============================================================================
"""
Move types:
    0: Foot
    1: Boot
    2: Wheel
    3: Track
    4: Air
    5: Naval
    6: Littoral
    7: Pipe
"""

class Unit(ABC):
    def __init__(self):
        self.hp = 100  # True hit points
        self.vhp = 10  # Visual hit points
        self.hidden = False
        self.daily_drain = 0
        self.id = 0
        
        self.cost = 0
        self.fuel = 0
        self.owner = 0
        self.move = 0
        self.move_type = 0
        self.can_hide = False
        
        self.ammo = 0
        self.direct = True
        self.min_range = 0
        self.max_range = 1
        self.transport = None
        self.active = True
        
        self.capture_power = 0  # Apply capture_power * vhp to properties
        
        self.location = None
        self.glocation = None

    def hide_unhide(self):
        if not self.hidden:
            self.hidden = True
            self.daily_drain = 8
        else:
            self.hidden = False
            self.daily_drain = 5

    def take_damage(self, amount: int):
        """
        Apply damage to unit, return False if unit dies
        """
        if self.hp <= amount:
            return False
        self.hp -= amount
        self.vhp = -(self.hp // -10)  # Upside-down floor probably overkill, but avoids floats
        return True

    def reduce_fuel(self, amount):
        if self.fuel - amount < 0:
            raise EngineValueException(
                f"{self} - Attempting to spend more fuel than remains\n"
                + f"Current reserve: {self.fuel}, spend amount: {amount}")
        else:
            logger.debug(
                f"{self.__class__.__name__} reducing fuel from {self.fuel} by {amount}, id: {hex(id(self))}")
            self.fuel -= amount

    def set_loc(self, loc, dims):
        self.location = loc
        self.glocation = loc_2_gloc(loc, dims)

    def set_gloc(self, gloc, dims):
        self.glocation = gloc
        self.location = gloc_2_loc(gloc, dims)
 
    def __repr__(self):
        outstr = f"{self.__class__.__name__}, Location: {self.glocation}, HP: {self.hp}"
        return outstr


# =============================================================================
# Land
# =============================================================================
class Infantry(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 0
        
        self.cost = 1000
        self.fuel = 99
        self.move = 3
    
        self.ammo = -1
        
        self.capture_power = 1


class Mech(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 1
        
        self.cost = 3000
        self.fuel = 70
        self.move = 2
        self.move_type = 1
        
        self.ammo = 3
        
        self.capture_power = 1


class Recon(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 2
        
        self.cost = 4000
        self.fuel = 80
        self.move = 8
        self.move_type = 2
        
        self.ammo = -1


class APC(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 3
        
        self.cost = 5000
        self.fuel = 60
        self.move = 6
        self.move_type = 3
        
        self.transport = Transport([0, 1], 1, [])


class Artillery(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 4
        
        self.cost = 6000
        self.fuel = 50
        self.move = 5
        self.move_type = 3
        
        self.ammo = 9
        self.direct = False
        self.min_range = 2
        self.max_range = 3


class Tank(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 5
        
        self.cost = 7000
        self.fuel = 70
        self.move = 6
        self.move_type = 3
        
        self.ammo = 9
        
        
class AntiAir(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 6
        
        self.cost = 8000
        self.fuel = 60
        self.move = 6
        self.move_type = 3
        
        self.ammo = 9
        

class Missile(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 7
        
        self.cost = 12000
        self.fuel = 50
        self.move = 4
        self.move_type = 2
        
        self.ammo = 6
        self.direct = False
        self.min_range = 3
        self.max_range = 5
     
        
class Rocket(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 8
        
        self.cost = 15000
        self.fuel = 50
        self.move = 5
        self.move_type = 2
        
        self.ammo = 6
        self.direct = False
        self.min_range = 3
        self.max_range = 5
        

class MediumTank(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 9
        
        self.cost = 16000
        self.fuel = 50
        self.move = 8
        self.move_type = 3
        
        self.ammo = 8


class Piperunner(Unit):
    
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 10
        
        self.cost = 20000
        self.fuel = 99
        self.move = 9
        self.move_type = 7
        
        self.ammo = 9
        self.direct = False
        self.min_range = 2
        self.max_range = 5


class NeoTank(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 11
        
        self.cost = 22000
        self.fuel = 99
        self.move = 6
        self.move_type = 3
        
        self.ammo = 9
        

class MegaTank(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 12
        
        self.cost = 280000
        self.fuel = 50
        self.move = 4
        self.move_type = 3
        
        self.ammo = 3
        

# =============================================================================
# Air
# =============================================================================

class TCopter(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 13
        
        self.daily_drain = 2
        
        self.cost = 5000
        self.fuel = 99
        self.move = 6
        self.move_type = 4
        
        self.transport = Transport([0, 1], 1, [])


class BCopter(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 14
        
        self.daily_drain = 2
        
        self.cost = 9000
        self.fuel = 99
        self.move = 6
        self.move_type = 4
        
        self.ammo = 6
        
        
class Fighter(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 15
        
        self.daily_drain = 5
        
        self.cost = 20000
        self.fuel = 99
        self.move = 9
        self.move_type = 4
        
        self.ammo = 9


class Bomber(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 16
        
        self.daily_drain = 5
        
        self.cost = 22000
        self.fuel = 99
        self.move = 7
        self.move_type = 4
        
        self.ammo = 9
        
        
class Stealth(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 17
        
        self.daily_drain = 5
        
        self.cost = 24000
        self.fuel = 60
        self.move = 6
        self.move_type = 4
        
        self.ammo = 9
        
        self.can_hide = True
        

# =============================================================================
# Sea
# =============================================================================

class BlackBoat(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 18
        
        self.daily_drain = 1
        
        self.cost = 7500
        self.fuel = 50
        self.move = 7
        self.move_type = 5
        
        self.transport = Transport([0, 1], 2, [])
        
        # Should the repair be implemented as an attack?


class Lander(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 19
        
        self.daily_drain = 1
        
        self.cost = 12000
        self.fuel = 99
        self.move = 6
        self.move_type = 6
        
        self.transport = Transport(list(range(0, 13)), 2, [])


class Cruiser(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 20
        
        self.daily_drain = 1
        
        self.cost = 18000
        self.fuel = 99
        self.move = 6
        self.move_type = 5
        
        self.ammo = 9
        
        self.transport = Transport([13, 14], 2, [])
        
        
class Sub(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 21
        
        self.daily_drain = 1
        
        self.cost = 20000
        self.fuel = 60
        self.move = 5
        self.move_type = 5
        
        self.ammo = 6
        
        self.can_hide = True


class Battleship(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 22
        
        self.daily_drain = 1
        
        self.cost = 28000
        self.fuel = 99
        self.move = 5
        self.move_type = 5
        
        self.ammo = 9
        self.direct = False
        self.min_range = 2
        self.max_range = 6


class Carrier(Unit):
    def __init__(self, owner=0):
        super().__init__()
        self.owner = owner
        self.id = 23
        
        self.daily_drain = 1
        
        self.cost = 30000
        self.fuel = 99
        self.move = 5
        self.move_type = 5
        
        self.ammo = 9
        self.direct = False
        self.min_range = 3
        self.max_range = 8
        
        self.transport = Transport([13, 14, 15, 16, 17], 2, [])


ARCHETYPES = [
    Infantry(),
    Mech(),
    Recon(),
    APC(),
    Artillery(),
    Tank(),
    AntiAir(),
    Missile(),
    Rocket(),
    MediumTank(),
    Piperunner(),
    NeoTank(),
    MegaTank(),
    TCopter(),
    BCopter(),
    Fighter(),
    Bomber(),
    Stealth(),
    BlackBoat(),
    Lander(),
    Cruiser(),
    Sub(),
    Battleship(),
    Carrier()]

UNITS = [
    Infantry,   #0
    Mech,       #1
    Recon,      #2
    APC,        #3
    Artillery,  #4
    Tank,       #5
    AntiAir,    #6
    Missile,    #7
    Rocket,     #8
    MediumTank, #9
    Piperunner, #10
    NeoTank,    #11
    MegaTank,   #12
    TCopter,    #13
    BCopter,    #14
    Fighter,    #15
    Bomber,     #16
    Stealth,    #17
    BlackBoat,  #18
    Lander,     #19
    Cruiser,    #20
    Sub,        #21
    Battleship, #22
    Carrier]    #23

UNIT_NAMES = [
    "Infantry",   #0 /
    "Mech",       #1 /
    "Recon",      #2 /
    "APC",        #3 /
    "Artillery",  #4 /
    "Tank",       #5 /
    "Anti-Air",   #6 /
    "Missile",    #7 /
    "Rocket",     #8 /
    "Md.Tank",    #9 /
    "Piperunner", #10 /
    "Neotank",    #11 /
    "Mega Tank",  #12 /
    "T-Copter",   #13 /
    "B-Copter",   #14 /
    "Fighter",    #15 /
    "Bomber",     #16 /
    "Stealth",    #17 /
    "Black Boat", #18 /
    "Lander",     #19 /
    "Cruiser",    #20 /
    "Sub",        #21 /
    "Battleship", #22 /
    "Carrier"]    #23 /