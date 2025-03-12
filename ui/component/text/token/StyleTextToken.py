from .TextToken import TextToken
from .TextStyle import TextStyle


class StyleTextToken(TextToken):

    def __init__(self, i_style: TextStyle):
        self.__style = i_style

    @property
    def style(self) -> TextStyle:
        return self.__style
