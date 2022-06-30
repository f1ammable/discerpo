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
        return f'Machine type from PE header ```{self.header}``` does not match valid machine types'


class InvalidMagic(Exception):
    def __init__(self, magic):
        self.magic = magic
        super().__init__()

    def __str__(self):
        return f'Magic bytes ```{self.magic}``` does not match valid magic bytes'
