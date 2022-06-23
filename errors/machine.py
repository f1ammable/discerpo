

__all__ = (
    "InvalidMachinePE",
    "InvalidMagic",
)


class WarnColours:
    ERR = '\033[93m'
    RESET = '\033[0m'

# The above is not windows compatible (specifically cmd)
# While I doubt that a lot of people will care or try to host this on windows
# I'll try and find a fix for this


class InvalidMachinePE(Exception):
    def __init__(self, header, message='does not match valid machine types'):
        self.header = header
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Identified machine type from PE header -> {WarnColours.ERR + self.header} {WarnColours.RESET + self.message}'


class InvalidMagic(Exception):
    def __init__(self, magic, message='does not match a valid executable file'):
        self.magic = magic
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Identified magic bytes from file header -> {WarnColours.ERR + self.magic} {WarnColours.RESET + self.message}'
