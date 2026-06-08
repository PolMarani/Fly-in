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
    