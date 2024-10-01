class NotFoundException(Exception):
    def __init__(self, message: str = "Entity not found"):
        self.message = message
        super().__init__(self.message)


class BadRequestException(Exception):
    def __init__(self, message: str ="The server cannot or will not process the request due to something that is perceived to be a client error"):
        self.message = message
        super().__init__(self.message)