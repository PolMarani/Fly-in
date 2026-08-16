from sys import argv


class Zone:
    def __init__(self, name: str, x: int, y: int,
                 zone_type: str = "normal",
                 max_drones: int = 1,
                 color: str | None = None) -> None:
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
    def __init__(self) -> None:
        zones_file = argv[1]
        self.nb_drones = 0
        self.start_hub = Zone | None
        self.end_hub = Zone | None
        self.zones = {}
        self.connections = {}
        self.seen_connections = set()
        self.read_zones(zones_file)

    def read_zones(self, zones_file: str) -> None:
        with open(zones_file, "r") as file:

            for i, line in enumerate(file, start=1):
                try:
                    line = line.strip()

                    if line.startswith('#') or not line:
                        continue

                    if line.startswith(("nb_drones")):
                        elements = line.split()
                        self.nb_drones = int(elements[1])
                        if self.nb_drones <= 0:
                            raise ValueError("Number of drones not a "
                                             "positive number")

                    elif line.startswith(("start_hub", "end_hub", "hub")):
                        elements = line.split()
                        metadati: dict[str, str] = {}
                        if len(elements) > 4:
                            metadati = self.metadati_extractor(
                                                        metadati, elements[4:])

                        zone_control = metadati.get("zone", "normal")
                        if zone_control not in ('normal', 'blocked',
                                                'restricted', 'priority'):
                            raise ValueError(f"Not a valid zone type."
                                             f" Attribute value of "
                                             f"{zone_control}")

                        max_drones_control = int(metadati.get("max_drones", 1))
                        if max_drones_control <= 0:
                            raise ValueError("Max drones not > 0")
                        if elements[1] in self.zones:
                            raise ValueError("Zones duplicated")

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

                        if (tuple(sorted((first_zone, second_zone)))
                                in self.seen_connections):
                            raise ValueError("Zone repetition, not valid mhmh")
                        self.seen_connections.add(tuple(sorted((first_zone,
                                                                second_zone))))
                        if (first_zone not in self.zones or
                                second_zone not in self.zones):
                            raise ValueError("Not valid connection")

                        metadati = {}
                        if len(elements) >= 3:
                            metadati = self.metadati_extractor(
                                                        metadati, elements[2:])
                        max_link_capacity_control = int(metadati.get(
                            "max_link_capacity", 1))
                        if max_link_capacity_control <= 0:
                            raise ValueError("Max link capacity not > 0")
                        connection = Connection(first_zone,
                                                second_zone,
                                                int(metadati.get(
                                                    "max_link_capacity", 1)))
                        self.connections[elements[1]] = connection

                    else:
                        raise ValueError("Valore non riconosciuto")

                except ValueError as e:
                    raise ValueError(f"{e}\n"
                                     f"in line {i}, value: ---{line}---")

            if not self.start_hub:
                raise ValueError("No start_hub definition in file")
            if not self.end_hub:
                raise ValueError("No end_hub definition in file")

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
