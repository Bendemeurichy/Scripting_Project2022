class Errorobj:
    def __init__(self):
        self.error: bool = False
        self.message: str = ""

    def getError(self) -> bool:
        return self.error

    def getMessage(self) -> str:
        return self.message

    def setMessage(self, text: str) -> None:
        self.message = text

    def setError(self, state: bool) -> None:
        self.error = state
