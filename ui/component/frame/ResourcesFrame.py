from pygame.surface import Surface

from .FrameComponent import FrameComponent
from ..text import TextRenderer
from ...theme.Theme import Theme


class ResourcesFrame(FrameComponent):

    def __init__(self, i_theme: Theme):
        # Initialize text renderer with the given theme and font size
        self.__textRenderer = TextRenderer(i_theme, "small")

        # Calculate frame size based on text surface and border size
        frameBorderSize = i_theme.frameBorderSize
        textSurface = self.__createTextSurface()
        size = (
            textSurface.get_width() + 2 * frameBorderSize,
            textSurface.get_height() + 2 * frameBorderSize
        )
        super().__init__(i_theme, size)

        # Move frame to the initial position
        self.moveTo((frameBorderSize, frameBorderSize))

    def __createTextSurface(self):
        # Render the resource text onto a surface
        textSurface = self.__textRenderer.render(
            "100<food> 200<wood> 150<stone>  10<gold>"
        )
        return textSurface

    # Component

    def render(self, i_surface: Surface):
        # Render the frame component
        super().render(i_surface)

        # Render the text surface onto the given surface
        textSurface = self.__createTextSurface()
        x, y = self.topLeft
        bs = self.theme.frameBorderSize
        i_surface.blit(textSurface, (x + bs, y + bs))
