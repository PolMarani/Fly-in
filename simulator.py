from map_parser import Zone

START = "\033[92m"
END = "\033[91m"
BLOCKED = "\033[31m"
ZONE = "\033[36m"
DRONE = "\033[33m"
CONNECTION = "\033[34m"
RESET = "\033[0m"


class Simulator:
    def __init__(self,
                 all_drone_turns: dict[str, dict[str, int]],
                 start_hub: Zone,
                 end_hub: Zone,
                 zones: dict[str, Zone]):
        self.all_drone_turns = all_drone_turns
        self.start_hub = start_hub
        self.end_hub = end_hub
        self.zones = zones

    def print_output(self):
        turns = max(max(sotto_dict.values())
                    for sotto_dict in self.all_drone_turns.values())

        print("Begin simulation:")
        print()
        for turn in range(1, turns + 1):
            for drone, drone_zones in self.all_drone_turns.items():
                for zone_name, zone_turn in drone_zones.items():
                    if zone_turn == turn:
                        if zone_name == self.start_hub.name:
                            color = START
                        elif zone_name == self.end_hub.name:
                            color = END
                        elif '-' in zone_name:
                            color = CONNECTION
                        elif self.zones[zone_name].zone_type == "blocked":
                            color = BLOCKED
                        else:
                            color = ZONE
                        print(
                            f"{DRONE}{drone}{RESET}-{color}{zone_name}{RESET}",
                            end=" ")

            print()

        print()
        print("Simulation ended")
