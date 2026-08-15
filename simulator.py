class Simulator:
    def __init__(self, all_drone_turns: dict[str, dict[str, int]]):
        self.all_drone_turns = all_drone_turns

    def print_output(self):
        turns = max(max(sotto_dict.values())
                    for sotto_dict in self.all_drone_turns.values())

        for turn in range(1, turns + 1):
            for drone, zones in self.all_drone_turns.items():
                for zone_name, zone_turn in zones.items():
                    if zone_turn == turn:
                        print(f"{drone}-{zone_name}", end=" ")
            print()
