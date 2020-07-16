from mtbot import MTClient

class mtbotnoafk(MTClient):
    """docstring for mtbotnoafk."""

    def __init__(self, addr, name, password, callback=None):
        super().__init__(addr, name, password, callback=None)

    def start(self):
        super().start()
        super().add_pack("playerpos", b'\xff\xff\xec\xa4\x00\t-\x9c\x00\x00=)\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0b\xa3\x00\x00\x8cO\x00\x00\x00\x01\x85\x04')
