from switch import Switch
from scapy.all import Ether

SRC = "0:1:2:3:4:5"
DST = "0:1:2:3:4:6"

packet = Ether(src=SRC, dst="0:1:2:3:4:1")

s1 = Switch(SRC)
s2 = Switch(DST)

s1.connect_device(s2, port_id=1, dest_port=0)

s1.handle_message(packet, from_port=0)

