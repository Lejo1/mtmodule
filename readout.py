import socket
import select
import mtbot.protocol as p
from mtbot.botpackage import *

class MTServer:
    """Some kind of proxy."""
    psock = {}
    saddr = {}
    pdst = {}

    def __init__(self, adr, dst):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(adr)
        self.destination = dst

    def create_socket(self, addr):
        nsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.psock[str(addr[1])] = nsocket
        self.saddr[str(nsocket.fileno())] = addr
        print("Created socket")

    def receive(self):
        sockets = [self.sock]
        for value in self.psock.values():
            sockets.append(value)

        read_sockets, write_sockets, error_sockets = select.select(sockets, [], [])
        for sock in read_sockets:
            try:
                data, addr = sock.recvfrom(1000)
                if data:
                    if sock == self.sock:
                        self.toserverhandler(sock, data, addr)
                    else:
                        self.toclienthandler(sock, data, addr)

            except Exception as e:
                print("Error: " + str(e))
                return

    def disconnect(self, sock):
        addr = self.saddr[str(sock.fileno())]
        del self.psock[str(addr[1])]
        del self.saddr[str(sock.fileno())]
        sock.close()
        print("disconnected socket")


    def close(self):
        self.sock.close()
        for sock in self.psock:
            sock.close()

    def toserverhandler(self, sock, data, addr):
        #print("ToserverData : %s" % data)
        send = True
        peer_id, channel, type, reliable, seqnum, dat = readPacket(data)
        #TODO find better index!!!
        ad = str(addr[1])
        #preprogressing
        print("t" + str(len(data)) + ":" + type + str(reliable) + str(seqnum) + "dat:" + str(dat))

        if not ad in self.psock:
            self.create_socket(addr)
            self.pdst[ad] = self.destination

        if send:
            self.psock[ad].sendto(data, self.pdst[ad])

        #postprogressing
        if type == "control" and dat:
             ctype = dat[0]
             if ctype == "disco":
                 self.disconnect(self.psock[ad])

    def toclienthandler(self, sock, data, addr):
        #print("ToclientData : %s" % data)
        send = True
        peer_id, channel, type, reliable, seqnum, dat = readPacket(data)
        #preprogressing
        print("f" + str(len(data)) + ":" + type + str(reliable) + str(seqnum) + "dat:" + str(dat))
        if type == "original":
            if dat[0] == p.tc["chat_message"]:
                d = dat[1]
                #len = d[:2]
                msg = d[5:]
                print("msg: " + str(msg))

        if send:
            self.sock.sendto(data, self.saddr[str(sock.fileno())])

        #postprogressing
        if type == "control" and dat:
             ctype = dat[0]
             if ctype == "disco":
                 self.disconnect(sock)

mt = MTServer(("0.0.0.0", 30001), ("185.234.72.95", 30001))

while (1):
    mt.receive()
