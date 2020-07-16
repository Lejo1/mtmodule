from antiafkkick import mtbotnoafk
import sys
from time import sleep

addr = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]
pw = sys.argv[4]
amount = int(sys.argv[5])
clients = []

def callback(command, inp):
    if command == mtbotnoafk.p.tc["access_denied"]:
        print("Access Denied: " +
              mtbotnoafk.p.accessDeniedStrings[mtbotnoafk.bytetonumb(inp)])

    elif command == mtbotnoafk.p.tc["access_denied_legacy"]:
        print("Access Denied(legacy): " + mtbotnoafk.from_std_wstring(inp))

try:
    for i in range(amount):
        t = mtbotnoafk((addr, port), name + str(i), pw, callback)
        t.start()
        sleep(1)
        clients.append(t)

    for i in range(len(clients)):
        clients[i].join()
except KeyboardInterrupt:
    for i in range(len(clients)):
        clients[i].close()
