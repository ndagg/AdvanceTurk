#%%

import logging
from bs4 import BeautifulSoup

from src.game_init import GameReader

from src.gameObjects.player import Player
from src.gameObjects.gamemap import BaseMap
from src.gameObjects.unitmap import UnitMap
from src.gameObjects.gamestate import GameState
from src.gameObjects.units import Infantry, Recon, Artillery, Tank

from src.codeUtils.log_helpers import logger
from src.codeUtils.plotting import (
    plot_map_graph,
    plot_map_image,
    plot_moves,
    add_edge_labels,
    plot_units_on_map
    )

from src.gameIntelligence.minimax import minimax
from src.gameIntelligence.evaluator import PureValueEvaluator

def main():

    with open("test_files/caustic_test.txt", 'r') as file:
        file = file.read()
    
    html = BeautifulSoup(file, 'html.parser')

    # game_container = html.find("div", {"id": "gamecontainer"})
    # game_header_table = game_container.find("div", {"id": "game-header-table"})
    # gamemap = game_header_table.find_all("a", href=True)[1]


    reader = GameReader()
    # reader.get_html("https://awbw.amarriner.com/game.php?games_id=1432305")
    reader.html = html
    reader.prettied = html.prettify()
    gmap = reader.generate_basemap()
    player1, player2 = reader.generate_players()


    tank = Tank(0)
    inf = Infantry(0)
    recon = Recon(1)
    # arty = Artillery(0)
    inf.set_loc((8, 12), gmap.dims)
    tank.set_loc((7, 13), gmap.dims)
    recon.set_loc((8, 13), gmap.dims)
    # arty.set_loc((8, 12), gmap.dims)
    unit_lists =  [[tank, inf], [recon]]
    tank.fuel = 1
    inf.fuel = 1
    recon.fuel = 4

    umap = UnitMap(gmap)
    buildings_dict = gmap.buildings_dict
    gamestate = GameState([player1, player2], unit_lists, buildings_dict, umap)

    gamestate.get_actions()
 
    ax = plot_map_image(gmap)
    ax = plot_moves(gamestate, tank, gmap.dims, ax)
    ax = plot_units_on_map([tank, inf, recon], ax)

    # score, move = minimax(gamestate, player1, 3, 0, PureValueEvaluator())



    # print(f"bot complete: {score}, {move}")



if __name__ == "__main__":
    main()
    print("Main complete")

# %%
