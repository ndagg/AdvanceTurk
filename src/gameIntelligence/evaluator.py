# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 17:52:07 2026

@author: ndagg
"""

from abc import ABC, abstractmethod

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
    def __init__(self):
        pass

    def unit_value(self, unit):
        value = unit.cost * unit.hp/100
        return value

    def evaluate(self, gamestate: object) -> int:
        # Negative value is sum of oppositions' units
        opposing = gamestate.unit_lists[1 - gamestate.current_player_id]
        opposing_value = sum(self.unit_value(u) for u in opposing)

        own = gamestate.unit_lists[gamestate.current_player_id]
        own_value = sum(self.unit_value(u) for u in own)

        return own_value - opposing_value