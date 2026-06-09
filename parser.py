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


class Parser:

    def __init__(self):
        map_file = argv[1]
        self.start_hub = {}
        self.map = {}
        self.read_map(map_file)

    def read_map(self, map_file: str):
        with open(map_file, "r") as file:
            for line in file:

                if line.startswith('#'):
                    continue

                if line.startswith(("start_hub", "end_hub", "hub")):
                    attributes = line.split()
                    metadati = {}
                    if len(attributes) > 4:
                        metadati = self.metadati_extractor(
                                                    metadati, attributes)

                    zone = Zone(attributes[1],
                                int(attributes[2]), int(attributes[3]),
                                metadati.get("zone_type", "normal"),
                                metadati.get("max_drones", 1),
                                metadati.get("color", None)
                                     )
                    if attributes[0] == "start_hub:":
                        self.start_hub = zone
                    elif attributes[0] == "end_hub:":
                        self.end_hub = zone

                    self.map[attributes[1]] = zone

                elif line.startswith('connection'):
                    attributes = line.split(" ")
                    splitted_zones = line.split("-")
                    metadati = {}
                    if len(attributes) > 4:
                        metadati = self.metadati_extractor(
                                                    metadati, attributes)
                    connection = Connection(splitted_zones[0],
                                            splitted_zones[1],
                                            metadati.get("max_link_capacity",
                                                         1))

                    self.map[attributes[1]] = connection




    def metadati_extractor(self, metadati: dict, attributes: list[str]) -> dict:

        stripped_attr = attributes[4].strip("[]")
        splitted_attr = stripped_attr.split(" ")

        for element in splitted_attr:
            key, value = element.split("=")
            metadati[key] = value

        return metadati


# b_drones: 5
#
# start_hub: hub 0 0 [color=green]
# end_hub: goal 10 10 [color=yellow]
# hub: roof1 3 4 [zone=restricted color=red]
# hub: roof2 6 2 [zone=normal color=blue]
# hub: corridorA 4 3 [zone=priority color=green max_drones=2]
# hub: tunnelB 7 4 [zone=normal color=red]
# hub: obstacleX 5 5 [zone=blocked color=gray]
# connection: hub-roof1
# connection: hub-corridorA
# connection: roof1-roof2
# connection: roof2-goal
# connection: corridorA-tunnelB [max_link_capacity=2]
# connection: tunnelB-go