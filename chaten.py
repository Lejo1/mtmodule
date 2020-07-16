from antiafkkick import mtbotnoafk
import sys
from mtbot.botpackage import to_std_wstring, from_std_wstring, bytetonumb
from time import sleep

addr = sys.argv[1]
port = int(sys.argv[2])
name = sys.argv[3]
pw = sys.argv[4]
msg = ""
for v in sys.argv[5:]:
    msg += v + " "
msg = to_std_wstring(msg)


t = mtbotnoafk((addr, port), name, pw)
try:
    t.start()
    while 1:
        sleep(5)
        t.add_pack("chat_message", msg)
except KeyboardInterrupt:
    t.close()
