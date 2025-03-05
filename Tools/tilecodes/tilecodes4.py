# Array of tile coordinates for each 4-connected code
# Format: [code] = (x, y) position in tileset
tilecodes4 = [
    # Code 0: No connections
    #  0
    # 000
    #  0
    (0, 0),

    # Code 1: Connect to left
    #  0
    # 100
    #  0
    (3, 0),

    # Code 2: Connect to top
    #  1
    # 000
    #  0
    (3, 3),

    # Code 3: Connect to left and top
    #  1
    # 100
    #  0
    (1, 2),

    # Code 4: Connect to bottom
    #  0
    # 000
    #  1
    (1, 3),

    # Code 5: Connect to left and bottom
    #  0
    # 100
    #  1
    (1, 1),

    # Code 6: Connect to top and bottom
    #  1
    # 000
    #  1
    (2, 3),

    # Code 7: Connect to left, top, bottom
    #  1
    # 100
    #  1
    (3, 2),

    # Code 8: Connect to right
    #  0
    # 001
    #  0
    (1, 0),

    # Code 9: Connect to left and right
    #  0
    # 101
    #  0
    (2, 0),

    # Code 10: Connect to top and right
    #  1
    # 001
    #  0
    (0, 2),

    # Code 11: Connect to left, top, right
    #  1
    # 101
    #  0
    (2, 2),

    # Code 12: Connect to bottom and right
    #  0
    # 001
    #  1
    (0, 1),

    # Code 13: Connect to left, bottom, right
    #  0
    # 101
    #  1
    (3, 1),

    # Code 14: Connect to top, bottom, right
    #  1
    # 001
    #  1
    (2, 1),

    # Code 15: Connect all directions
    #  1
    # 101
    #  1
    (0, 3),
]