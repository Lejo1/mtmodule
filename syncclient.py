import mtbot

def callback(command, inp):
    if command == mtbot.p.tc["access_denied"]:
        print("Access Denied: " + mtbot.p.accessDeniedStrings[mtbot.bytetonumb(inp)])

    elif command == mtbot.p.tc["access_denied_legacy"]:
        print("Access Denied(legacy): " + mtbot.from_std_wstring(inp))

    elif command == mtbot.p.tc["chat_message"]:
        #sepcial is wstring
        print("chatlog: " + mtbot.from_std_wstring(inp[4:len(inp) - 8]))

mt = mtbot.MTClient(("subgames.minetest.land", 30001), "Lejo", "youthought", callback)
try:
    mt.run()
except KeyboardInterrupt:
    mt.close()
