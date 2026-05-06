# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:17:07 2026

@author: ndagg
"""
import logging

from src.gameObjects.gamestate import GameState
from src.gameObjects.player import Player
from src.gameIntelligence.evaluator import Evaluator


logger = logging.getLogger("mainlogger.minimax")


def minimax(gamestate: GameState,
            player: Player,
            max_depth: int,
            current_depth: int,
            evaluator: Evaluator
            ):
    
    logger.parent.handlers[0].formatter.indent = current_depth
    logger.parent.handlers[0].formatter.current_player = gamestate.current_player_id
    logger.info(f"Entering minimax at depth {current_depth}")
    
    # Check if recursion has to end
    if gamestate.is_gameover() or current_depth == max_depth:
        return evaluator.evaluate(gamestate), None
    
    # Otherwise bubble up
    best_action = None
    if gamestate.current_player == player.player_number:
        best_score = -1e10
    else:
        best_score = 1e10
    
    # Go through actions
    actions = gamestate.get_actions()
    if not actions:
        return evaluator.evaluate(gamestate), best_action
    for i, move in enumerate(actions):
        new_gamestate = gamestate.make_action_on_new_state(move, i)

        # Recurse
        current_score, current_move = minimax(
            new_gamestate,
            player,
            max_depth,
            current_depth+1,
            evaluator)
        
        logger.parent.handlers[0].formatter.indent = current_depth
        logger.info(f"Exiting minimax, score: {current_score}, depth: {current_depth}")
        
        # Update best score
        if gamestate.current_player == player.player_number:
            if current_score > best_score:
                logger.info(f"New best score: {current_score}, previous score: {best_score}")
                best_score = current_score
                best_action = move
        else:
            if current_score <= best_score:
                logger.debug(f"No improvement, current score: {best_score}, discarded score: {current_score}")
                best_score = current_score
                best_action = move
    
    return best_score, best_action
