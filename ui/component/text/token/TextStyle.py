from __future__ import annotations

from typing import Optional, cast

import pygame
from pygame.rect import Rect
from pygame.surface import Surface

from ui.theme.Theme import Theme

class TextStyle:
    # Text style flags
    PLAIN = 0
    BOLD = 1
    ITALIC = 2
    UNDERLINE = 4

    __slots__ = ["__fontName", "__colorName", "__flags"]

    def __init__(self, 
                 i_fontName: Optional[str] = None,
                 i_colorName: Optional[str] = None,
                 i_flags: int = 0):
        # Initialize TextStyle with optional font name, color name, and style flags
        self.__fontName = i_fontName
        self.__colorName = i_colorName
        self.__flags = i_flags

    def clone(self) -> TextStyle:
        # Return a copy of the current TextStyle
        return TextStyle(self.__fontName, self.__colorName, self.__flags)

    @property
    def colorName(self) -> Optional[str]:
        # Get the color name
        return self.__colorName

    def styleColor(self, i_colorName) -> TextStyle:
        # Return a new TextStyle with the specified color name
        if self.colorName == i_colorName:
            return self
        return TextStyle(self.__fontName, i_colorName, self.__flags)

    @property
    def italic(self) -> bool:
        # Check if the italic flag is set
        return (self.__flags & TextStyle.ITALIC) != 0

    def styleItalic(self, i_enable: bool = True) -> TextStyle:
        # Return a new TextStyle with the italic flag set or unset
        if self.italic == i_enable:
            return self
        if i_enable:
            i_flags = self.__flags | TextStyle.ITALIC
        else:
            i_flags = self.__flags & (~TextStyle.ITALIC)
        return TextStyle(self.__fontName, self.__colorName, i_flags)

    @property
    def bold(self) -> bool:
        # Check if the bold flag is set
        return (self.__flags & TextStyle.BOLD) != 0

    def styleBold(self, i_enable: bool = True) -> TextStyle:
        # Return a new TextStyle with the bold flag set or unset
        if self.bold == i_enable:
            return self
        if i_enable:
            i_flags = self.__flags | TextStyle.BOLD
        else:
            i_flags = self.__flags & (~TextStyle.BOLD)
        return TextStyle(self.__fontName, self.__colorName, i_flags)

    @property
    def underline(self) -> bool:
        # Check if the underline flag is set
        return (self.__flags & TextStyle.UNDERLINE) != 0

    def styleUnderline(self, i_enable: bool = True) -> TextStyle:
        # Return a new TextStyle with the underline flag set or unset
        if self.underline == i_enable:
            return self
        if i_enable:
            i_flags = self.__flags | TextStyle.UNDERLINE
        else:
            i_flags = self.__flags & (~TextStyle.UNDERLINE)
        return TextStyle(self.__fontName, self.__colorName, i_flags)

    def render(self, i_theme: Theme, i_text: str) -> Surface:
        # Render the text with the current TextStyle using the provided theme
        
        # Get the font object from the theme using the font name
        font = i_theme.getFont(self.__fontName)
        
        # Get the font crop values from the theme using the font name
        crop = i_theme.getFontCrop(self.__fontName)
        
        # Set the bold and italic properties of the font
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        
        # Get the font color from the theme using the color name
        color = i_theme.getFontColor(self.__colorName)
        
        # Render the text onto a surface with the specified color
        surface = font.render(str(i_text), False, color)
        
        # If underline is enabled, draw an underline on the surface
        if self.underline:
            ascent = font.get_ascent()
            pygame.draw.line(
                surface, color,
                (0, ascent + 1),
                (surface.get_width(), ascent + 1)
            )
        
        # If crop values are provided, crop the surface accordingly
        if crop is not None:
            surface0 = surface
            width = surface0.get_width()
            height = crop[1] - crop[0]
            surface = Surface((width, height))
            area = Rect(0, crop[0], width, height)
            surface.blit(surface0, (0, 0), area)
        
        # Return the final rendered surface
        return surface

    def __str__(self):
        # Return a string representation of the TextStyle
        description = f"{self.__fontName} color:{self.__colorName}"
        if self.italic:
            description += " italic"
        if self.bold:
            description += " bold"
        if self.underline:
            description += " underline"
        return description

    def __eq__(self, i_other: object) -> bool:
        # Check if two TextStyle objects are equal
        if not isinstance(i_other, TextStyle):
            return False
        i_other = cast(TextStyle, i_other)
        return self.__fontName == i_other.__fontName \
               and self.__colorName == i_other.__colorName \
               and self.__flags == i_other.__flags

    def __hash__(self) -> int:
        # Return the hash of the TextStyle
        return hash(self.__fontName) \
               + hash(self.__colorName) \
               + hash(self.__flags)
