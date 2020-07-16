import mtbot.protocol as p
from hashlib import sha1
from base64 import b64encode
from time import time

# Class for seqnums
# And Packetbuffer later


class Seqnum:
    """docstring for Seqnum.
    Managing mt seqnums"""

    def __init__(self):
        self.seqs = {}
        self.next = p.seqnum_initial

    def pop(self, seq):
        key = str(int.from_bytes(seq, "big") - p.seqnum_initial)
        if key in self.seqs:
            self.seqs.pop(key)

    def get(self):
        s = self.next
        self.next += 1
        if self.next > p.seqnum_max:
            self.next = p.seqnum_initial

        return s.to_bytes(2, byteorder="big")

    def buffer(self, seq, buf):
        self.seqs[str((int.from_bytes(seq, "big") - p.seqnum_initial))] = (buf, time())

    def toresend(self):
        out = []
        for i in self.seqs:
            buf, t = self.seqs[i]
            if t+2 < time():
                out.append(buf)
                self.seqs[i] = (buf, time())

        return out

def translate_password(name, password):
    if len(password) == 0:
        return ""

    sr = name + password
    sh = sha1(sr).digest()
    return b64encode(sh)


def std_string(sr):
    n = sr
    if isinstance(sr, str):
        n = sr.encode()
    return numbtobyte(len(n), 2) + n


def from_std_wstring(string):
    newstring = ""
    for i in range(len(string[2:])):
        s = string[i + 2]
        if s != 0:
            newstring += chr(s)

    return newstring


def to_std_wstring(string):
    newbyte = b""
    len = 0
    for i in string:
        len += 1
        newbyte += b"\x00" + i.encode()

    return numbtobyte(len, 2) + newbyte


def std_stringtobyte(bytes):
    return bytes[2:]


def bytetonumb(bytes):
    return int.from_bytes(bytes, "big")


def numbtobyte(numb, size=1):
    return numb.to_bytes(size, byteorder="big")

# access the bytes in the array using byt[4:5] instead of byt[4] to get binary data.


def makePacket(peer_id, channel, data):
    byt = p.protocol_id
    byt += peer_id
    byt += p.channel[channel]
    byt += data
    return byt


def makeDataControl(controltype, cdata=b""):
    byt = p.packagetype["control"]
    byt += controltype
    if cdata != -1:
        byt += cdata

    return byt


def makeDataOriginal(command, data=-1):
    byt = p.packagetype["original"]
    byt += command
    if data != -1:
        byt += data

    return byt


def makeDataReliable(seqnum, data):
    byt = p.packagetype["reliable"]
    byt += seqnum
    byt += data
    return byt


def readPacket(data):
    if len(data) >= 9:
        if data[:4] == p.protocol_id:
            peer_id = data[4:6]
            channel = data[6]
            type = data[7:8]
            reliable = False
            seqnum = b"\x00"
            if type == p.packagetype["control"]:
                type, data = "control", readControl(data[7:])
            elif type == p.packagetype["original"]:
                type, data = "original", readOriginal(data[7:])
            elif type == p.packagetype["split"]:
                type, data = "split", data[7:]
            elif type == p.packagetype["reliable"]:
                reliable = True
                seqnum, type, data = readReliable(data[7:])

            return peer_id, channel, type, reliable, seqnum, data

    return False


def readControl(data):
    controltype = data[1:2]
    if controltype == p.controltype["ack"]:
        seqnum = data[2:4]
        return "ack", seqnum
    elif controltype == p.controltype["set_peer_id"]:
        peer_id = data[2:4]
        return "set_peer_id", peer_id
    elif controltype == p.controltype["disco"]:
        return "disco", "a"


def readOriginal(data):
    command = data[1:3]
    data = data[3:]
    return command, data


def readReliable(data):
    seqnum = data[1:3]
    type = data[3:4]
    if type == p.packagetype["control"]:
        return seqnum, "control", readControl(data[3:])
    elif type == p.packagetype["original"]:
        return seqnum, "original", readOriginal(data[3:])
    elif type == p.packagetype["split"]:
        return seqnum, "split", data[3:]
