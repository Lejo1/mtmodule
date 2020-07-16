import socket
from time import sleep
from threading import Thread, Lock
from mtbot.botpackage import *
# build from C
# pip3 install srp
import srp

srp.rfc5054_enable() 

class MTClient(Thread):

    """
    Creates a MT Client without any visual gui.

    MTClient(("coolserver.com", 30000), "Foo", "Bar", callbackfunction)

    callbackfunction will be called on original packages
    callbackfunction(command, data)
    You may use the botpackage functions and protocol to identify
    the command and data
    IMPORANT: Runs in the client thread!!!

        Child class of threading.Thread

        start()                 Start the login/join process
        close()                 Stop and close the Client
        joined()                Check if client is joined already
        add_pack(command, data) Packets to send, will be send when joined

    """

    def __init__(self, addr, name, password, callback=None):
        super().__init__(target=self.do, name="MTBOT-" + name)
        self.addr = addr
        self.name = name
        self.password = password
        self.callback = callback
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(29)
        self.state = 0
        self.peer_id = b"\x00\x00"
        self.actions = []
        self.active = False
        self.seq = [Seqnum(), Seqnum(), Seqnum()]
        self.actionlock = Lock()

    def __del__(self):
        self.sock.close()

    def connect(self):
        print("Requesting peer...")
        # get peer_id and build connection (send empty package)
        self.packori("get_peer")

    def add_pack(self, command, data):
        self.actionlock.acquire()
        self.actions.append((command, data))
        self.actionlock.release()

    def joined(self):
        return self.state == 4

    def init(self):
        print("Sending init...")
        self.packori("init", p.serialization_version + b"\x00\x00" +
                     p.protocol_version_min + p.protocol_version_max + std_string(self.name))
        sleep(0.05)

    def send(self, channel, data):
        buf = makePacket(self.peer_id, channel, data)
        self.raw_send(buf)

    def raw_send(self, data):
        #print("t: %s" % data)
        self.sock.sendto(data, self.addr)

    def packori(self, command, data=-1):
        channel, reliable = p.ts_commandspecs[command]
        d = makeDataOriginal(p.ts[command], data)
        if reliable:
            obj = self.seq[channel]
            s = obj.get()
            d = makePacket(self.peer_id, channel, makeDataReliable(s, d))
            obj.buffer(s, d)
            self.raw_send(d)
        else:
            d = makePacket(self.peer_id, channel, d)
            self.raw_send(d)

    def do(self):
        self.active = True
        self.connect()
        while self.active:
            if self.state == 1:
                self.init()
            elif self.joined() and self.actions:
                self.actionlock.acquire()
                for i in range(len(self.actions)):
                    self.packori(self.actions[i][0], self.actions[i][1])
                    self.actions.pop(i)

                self.actionlock.release()

            self.receive()

    def receive(self):
        try:
            data, addr = self.sock.recvfrom(1000)
            if self.active:
                if data:
                    #print("f: %s" % data)
                    self.processpackage(data)
                else:
                    print("Timed out!")

        except Exception as e:
            print("Error: " + str(e))
            return

    def close(self):
        self.active = False
        self.send(0, makeDataControl(p.controltype["disco"]))
        self.sock.close()
        print("Closed Sockets!")

    def processpackage(self, data):
        # Serializing Packet
        peer_id, channel, type, reliable, seqnum, dat = readPacket(data)
        if peer_id == p.server_peer_id:

            # send acks
            if reliable:
                self.send(channel, makeDataControl(
                    p.controltype["ack"], seqnum))

            if type == "control" and dat:
                ctype = dat[0]
                if ctype == "ack":
                    obj = self.seq[channel]
                    obj.pop(dat[1])
                elif ctype == "set_peer_id":
                    self.state = 1
                    self.peer_id = dat[1]
                elif ctype == "disco":
                    print("Closing socket got disco package")
                    self.close()

            # Normal Packet handler for all original packets
            elif type == "original":
                command = dat[0]
                inp = dat[1]
                # print("Original Package Command: %s Data: %s" %
                #      (p.get(command), inp))
                if command == p.tc["hello"]:
                    print("Got Hello Auth Method:")
                    self.state = 2
                    auth = inp[5:9]
                    username = std_stringtobyte(inp[9:]).decode()
                    #print("username is " + username)
                    #print("auth is: %s" % auth)
                    if auth == p.authmechanism["srp"] or auth == p.authmechanism["legacy"]:
                        print("legacy/srp")
                        based_on = b"\x01"
                        if auth == p.authmechanism["legacy"]:
                            self.password = translate_password(
                                username, self.password)
                            based_on = b"\x00"

                        print("s")
                        self.auth_data = srp.User(
                            username.lower(), self.password)
                        username, bytes_a = self.auth_data.start_authentication()
                        print("s2")
                        #print("bytes_a:" + str(bytes_a))
                        self.packori("srp_bytes_a", std_string(
                            bytes_a) + based_on)
                    elif auth == p.authmechanism["first_srp"]:
                        print("first_srp")
                        print("s")
                        salt, verifier = srp.create_salted_verification_key(
                            username.lower(), self.password)
                        print("s2")
                        empty = b"\x00"
                        if self.password == "":
                            empty = b"\x01"

                        self.packori("first_srp", std_string(
                            salt) + std_string(verifier) + empty)

                elif command == p.tc["srp_bytes_s_b"]:
                    if self.auth_data:
                        #bs_len = bytetonumb(inp[:2])
                        bytes_s = std_stringtobyte(inp[2:18])
                        #bb_len = bytetonumb(inp[(bs_len+3):(bs_len+5)])
                        bytes_b = std_stringtobyte(inp[18:])
                        print("bytes are: %s and %s" % (bytes_s, bytes_b))
                        bytes_M = self.auth_data.process_challenge(
                            bytes_s, bytes_b)
                        if bytes_M:
                            print("sending srp_bytes_m: %s" % bytes_M)
                            self.packori("srp_bytes_m", std_string(bytes_M))
                        else:
                            print("Srp bytes_s_b check failed!")
                    else:
                        print("Got srp_bytes_s_b without prior created auth data")

                elif command == p.tc["auth_accept"]:
                    print("Auth accepted, sening init2")
                    self.state = 3
                    self.packori("init2", std_string(b"de"))

                elif command == p.tc["csm_restriction_flags"]:
                    # Last init thing sent, client_Ready afterwards
                    self.state = 4
                    print("Sending client ready, Ready!")
                    self.packori("client_ready", p.version)

                if self.callback:
                    self.callback(command, inp)

            # Handle resending
            for c in range(len(self.seq)):
                obj = self.seq[c]
                d = obj.toresend()
                if d:
                    for buf in d:
                        print("resending: %s" % buf)
                        self.raw_send(buf)
