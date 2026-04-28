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

    def __init__(self, players: list[object]):
        self.players = players

    def unit_value(self, unit):
        value = unit.cost * unit.hp/100

    def evaluate(self, player: object) -> int:
        # Negative value is sum of oppositions' units
        opposing = [p for p in self.players if p.team != player.team]
        opposing_value = sum(sum(self.unit_value(u) for u in p.units.values()) for p in opposing)

        own = [p for p in self.players if p.team == player.team]
        own_value = sum(sum(self.unit_value(u) for u in p.units.values()) for p in own)

        return own_value - opposing_value