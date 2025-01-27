class MouseWheel:
    # Initialize the MouseWheel object with optional parameters
    def __init__(self, input_x: int = 0, input_y: int = 0, input_flipped: bool = False, input_which: int = 0):
        # Horizontal scroll delta (positive for right, negative for left)
        self.x = input_x

        # Vertical scroll delta (positive for up, negative for down)
        self.y = input_y

        # Indicates if the mouse wheel direction is flipped (True for flipped)
        self.flipped = input_flipped

        # Identifier for the specific mouse wheel (useful for devices with multiple wheels)
        self.which = input_which
