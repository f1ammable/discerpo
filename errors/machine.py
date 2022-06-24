from . import logger

__all__ = (
    "InvalidMachinePE",
    "InvalidMagic",
)
class InvalidMachinePE(Exception):
    def __init__(self, header):
        self.header = header
        super().__init__()

    def __str__(self):
        logger.error(f'Machine type from PE header {self.header} does not match valid machine types')
        return "Machine type not supported"


class InvalidMagic(Exception):
    def __init__(self, magic):
        self.magic = magic
        super().__init__()

    def __str__(self):
        logger.error(f'Magic bytes {self.magic} does not match valid magic bytes')
        return "Invalid Magic bytes"

# Both of these errors only log to the logger as of now
