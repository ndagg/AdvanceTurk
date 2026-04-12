from bs4 import BeautifulSoup
from src.gameObjects.player import Player
from src.game_init import GameReader

from src.gameObjects.gamemap import BaseMap
from src.gameObjects.unitmap import UnitMap
from src.gameObjects.gamestate import GameState
from src.gameObjects.units import Infantry, Recon, Artillery, Rocket
from src.codeUtils.plotting import (
    plot_map_graph,
    plot_map_image,
    plot_moves,
    add_edge_labels
    )

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


    inf = Infantry(0)
    recon = Recon(1)
    arty = Artillery(0)
    inf.set_loc((7, 13), gmap.dims)
    recon.set_loc((8, 13), gmap.dims)
    arty.set_loc((8, 12), gmap.dims)

    player1 = Player(0, None, [inf, arty])
    player2 = Player(1, None, [recon])
    umap = UnitMap(gmap, {0: player1.units, 1: player2.units})
    gamestate = GameState([player1, player2], umap)

    umap.update_units(player2)
    umap.update_units(player1)
    player1_moves = gamestate.get_moves()


    ax = plot_map_image(gmap)
    # ax = plot_moves(player1.attacks[0], gmap.dims, ax, True)
    ax = plot_moves(player1.attacks[1], gmap.dims, ax, True)
    # ax = plot_moves(player2.moves[0], gmap.dims, ax, True)
    ax = plot_moves(player2.attacks[0], gmap.dims, ax, True)

    print("bot complete")
    # ax._children[0]._A *= 0


if __name__ == "__main__":
    main()
