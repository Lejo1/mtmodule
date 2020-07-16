import mtbot
import sys


def callback(command, inp):
    if command == mtbot.p.tc["access_denied"]:
        print("Access Denied: " +
              mtbot.p.accessDeniedStrings[mtbot.bytetonumb(inp)])

    elif command == mtbot.p.tc["access_denied_legacy"]:
        print("Access Denied(legacy): " + mtbot.from_std_wstring(inp))

    elif command == mtbot.p.tc["chat_message"]:
        #sepcial is wstring
        print("chatlog: " + mtbot.from_std_wstring(inp[4:len(inp) - 8]))


t = mtbot.MTClient(sys.argv[1], int(sys.argv[2]),
                   sys.argv[3], sys.argv[4], callback)
t.start()
t.join()
