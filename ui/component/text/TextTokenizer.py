import logging
from html.parser import HTMLParser
from typing import List, Optional

from .token import ContentTextToken, IconTextToken, ReturnTextToken, TextToken, StyleTextToken
from ...theme.Theme import Theme
from ui.component.text.token.TextStyle import TextStyle

class TextTokenizer(HTMLParser):

    def __init__(self, i_theme: Theme):
        super(TextTokenizer, self).__init__()
        self.__tokens: List[TextToken] = []  # List to store parsed tokens
        self.__styleStack: List[TextStyle] = []  # Stack to manage nested styles
        self.__frameTileset = i_theme.getTileset("frame")  # Get the frame tileset from the theme

    def parse(self, i_content: str, i_style: TextStyle) -> List[TextToken]:
        """Parse the input content and apply the initial style."""
        self.__styleStack.clear()  # Clear the style stack
        self.__styleStack.append(i_style)  # Push the initial style onto the stack
        self.__tokens.clear()  # Clear the tokens list
        self.feed(i_content)  # Parse the content
        return self.__tokens  # Return the list of tokens

    def handle_starttag(self, i_tag, i_attrs):
        """Handle the start of an HTML tag."""
        if i_tag == "flag":
            for name, value in i_attrs:
                if name == "player":
                    try:
                        playerId = int(value)
                        assert 0 <= playerId <= 4
                        token = IconTextToken(
                            self.__frameTileset.surface,
                            self.__frameTileset.getTileRects("flag")[playerId]
                        )
                        self.__tokens.append(token)
                    except:
                        logging.warning(f"Invalid value {value} for attribute {name} for <flag>")
                else:
                    logging.warning(f"Invalid attribute {name} for <s>")
        elif i_tag == "br":
            self.__tokens.append(ReturnTextToken())  # Add a line break token
        elif self.__frameTileset.hasTileRects(i_tag):
            token = IconTextToken(
                self.__frameTileset.surface,
                self.__frameTileset.getTileRect(i_tag)
            )
            self.__tokens.append(token)  # Add an icon token
        else:
            currentStyle = self.__styleStack[-1]
            newStyle: Optional[TextStyle] = None
            if i_tag == "i":
                newStyle = currentStyle.styleItalic()  # Apply italic style
            elif i_tag == "b":
                newStyle = currentStyle.styleBold()  # Apply bold style
            elif i_tag == "u":
                newStyle = currentStyle.styleUnderline()  # Apply underline style
            elif i_tag == "s":
                for name, value in i_attrs:
                    if name == "color":
                        newStyle = currentStyle.styleColor(value)  # Apply color style
                    else:
                        logging.warning(f"Invalid attribute {name} for <s>")
            else:
                logging.warning(f"Invalid or unsupported tag {i_tag}")
            if newStyle is not None:
                self.__styleStack.append(newStyle)  # Push the new style onto the stack
                self.__tokens.append(StyleTextToken(newStyle))  # Add a style token

    def handle_data(self, i_content):
        """Handle the data within an HTML tag."""
        if len(i_content) > 0:
            self.__tokens.append(ContentTextToken(i_content))  # Add a content token

    def handle_endtag(self, i_tag):
        """Handle the end of an HTML tag."""
        currentStyle = self.__styleStack[-1]
        if i_tag == "i":
            assert currentStyle.italic  # Ensure the current style is italic
        elif i_tag == "b":
            assert currentStyle.bold  # Ensure the current style is bold
        elif i_tag == "u":
            assert currentStyle.underline  # Ensure the current style is underline
        elif i_tag == "s":
            pass
        else:
            logging.warning(f"Invalid or unsupported end tag {i_tag}")
        self.__styleStack.pop()  # Pop the current style from the stack
        self.__tokens.append(StyleTextToken(self.__styleStack[-1]))  # Add a style token for the previous style
