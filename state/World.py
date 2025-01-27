class World:
    def __init__(self, input_width : int, input_height : int):
        # size of are world. Should be immutable.
        self.__width = input_width
        self.__height = input_height
        # Value of every cell of the world. Should be immutable.
        # A 2d matrix - each row has width columns (initialized to 0)
        # and we have height rows
        self.__cells = []
        for y in range(input_height):
            row = [0] * input_width
            self.__cells.append(row)

    # Getter properties
    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    # Getter and Setter for a single cell's value

    def get_cell_value(self, input_x : int, input_y : int) -> int:
        # Assert that the coordinates are at between proper limits, otherwise notify
        assert 0 <= input_x < self.__width, f"invalid cell x coordinate: {input_x}"
        assert 0 <= input_y < self.__height, f"invalid cell y coordinate: {input_y}"

        return self.__cells[input_y][input_x]

    def set_cell_value(self, input_x : int, input_y : int, value : int) -> None:
        # Same here
        assert 0 <= input_x < self.__width, f"invalid cell x coordinate: {input_x}"
        assert 0 <= input_y < self.__height, f"invalid cell y coordinate: {input_y}"
        assert 0 <= value <= 1 and type(value) == int, f"invalid cell value: {value}"
        self.__cells[input_y][input_x] = value