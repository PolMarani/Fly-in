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
        self.occupied = {}

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

    def reconstruct_path(self, destination_zone: str) -> list:
        current = destination_zone
        path = []

        while current is not None:
            path.append(current)
            current = self.came_from[current]

        path.reverse()
        return path

    def compute_turns(self, zone_list: list[str]) -> dict[str, int]:
        drone_turn = {}
        turn = 0

        for zone in zone_list:
            drone_turn[zone] = turn
            if self.zones[zone].zone_type == "restricted":
                turn += 2
            else:
                turn += 1

        return drone_turn

    def update_zone(self, zone_occupied: dict[]):
        for element in self.occupied.items():
            for in self.nb_drones:
                if 
            

if __name__ == "__main__":
    parser = Parser()
    istanza = Pathfinder(parser.zones, parser.connections,
                         parser.nb_drones, parser.start_hub, parser.end_hub)
    print(istanza.find_path())
    path = istanza.reconstruct_path(istanza.end_hub.name)
    print(path)
    print(istanza.compute_turns(path))
