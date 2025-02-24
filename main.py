from state import World
from state.constants import LAYER_GROUND_EARTH
from ui import UserInterface, Theme

# Create a basic game state
from ui.mode import EditGameMode

world = World(16, 10)
for y in range(3, 7):
    for x in range(4, 12):
        world.set_cell_value(x, y, LAYER_GROUND_EARTH)

# Create a user interface object and run it
theme = Theme()
user_interface = UserInterface(theme)
gameMode = EditGameMode(theme, world)
user_interface.setGameMode(gameMode)
user_interface.setRenderSize(world.width * theme.tileWidth, world.height * theme.tileHeight)
user_interface.run()
user_interface.quit()