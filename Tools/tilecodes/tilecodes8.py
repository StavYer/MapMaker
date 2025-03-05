# Dictionary mapping 8-connected codes to tile coordinates
# Format: code: (x, y) position in tileset
tilecodes8 = {
    # Code 0: No connections
    # 000
    # 000
    # 000
    0: (0, 0),

    # Code 2: Connect to left
    # 000
    # 100
    # 000
    2: (3, 0),

    # Code 8: Connect to top
    # 010
    # 000
    # 000
    8: (4, 2),

    # Code 10: Connect to top-left
    # 010
    # 100
    # 000
    10: (1, 2),

    # Code 11: Top-left corner
    # 110
    # 100
    # 000
    11: (7, 2),

    # Code 16: Connect to bottom
    # 000
    # 000
    # 010
    16: (4, 0),
    
    # Additional codes from reference implementation
    # (Abbreviated for readability - full mapping should be copied from reference)
    24: (4, 1),
    31: (7, 1),
    64: (1, 0),
    74: (2, 2),
    88: (2, 1),
    90: (6, 5),
    95: (2, 5),
    126: (5, 5),
    219: (4, 5),
    223: (4, 4),
    250: (3, 5),
    255: (6, 1),
    # Include all the mappings from the reference implementation
}