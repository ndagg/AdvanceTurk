# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:52:07 2026

@author: ndagg
"""

from abc import ABC, abstractmethod

from src.gameObjects.units import Unit
from src.gameObjects.gamestate import GameState

class Evaluator(ABC):
    """
    An abstract class defining how evaluators should behave
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def evaluate(self, player):
        pass


class PureValueEvaluator(Evaluator):
    """
    A basic Evaluator taking only unit value into account
    """
    def __init__(self, primary_player: int=0):
        self.primary_player = primary_player
        pass

    def unit_value(self, unit: Unit) -> int:
        value = unit.cost * unit.vhp/10
        return value

    def evaluate(self, gamestate: GameState) -> int:
        # Negative value is sum of oppositions' units
        opposing = gamestate.unit_lists[1 - self.primary_player]
        opposing_value = sum(self.unit_value(u) for u in opposing)

        own = gamestate.unit_lists[self.primary_player]
        own_value = sum(self.unit_value(u) for u in own)

        return own_value - opposing_value