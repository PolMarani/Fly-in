from map_parser import Zone, Connection
import heapq


class Pathfinder:
    def __init__(self,
                 zones: dict[str, Zone],
                 connections: dict[str, Connection],
                 nb_drones: int,
                 start_hub: Zone,
                 end_hub: Zone):
        self.nb_drones = nb_drones
        self.zones = zones
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.connections = connections
        self.costs = {}
        self.queue = []

    def find_path(self) -> list[Zone | Connection]:
        self.costs = {element: float("inf") for element in self.zones}
        self.costs[self.start_hub.name] = 0
        heapq.heappush(self.queue, (0, self.start_hub.name))

        while self.queue:
            cost, zone = heapq.heappop(self.queue)
            for element in self.connections.values():
                if element.zone1 == zone or element.zone2 == zone:
                    neighbor = (element.zone1
                                if element.zone1 == zone else element.zone2)
                zone_type = self.zones[neighbor].zone_type
                total_cost = cost + (2 if zone_type == "restricted" else 1)
