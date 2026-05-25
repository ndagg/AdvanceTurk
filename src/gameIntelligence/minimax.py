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
            evaluator: Evaluator,
            ):
    
    logger.parent.handlers[0].formatter.indent = current_depth
    logger.parent.handlers[0].formatter.current_player = gamestate.current_player_id
    logger.info(f"Entering minimax at depth {current_depth}")
    
    # Check if recursion has to end
    if current_depth == max_depth:
        logger.info("Exiting minimax due to max depth")
        return evaluator.evaluate(gamestate), []
    if gamestate.is_gameover():
        logger.info("Exiting minimax due to gameover")
        return evaluator.evaluate(gamestate), []
    
    # Otherwise bubble up
    if gamestate.current_player_id == player.player_number:
        best_score = -1e10
    else:
        best_score = 1e10
    
    best_action_at_this_level = None
    best_action_sequence = []
    
    # Go through actions
    actions = gamestate.get_actions()
    if not actions:
        logger.info("Exiting minimax due to no further actions")
        return evaluator.evaluate(gamestate), []

    for i, action in enumerate(actions):
        new_gamestate = gamestate.make_action_on_new_state(action, i)

        # Recurse
        current_score, current_action_sequence = minimax(
            new_gamestate,
            player,
            max_depth,
            current_depth+1,
            evaluator,
            )
        
        logger.parent.handlers[0].formatter.indent = current_depth
        logger.parent.handlers[0].formatter.current_player = gamestate.current_player_id
        
        # Update best score and track the action that led to it
        if gamestate.current_player_id == player.player_number:
            if current_score > best_score:
                logger.info(f"New best score: {current_score}, previous score: {best_score}")
                best_score = current_score
                best_action_at_this_level = action
                best_action_sequence = current_action_sequence
            else:
                logger.debug(f"No improvement, current score: {best_score}, discarded score: {current_score}")
        else:
            if current_score < best_score:
                logger.debug(f"New best score: {current_score}, previous score: {best_score}")
                best_score = current_score
                best_action_at_this_level = action
                best_action_sequence = current_action_sequence
            else:
                logger.debug(f"No improvement, current score: {best_score}, discarded score: {current_score}")
    
    logger.info(f"Exiting minimax, score: {best_score}, depth: {current_depth}")
    return best_score, [best_action_at_this_level] + best_action_sequence
