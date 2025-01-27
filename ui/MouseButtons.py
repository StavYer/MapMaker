class MouseButtons:
    # Initialize the MouseButtons object with three optional boolean button states
    def __init__(self, input_button1: bool = False, input_button2: bool = False, input_button3: bool = False):
        # Store the button states in a single integer using bitwise operations
        # Button 1 -> bit 0, Button 2 -> bit 1, Button 3 -> bit 2
        self.buttons = input_button1 | input_button2 << 1 | input_button3 << 2

    @property
    def button1(self) -> bool:
        # Check if bit 0 (button 1) is set (True) in the integer representation
        return (self.buttons & 1) != 0

    @property
    def button2(self) -> bool:
        # Check if bit 1 (button 2) is set (True) in the integer representation
        return (self.buttons & 2) != 0

    @property
    def button3(self) -> bool:
        # Check if bit 2 (button 3) is set (True) in the integer representation
        return (self.buttons & 4) != 0
