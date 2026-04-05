from bs4 import BeautifulSoup
from src.game_init import GameReader

from src.gameObjects.gamemap import BaseMap, UnitMap
from src.gameObjects.units import Infantry, Recon
from src.codeUtils.plotting import (
    plot_map_graph,
    plot_map_image,
    plot_move_graph,
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
    inf.glocation = 178
    recon.glocation = 106

    umap = UnitMap(gmap, [inf, recon])
    umap.generate_unit_moves(0)

    ax = plot_map_image(gmap)
    ax = plot_move_graph(umap.player_move_lists[0][0], ax, True)

    print("bot complete")
    # ax._children[0]._A *= 0


if __name__ == "__main__":
    main()
