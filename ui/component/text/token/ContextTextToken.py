from .TextToken import TextToken

class ContentTextToken(TextToken):

    def __init__(self, content: str):
        self.__content = content

    @property
    def content(self) -> str:
        return self.__content