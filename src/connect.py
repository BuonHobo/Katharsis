import sys

from Kathara.manager.Kathara import Kathara

print("Connecting to", sys.argv[1] + "...")

while True:
    Kathara.get_instance().connect_tty(machine_name=sys.argv[1], lab_hash=sys.argv[2])
