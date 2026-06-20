from map_parser import Zone, Connection, Parser
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
        self.came_from = {element: None for element in self.zones}

    def find_path(self) -> list[Zone | Connection]:
        self.costs = {element: float("inf") for element in self.zones}
        self.costs[self.start_hub.name] = 0
        heapq.heappush(self.queue, (0, self.start_hub.name))

        while self.queue:
            cost, zone = heapq.heappop(self.queue)
            for element in self.connections.values():
                if element.zone1 == zone or element.zone2 == zone:
                    neighbor = (element.zone2
                                if element.zone1 == zone else element.zone1)
                    if self.zones[neighbor].zone_type == "blocked":
                        continue
                    zone_type = self.zones[neighbor].zone_type
                    total_cost = cost + (2 if zone_type == "restricted" else 1)
                    if total_cost < self.costs[neighbor]:
                        self.costs[neighbor] = total_cost
                        heapq.heappush(self.queue, (total_cost, neighbor))
                        self.came_from[neighbor] = zone

        return self.costs


if __name__ == "__main__":
    parser = Parser()
    istanza = Pathfinder(parser.zones, parser.connections,
                         parser.nb_drones, parser.start_hub, parser.end_hub)
    print(istanza.find_path())
