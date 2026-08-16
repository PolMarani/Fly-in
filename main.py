from .map_parser import Parser


if __name__ == "__main__":
    try:
        parser = Parser()
    except ValueError as e:
        print("Parsing error:", e)
        sys.exit(1)
    istanza = Pathfinder(parser.zones, parser.connections,
                         parser.nb_drones, parser.start_hub, parser.end_hub)
    drones_result = istanza.run()
    simulator = Simulator(drones_result)
    simulator.print_output()
