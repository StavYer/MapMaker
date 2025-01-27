from state import World
from state.constants import LAYER_GROUND_EARTH
from ui import UserInterface

# Create a basic game state
world = World(16, 10)
for y in range(3, 7):
    for x in range(4, 12):
        world.set_cell_value(x, y, LAYER_GROUND_EARTH)

# Create a user interface object and run it
userInterface = UserInterface(world)
userInterface.run()
userInterface.quit()
