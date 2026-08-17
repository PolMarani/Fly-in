*This project has been created as part of the 42 curriculum by pmarani.*

# 🎮🚁 Fly-in

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![flake8](https://img.shields.io/badge/flake8-passing-brightgreen)
![mypy](https://img.shields.io/badge/mypy-strict%20flags-blue)
![Paradigm](https://img.shields.io/badge/paradigm-OOP-orange)
![Dependencies](https://img.shields.io/badge/dependencies-stdlib%20only-lightgrey)

A drone-fleet routing simulator: multiple drones travel across a graph of zones, from a shared start to a shared end, in the fewest possible simulation turns — respecting zone types, zone capacity, and connection capacity.

## 📋 Table of Contents

- [📖 Description](#description)
- [⚙️ Instructions](#instructions)
- [🧠 Algorithm and Design](#algorithm-and-design)
- [🗺️ Input File Format](#input-file-format)
- [📤 Output Format](#output-format)
- [🎨 Visual Representation](#visual-representation)
- [🛡️ Parser Validation](#parser-validation)
- [🧩 Challenges Faced](#challenges-faced)
- [🏁 Performance](#performance)
- [🎁 Bonus](#bonus)
- [📁 Project Structure](#project-structure)
- [📚 Resources and AI Usage](#resources-and-ai-usage)

## 📖 Description

Fly-in routes a fleet of `nb_drones` drones from a single `start_hub` to a single `end_hub` through a network of connected zones, described in a custom text map format. Each zone has a type that affects movement cost (`normal`, `priority`, `restricted`, `blocked`) and a maximum simultaneous occupancy (`max_drones`); each connection between zones has a maximum simultaneous traversal capacity (`max_link_capacity`).

The simulation must:

- Move every drone from start to end in as few total turns as possible
- Respect zone and connection capacity at every turn
- Handle drones waiting when a path is temporarily blocked
- Produce a turn-by-turn log of every drone movement

No graph library (`networkx`, `graphlib`, etc.) is used — the graph, the priority-queue pathfinding, and the whole simulation are implemented from scratch in an object-oriented design.

## ⚙️ Instructions

**Requirements:** Python 3.10+

```bash
make install               # installs flake8 and mypy (requirements.txt)
make run                   # runs the simulation on the bundled map.txt
make run MAP=other.txt     # runs the simulation on a custom map file
make debug                 # runs the simulation under pdb
make lint                  # flake8 + mypy with the flags required by the subject
make clean                 # removes __pycache__ and .mypy_cache
```

`run.py` is the entry point; it wires `Parser` → `Pathfinder` → `Simulator` together.

## 🧠 Algorithm and Design

- **Pathfinding — Dijkstra's algorithm.** Each drone's shortest weighted path from `start_hub` to `end_hub` is computed with Dijkstra's algorithm, implemented on top of Python's `heapq` as the priority queue. Movement cost depends on the destination zone's type: `normal` and `priority` cost 1 turn, `restricted` costs 2 turns, `blocked` is never entered.
- **Multi-drone scheduling — sequential greedy.** Drones are routed one at a time, not solved jointly. After each drone's path is found, the zones and connections it occupies at each turn are recorded in two occupancy registries (`Pathfinder.occupied` for zones, `Pathfinder.link_occupied` for connections). Every later drone's Dijkstra run checks these registries and "waits" — pushing its candidate arrival turn forward — until a slot respecting `max_drones` / `max_link_capacity` is free.
- **Design trade-off.** This sequential approach is simpler to implement and reason about than a fully joint multi-agent scheduler (e.g. a time-expanded graph solved for all drones at once), but it is **not guaranteed to be globally optimal**: an earlier drone occupying a zone can force a later drone into a longer wait that a joint solver might have avoided. It was chosen deliberately to guarantee a correct, working mandatory part within the project's time constraints.
- **Restricted-zone transit.** Since a `restricted` zone costs 2 turns to enter, a drone spends one intermediate turn "in flight" on the connection leading to it. This is tracked as an extra entry in the per-drone turn schedule and surfaces in the output as `D<ID>-<connection-name>` instead of `D<ID>-<zone-name>`, exactly as the subject specifies.
- **Undirected connections.** The map format allows a connection to be traversed in either direction. Internally, the two zone names of a connection are normalized (sorted alphabetically) before being used as a dictionary key, so `hub-roof1` and `roof1-hub` always resolve to the same occupancy slot.
- **Complexity and memory.** For a single drone, Dijkstra over `Z` zones and `C` connections runs in `O((Z + C) log Z)` with a binary heap. For `N` drones routed sequentially, the total cost is `O(N · (Z + C) log Z)` — each drone triggers a fresh Dijkstra run; nothing is cached between drones, since occupancy changes after every drone and would invalidate a cached path anyway. Memory usage is dominated by the occupancy dictionaries, which grow with the number of distinct `(zone, turn)` and `(connection, turn)` pairs actually visited — bounded by the total number of turns across all drones, not by the map size alone.

## 🗺️ Input File Format

| Line type | Syntax | Example |
|---|---|---|
| Drone count | `nb_drones: <int>` | `nb_drones: 2` |
| Start zone | `start_hub: <name> <x> <y> [metadata]` | `start_hub: hub 0 0 [color=green]` |
| End zone | `end_hub: <name> <x> <y> [metadata]` | `end_hub: goal 10 10 [color=yellow]` |
| Regular zone | `hub: <name> <x> <y> [metadata]` | `hub: roof1 3 4 [zone=restricted color=red]` |
| Connection | `connection: <zone1>-<zone2> [metadata]` | `connection: hub-roof1` |
| Comment | `# ...` | `# ignored by the parser` |

| Zone type | Turn cost to enter | Notes |
|---|---|---|
| `normal` (default) | 1 | — |
| `priority` | 1 | preferred by the algorithm when costs tie |
| `restricted` | 2 | drone occupies the connection for the extra turn |
| `blocked` | — | never entered; any path through it is invalid |

Full example (bundled as `map.txt`):

```text
nb_drones: 5

start_hub: hub 0 0 [color=green]
end_hub: goal 10 10 [color=yellow]
hub: roof1 3 4 [zone=restricted color=red]
hub: roof2 6 2 [zone=normal color=blue]
hub: corridorA 4 3 [zone=priority color=green max_drones=2]
hub: tunnelB 7 4 [zone=normal color=red]
hub: obstacleX 5 5 [zone=blocked color=gray]

connection: hub-roof1
connection: hub-corridorA
connection: roof1-roof2
connection: roof2-goal
connection: corridorA-tunnelB [max_link_capacity=2]
connection: tunnelB-goal
```

## 📤 Output Format

One line per simulation turn, listing every drone that moved that turn as `D<ID>-<zone>` (or `D<ID>-<connection>` while in transit through a `restricted` zone). Drones that don't move that turn are omitted; drones that reach `end_hub` are no longer tracked.

Actual output of `make run` on the bundled `map.txt` (5 drones):

```text
Begin simulation:

D1-corridorA D2-hub-roof1
D1-tunnelB D2-roof1 D3-corridorA D4-hub-roof1
D1-goal D2-roof2 D3-tunnelB D4-roof1 D5-corridorA
D2-goal D4-roof2 D5-tunnelB
D3-goal
D4-goal
D5-goal

Simulation ended
 in 7 turns
```

`D1` takes the `corridorA → tunnelB → goal` path first, since nothing is occupied yet. `D2` takes `roof1 → roof2 → goal`, spending turn 1 in transit on the `hub-roof1` connection before entering the `restricted` zone `roof1` on turn 2. `D3`–`D5` reuse the same two routes, each waiting where a zone or connection is already at capacity from an earlier drone (e.g. `corridorA` allows `max_drones=2`, so `D3` has to wait for `D1` to clear it before entering).

## 🎨 Visual Representation

Terminal output is colored using raw ANSI escape codes (no external dependency such as `colorama`, so `make install` stays minimal):

| Element | Color |
|---|---|
| Drone ID (`D1`, `D2`, ...) | Yellow |
| Start zone | Bright green |
| End zone | Bright red |
| Normal / priority zone | Cyan |
| Blocked zone | Red |
| Connection (in-transit, restricted) | Blue |

Coloring drone IDs separately from destinations makes it possible to scan a turn's line and immediately tell *which* drone went *where* without reading every token, and to spot at a glance when a drone is mid-transit on a connection rather than parked in a zone.

## 🛡️ Parser Validation

- **`nb_drones`** must be a positive integer
- Exactly **one `start_hub`** and **one `end_hub`** must be present
- **Zone type**, if given, must be one of `normal`, `blocked`, `restricted`, `priority`
- **`max_drones`** and **`max_link_capacity`**, if given, must be positive integers
- **Zone names** must be unique
- **Connections** must reference zones that were already defined
- **Duplicate connections** are rejected (`a-b` and `b-a` count as the same connection)
- Any **unrecognized line format** raises an error
- **Malformed values** (e.g. non-integer coordinates) raise an error instead of crashing with a raw traceback

Every parsing error reports the exact line number and the offending line content, then the program exits cleanly (`sys.exit(1)`) instead of printing a Python traceback.

## 🧩 Challenges Faced

- **Turns computed independently of the capacity waits Dijkstra had already resolved.** The most significant bug found: `find_path` correctly computes `self.costs[zone]` *including* any waiting needed to respect `max_drones` / `max_link_capacity`. But `compute_turns` — used to build the final per-drone schedule — recomputed turn numbers from scratch (`turn = 0`, `+1`/`+2` per zone) instead of reading `self.costs`, silently discarding every wait Dijkstra had calculated. The chosen *route* was always correct; the *turn numbers* attached to it were not. This was invisible on the small example map, but running the official easy/medium/hard benchmark maps and writing a small script to check every turn's occupancy against each zone's `max_drones` and each connection's `max_link_capacity` surfaced it immediately — every single benchmark map had multiple capacity violations. Fixed by having `compute_turns` read the turn for each zone directly from `self.costs` (and the in-transit turn for a `restricted` zone as `self.costs[next_zone] - 1`) instead of re-deriving it. All ten official maps validate cleanly after the fix — see [Performance](#performance).
- **Directional connection keys.** Occupancy tracking initially keyed connections by the literal `zone1-zone2` order from the file, so `hub-roof1` and `roof1-hub` were treated as two different connections — silently breaking capacity enforcement. Fixed by normalizing the pair (sorted alphabetically) before using it as a dictionary key, both when checking and when recording occupancy.
- **Wrong zone checked for restricted cost.** `compute_turns` initially read the movement cost from the *current* zone in the path instead of the *next* one, so entering a `restricted` zone never actually cost the required 2 turns. Fixed by checking `zone_list[i + 1]`'s type instead of `zone_list[i]`'s.
- **mypy strict typing on composite keys.** `tuple(sorted((a, b)))` is typed by mypy as `tuple[str, ...]` (variable length), which doesn't satisfy a `dict[tuple[str, str], int]`. Resolved by building the normalized pair explicitly (`sorted_zones = sorted((a, b)); pair = (sorted_zones[0], sorted_zones[1])`) instead of relying on `tuple()` around `sorted()`.
- **Optional attributes vs. guaranteed invariants.** `start_hub` / `end_hub` are typed `Zone | None` while the map is being read (they might not exist yet), but are guaranteed non-`None` once parsing succeeds without error. `assert ... is not None` after parsing was used to communicate this invariant to mypy.

## 🏁 Performance

Verified against all ten official benchmark maps (`maps/`), with a script that replays the full output and checks every turn's zone/connection occupancy against the map's own `max_drones` / `max_link_capacity` — every map produces a **capacity-valid** simulation, and every result **beats** its target from the subject (section VII.7):

| Map | Drones | Turns | Target |
|---|---|---|---|
| `easy/01_linear_path` | 2 | **4** | ≤ 6 |
| `easy/02_simple_fork` | 4 | **6** | ≤ 8 |
| `easy/03_basic_capacity` | 4 | **6** | ≤ 6 |
| `medium/01_dead_end_trap` | 5 | **8** | ≤ 12 |
| `medium/02_circular_loop` | 6 | **10** | ≤ 15 |
| `medium/03_priority_puzzle` | 5 | **8** | ≤ 12 |
| `hard/01_maze_nightmare` | 8 | **13** | ≤ 30 |
| `hard/02_capacity_hell` | 12 | **16** | ≤ 35 |
| `hard/03_ultimate_challenge` | 15 | **26** | ≤ 45 |
| `challenger/01_the_impossible_dream` | 25 | **43** | record: 45 |

## 🎁 Bonus

Both bonus criteria from Chapter IX are met by the current implementation, though neither was chased separately — they fell out of getting the mandatory part (and its capacity constraints) actually correct:

- **Exceptional performance.** Every provided map (easy/medium/hard) meets or beats its reference turn target — see the table above.
- **Challenger map.** *The Impossible Dream* (25 drones) is solved in **43 turns**, beating the reference record of 45.

## 📁 Project Structure

| File | Responsibility |
|---|---|
| `map_parser.py` | `Zone`, `Connection`, `Parser` — reads and validates the map file |
| `pathfinder.py` | `Pathfinder` — Dijkstra pathfinding, occupancy tracking, multi-drone scheduling |
| `simulator.py` | `Simulator` — turn-by-turn colored terminal output |
| `run.py` | Entry point wiring everything together |
| `map.txt` | Example map (from the subject) |
| `maps/` | Official easy/medium/hard/challenger benchmark maps |
| `requirements.txt` | Dev dependencies (`flake8`, `mypy`) |
| `Makefile` | `install`, `run`, `debug`, `clean`, `lint` |

## 📚 Resources and AI Usage

**Classic references:**

- [Dijkstra's algorithm — Wikipedia](https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm)
- [Python `heapq` documentation](https://docs.python.org/3/library/heapq.html)
- [Python `typing` documentation](https://docs.python.org/3/library/typing.html)
- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
- [ANSI escape code reference — Wikipedia](https://en.wikipedia.org/wiki/ANSI_escape_code)

**How AI was used:**

Claude (Anthropic) was used throughout as a Socratic pair-programming *navigator*, with Pol as the *driver*, under an explicit pact: Claude asked guiding questions rather than supplying logic or architecture, and let Pol write, run, and debug every line of the parser, the Dijkstra pathfinder, the multi-drone scheduler, and the output formatter himself. When Pol's reasoning was off, Claude asked a question meant to lead him to find the issue rather than stating it directly.

Concretely, Claude helped with:

- **Explaining CS/Python concepts on request** (BFS vs. DFS, Dijkstra's algorithm, priority queues via `heapq`, `set`/`tuple` typing) without supplying the project-specific solution built on top of them
- **Pointing out bugs through questions**, e.g. an inverted neighbor-lookup condition, a misplaced `self.` in an `__init__`, or a variable name mismatch between where a value was created and where it was checked
- **Immediate correction of structural/undefined-behavior issues** when spotted (per the agreed exception for this category), e.g. flagging a `try/except` positioned so it silently swallowed valid rows, or a type annotation that assigned a type object instead of declaring one
- **A full `mypy`/`flake8` cleanup pass**, explaining each reported error and its cause while Pol wrote every fix himself

Three parts were explicitly excluded from the navigator/driver pact and written directly by Claude: **this README**, **docstrings**, and the **colored terminal visualization** in `simulator.py`.
