from sys import argv

class Zone:
    
    def __init__(self, name: str, x: int, y: int, 
                 zone_type: str = "normal",
                 max_drones: int = 1,
                 color: str | None = None):
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.max_drones = max_drones
        self.color = color 


class Connection:

    def __init__(self, zone1: str, zone2: str,
                 max_link_capacity: int = 1):
        self.zone1 = zone1
        self.zone2 = zone2
        self.max_link_capacity = max_link_capacity
        map = {}


class Parser:

    def __init__(self):
        map_file = argv[1];
        self.read_map(map_file)

    def read_map(self, map_file: str):
        with open(map_file, "r") as file:
            for line in file:

                if line.startswith('#'):
                    continue

                if line.startswith("start_hub"):
                    attributes = line.split()
                    stripped_attr = attributes[4].strip("[]")
                    splitted_attr = stripped_attr.split(" ")
                    for element in splitted_attr:
                        if element[0] == "color"


                elif line.startswith("end_hub"):
                    
                elif line.startswith('hub'):
                    
                elif line.startswith('connection'):
                    