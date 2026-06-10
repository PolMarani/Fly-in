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
        zones_file = argv[1]
        self.nb_drones = 0
        self.start_hub = {}
        self.zones = {}
        self.connections = {}
        self.read_zones(zones_file)

    def read_zones(self, zones_file: str):
        with open(zones_file, "r") as file:
            for line in file:

                if line.startswith('#'):
                    continue

                line = line.strip()

                if line.startswith(("nb_drones")):
                    elements = line.split()
                    self.nb_drones = int(elements[1])

                if line.startswith(("start_hub", "end_hub", "hub")):
                    elements = line.split()
                    metadati = {}
                    if len(elements) > 4:
                        metadati = self.metadati_extractor(
                                                    metadati, elements[4:])

                    zone = Zone(elements[1],
                                int(elements[2]), int(elements[3]),
                                metadati.get("zone", "normal"),
                                int(metadati.get("max_drones", 1)),
                                metadati.get("color", None)
                                )
                    if elements[0] == "start_hub:":
                        self.start_hub = zone
                    elif elements[0] == "end_hub:":
                        self.end_hub = zone

                    self.zones[elements[1]] = zone

                elif line.startswith('connection'):
                    elements = line.split(" ")
                    first_zone, second_zone = elements[1].split("-")
                    metadati = {}
                    if len(elements) >= 3:
                        metadati = self.metadati_extractor(
                                                    metadati, elements[2:])
                    connection = Connection(first_zone,
                                            second_zone,
                                            int(metadati.get(
                                                "max_link_capacity", 1)))

                    self.connections[elements[1]] = connection

    def metadati_extractor(self, metadati: dict, elements: list[str]) -> dict:
        elements = " ".join(elements)
        stripped_attr = elements.strip("[]")
        splitted_attr = stripped_attr.split(" ")

        for element in splitted_attr:
            if element == "":
                continue
            key, value = element.split("=")
            metadati[key] = value

        return metadati
