class ServiceException(Exception):
    def __init__(self, detail: str = "Service Exception"):
        self.detail = detail
