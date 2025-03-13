import logging
from html.parser import HTMLParser
from typing import List, Optional

from .token import ContentTextToken, IconTextToken, ReturnTextToken, TextToken, StyleTextToken
from ...theme.Theme import Theme
from ui.component.text.token.TextStyle import TextStyle


class TextTokenizer(HTMLParser):

    def __init__(self, theme: Theme):
        super(TextTokenizer, self).__init__()
        self.__tokens: List[TextToken] = []
        self.__styleStack: List[TextStyle] = []

        frame = theme.getTileset("frame")
        icons = theme.getTileset("icons")
        self.__tiles = {
            "dungeon": (frame.surface, frame.getTileRect("dungeon")),
            "food": (icons.surface, icons.getTileRect("food")),
            "wood": (icons.surface, icons.getTileRect("wood")),
            "stone": (icons.surface, icons.getTileRect("stone")),
            "gold": (icons.surface, icons.getTileRect("gold")),
        }

    def parse(self, content: str, style: TextStyle) -> List[TextToken]:
        self.__styleStack.clear()
        self.__styleStack.append(style)
        self.__tokens.clear()
        self.feed(content)
        return self.__tokens

    def handle_starttag(self, tag, attrs):
        if tag in self.__tiles:
            tile = self.__tiles[tag]
            token = IconTextToken(tile[0], tile[1])
            self.__tokens.append(token)
        elif tag == "br":
            self.__tokens.append(ReturnTextToken())
        else:
            currentStyle = self.__styleStack[-1]
            newStyle: Optional[TextStyle] = None
            if tag == "i":
                newStyle = currentStyle.styleItalic()
            elif tag == "b":
                newStyle = currentStyle.styleBold()
            elif tag == "u":
                newStyle = currentStyle.styleUnderline()
            elif tag == "s":
                for name, value in attrs:
                    if name == "color":
                        newStyle = currentStyle.styleColor(value)
                    else:
                        logging.warning(f"Invalid attribute {name} for <s>")
            else:
                logging.warning(f"Invalid or unsupported tag {tag}")
            if newStyle is not None:
                self.__styleStack.append(newStyle)
                self.__tokens.append(StyleTextToken(newStyle))

    def handle_data(self, content):
        if len(content) > 0:
            self.__tokens.append(ContentTextToken(content))

    def handle_endtag(self, tag):
        currentStyle = self.__styleStack[-1]
        if tag == "i":
            assert currentStyle.italic
        elif tag == "b":
            assert currentStyle.bold
        elif tag == "u":
            assert currentStyle.underline
        elif tag == "s":
            pass
        else:
            logging.warning(f"Invalid or unsupported end tag {tag}")
        self.__styleStack.pop()
        self.__tokens.append(StyleTextToken(self.__styleStack[-1]))


