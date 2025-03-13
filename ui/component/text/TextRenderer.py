from typing import cast, Optional, List, Tuple

import pygame
from pygame import Surface
from pygame.rect import Rect

from ui.component.text.token.TextStyle import TextStyle
from .TextTokenizer import TextTokenizer
from .token import ReturnTextToken, ContentTextToken, IconTextToken, StyleTextToken
from ...theme.Theme import Theme


class TextRenderer:

    def __init__(self, theme: Theme, fontName: Optional[str] = None):
        self.__theme = theme
        self.__tokenizer = TextTokenizer(theme)
        self.__style = TextStyle(fontName)

    def render(self, message: str) -> Surface:
        tokens = self.__tokenizer.parse(message, self.__style)

        # Compute text surfaces and final surface size
        blits: List[Tuple[Surface, Tuple[int, int], Optional[Rect]]] = []
        x, y = 0, 0
        currentStyle = self.__style
        surfaceWidth, surfaceHeight = 0, 0
        for token in tokens:
            if isinstance(token, ContentTextToken):
                contentToken = cast(ContentTextToken, token)
                surface = currentStyle.render(self.__theme, contentToken.content)
                height = surface.get_height()
                surfaceHeight = max(surfaceHeight, y + height)
                blits.append((cast(pygame.Surface, surface), (x, surfaceHeight - height), None))
                x += surface.get_width() + 1
            elif isinstance(token, IconTextToken):
                iconToken = cast(IconTextToken, token)
                surface = iconToken.tileset
                rect = iconToken.tile
                blits.append((surface, (x, y), rect))
                x += rect.width + 1
                surfaceHeight = max(surfaceHeight, y + rect.height)
            elif isinstance(token, ReturnTextToken):
                x, y = 0, surfaceHeight + 2
            elif isinstance(token, StyleTextToken):
                styleToken = cast(StyleTextToken, token)
                currentStyle = styleToken.style
            else:
                raise ValueError("Invalid token")
            surfaceWidth = max(surfaceWidth, x)

        # Build the final surface
        textSurface = Surface((surfaceWidth, surfaceHeight), flags=pygame.SRCALPHA)
        for blit in blits:
            textSurface.blit(*blit)

        return textSurface
