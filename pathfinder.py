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
        self.costs: dict[str, int | float] = {}
        self.queue: list[tuple[int, str]] = []
        self.came_from: dict[str, str | None] = {element: None
                                                 for element in self.zones}
        self.occupied: dict[tuple[str, int], int] = {}
        self.link_occupied: dict[tuple[tuple[str, str], int], int] = {}

    def find_path(self) -> None:
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

                    sorted_zones = sorted((element.zone1, element.zone2))
                    zone_pair = (sorted_zones[0], sorted_zones[1])

                    while (self.link_occupied.get(
                        (zone_pair, total_cost), 0) >=
                           element.max_link_capacity):
                        total_cost += 1
                    while self.occupied.get((neighbor, total_cost), 0) >= (
                            self.zones[neighbor].max_drones):
                        total_cost += 1
                    if total_cost < self.costs[neighbor]:
                        self.costs[neighbor] = total_cost
                        heapq.heappush(self.queue, (total_cost, neighbor))
                        self.came_from[neighbor] = zone

    def reconstruct_path(self, destination_zone: str) -> list:
        current: str | None = destination_zone
        path = []

        while current is not None:
            path.append(current)
            current = self.came_from[current]

        path.reverse()
        return path

    def compute_turns(self, zone_list: list[str]) -> dict[str, int]:
        drone_turn = {}

        for i in range(len(zone_list)):
            drone_turn[zone_list[i]] = int(self.costs[zone_list[i]])
            if i + 1 < len(zone_list):
                if self.zones[zone_list[i+1]].zone_type == "restricted":
                    drone_turn[zone_list[i] + "-" + zone_list[i+1]] = (
                        int(self.costs[zone_list[i+1]] - 1))

        return drone_turn

    def update_zone(self, drone_turns: dict[str, int]) -> None:
        for zone, turn in drone_turns.items():
            if (zone, turn) in self.occupied:
                self.occupied[(zone, turn)] += 1
            else:
                self.occupied[(zone, turn)] = 1

    def update_link(self, zone_list: list[str],
                    drone_turns: dict[str, int]) -> None:
        for i in range(len(zone_list) - 1):
            sorted_zones = sorted((zone_list[i], zone_list[i+1]))
            zone_pair = (sorted_zones[0], sorted_zones[1])

            if (zone_pair, drone_turns[zone_list[i+1]]) in self.link_occupied:
                self.link_occupied[(zone_pair,
                                    drone_turns[zone_list[i+1]])] += 1
            else:
                self.link_occupied[(zone_pair,
                                    drone_turns[zone_list[i+1]])] = 1

    def run(self) -> dict:
        all_drone_turns: dict[str, dict[str, int]] = {}

        for drone in range(self.nb_drones):
            self.find_path()
            path = self.reconstruct_path(self.end_hub.name)
            turns = self.compute_turns(path)
            self.update_zone(turns)
            self.update_link(path, turns)
            all_drone_turns["D" + str(drone + 1)] = turns

        return all_drone_turns
