from core.state import World
from core.constants import CellValue
from ui import UserInterface, Theme

# Create a basic game state
from ui.mode import EditGameMode

world = World(20, 15)
ground = world.ground
for y in range(0, world.height):
    for x in range(0, world.width):
        ground.set_cell_value(x, y, CellValue.GROUND_EARTH)

# Create a user interface object and run it
theme = Theme()
user_interface = UserInterface(theme)
gameMode = EditGameMode(theme, world)
user_interface.setGameMode(gameMode)
user_interface.setRenderSize(world.width * theme.tileWidth, world.height * theme.tileHeight)
user_interface.run()
user_interface.quit()