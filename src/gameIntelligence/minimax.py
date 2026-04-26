# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 20:17:07 2026

@author: ndagg
"""
import logging

logger = logging.getLogger("mainlogger.minimax")

def minimax(gamestate: object,
            player: object,
            max_depth: int,
            current_depth: int
            ):
    
    logger.info(f"Entering minimax at depth {current_depth}")
    # Check if recursion has to end
    if gamestate.is_gameover() or current_depth == max_depth:
        return gamestate.evaluate(player)
    
    # Otherwise bubble up
    best_move = None
    if gamestate.current_player == player:
        best_score = -1e10
    else:
        best_score = 1e10
    
    # Go through moves
    for move in gamestate.get_moves():
        new_gamestate = gamestate.make_move(move)

        # Recurse
        current_score, current_move = minimax(
            new_gamestate,
            player,
            max_depth,
            current_depth+1)
        logger.info(f"Exiting minimax, score: {current_score}, depth: {current_depth}")
        
        # Update best score
        if gamestate.current_player == player:
            if current_score > best_score:
                logger.info(f"New best score: {current_score}, previous score: {best_score}")
                best_score = current_score
                best_move = move
        else:
            if current_score < best_score:
                logger.debug(f"No improvement, current score: {best_score}, discarded score: {current_score}")
                best_score = current_score
                best_move = move
    
    return best_score, best_move
