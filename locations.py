import copy
import random
from collections import deque
from dataclasses import dataclass
from BaseClasses import Location
from .options import LOROptions
from .gamedata.receptions import ReceptionNode, reception_nodes, receptions_dict
from .gamedata.floors import Floor, FloorStage, vanilla_floors, vanilla_floor_stages
from .gamedata.books import BookInfo, books, books_dict


class LORLocation(Location):
    game: str = "Library of Ruina"


@dataclass(frozen=True)
class LORLocationData:
    id: int
    name: str


@dataclass
class ProgressionNode:
    key: str
    name: str
    id: int
    chapter: int
    req_librarians: int
    kind: str
    source: ReceptionNode | FloorStage
    floor: Floor | None = None
    progression_weight: float = 0.0
    order_index: int = 0
    backbone: bool = False
    branch_side: int = 0
    #visual_x: int = 0 #float = 0.0
    #visual_y: int = 0 #float = 0.0

    @property
    def req_books(self) -> list[int]:
        return self.source.req_books


reception_locations: list[LORLocationData] = []
for _, reception in receptions_dict.items():
    for index in range(reception.checks):
        reception_locations.append(LORLocationData(reception.id | (index << 28), f"{reception.name} ({index + 1})"))

abno_locations: list[LORLocationData] = []
for stage in vanilla_floor_stages:
    for index in range(stage.checks):
        abno_locations.append(LORLocationData(stage.id | (index << 28), f"{stage.name} ({index + 1})"))

all_locations = [*reception_locations, *abno_locations]
locations_id_to_name = {location.id: location.name for location in all_locations}
locations_name_to_id = {location.name: location.id for location in all_locations}


class ReceptionTree:
    def __init__(self) -> None:
        self.reception_nodes: list[ReceptionNode] = []
        self.first_reception: int = 0
        self.last_reception: int = 0

    def get_node(self, node_id: int) -> ReceptionNode:
        return {node.id: node for node in self.reception_nodes}[node_id]


@dataclass
class LORSetupResult:
    tree: ReceptionTree
    floors: list[Floor]
    progression_nodes: list[ProgressionNode]
    progression_edges: list[tuple[str, str]]
    abno_stage_chapters: dict[int, int]
    used_book_requirements: set[int]


def _option_enabled(options: LOROptions, option_name: str) -> bool:
    option = getattr(options, option_name)
    return bool(getattr(option, "value", option))


def _option_value(options: LOROptions, option_name: str, default: int) -> int:
    option = getattr(options, option_name, default)
    return int(getattr(option, "value", option))



def _clone_reception_nodes() -> list[ReceptionNode]:
    return copy.deepcopy(reception_nodes)


def _clone_floors() -> list[Floor]:
    return copy.deepcopy(vanilla_floors)


def _reset_req_books(tree: ReceptionTree, floors: list[Floor]) -> None:
    for node in tree.reception_nodes:
        node.req_books.clear()
    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            stage.req_books.clear()


def _stage_to_floor_lookup(floors: list[Floor]) -> dict[int, Floor]:
    lookup: dict[int, Floor] = {}
    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            lookup[stage.id] = floor
    return lookup


def _book_chapter(book: BookInfo) -> int:
    chapter = getattr(book, "chapter", (book.id // 10000) - 19)
    return max(1, min(7, chapter))


def _node_sort_key(rng: random.Random, node: ProgressionNode) -> tuple[float, float, int]:
    return node.progression_weight, rng.random(), node.id


def _assign_progression_weights(rng: random.Random, nodes: list[ProgressionNode]) -> None:
    for node in nodes:
        base = node.chapter * 12.0
        base += min(node.source.checks, 11) * 0.20
        base += max(0, node.req_librarians - 1) * 2.0
        if node.kind == "stage":
            base += 10.0
        if "Realization" in node.name:
            base += 12.0

        noise = rng.gauss(0.0, 8.0)
        node.progression_weight = max(1.0, base + noise)


def _outgoing_count(edges: list[tuple[str, str]], key: str) -> int:
    return sum(1 for source, _ in edges if source == key)


def _max_forward_chapter_jump(source: ProgressionNode) -> int:
    return 1 if source.chapter <= 2 else 2


def _can_connect_chapters(source: ProgressionNode, target: ProgressionNode) -> bool:
    if target.chapter >= source.chapter:
        return target.chapter - source.chapter <= _max_forward_chapter_jump(source)
    return source.chapter - target.chapter <= 1


def _add_edge(edges: list[tuple[str, str]], source: ProgressionNode, target: ProgressionNode) -> bool:
    if source.key == target.key:
        return False
    if not _can_connect_chapters(source, target):
        return False
    edge = (source.key, target.key)
    if edge in edges:
        return True
    if _outgoing_count(edges, source.key) >= max(1, source.source.checks):
        return False
    edges.append(edge)
    return True


def _topological_order(nodes_by_key: dict[str, ProgressionNode], edges: list[tuple[str, str]]) -> list[ProgressionNode]:
    outgoing: dict[str, list[str]] = {key: [] for key in nodes_by_key}
    indegree: dict[str, int] = {key: 0 for key in nodes_by_key}

    for source, target in edges:
        if source not in nodes_by_key or target not in nodes_by_key:
            raise Exception(f"LORAP graph edge references an unknown node: {source} -> {target}")
        outgoing[source].append(target)
        indegree[target] += 1

    queue = sorted([key for key, degree in indegree.items() if degree == 0], key=lambda key: nodes_by_key[key].progression_weight)
    ordered: list[str] = []

    while queue:
        key = queue.pop(0)
        ordered.append(key)
        for child in sorted(outgoing[key], key=lambda child_key: nodes_by_key[child_key].progression_weight):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort(key=lambda queued_key: nodes_by_key[queued_key].progression_weight)

    if len(ordered) != len(nodes_by_key):
        raise Exception("LORAP progression graph contains a cycle")

    return [nodes_by_key[key] for key in ordered]


def _path_exists(
    edges: list[tuple[str, str]],
    start: str,
    target: str,
    ignored_edge: tuple[str, str] | None = None,
) -> bool:
    outgoing: dict[str, list[str]] = {}
    for edge in edges:
        if edge == ignored_edge:
            continue
        outgoing.setdefault(edge[0], []).append(edge[1])

    reached: set[str] = set()
    queue = deque([start])
    while queue:
        key = queue.popleft()
        if key == target:
            return True
        if key in reached:
            continue
        reached.add(key)
        queue.extend(outgoing.get(key, []))
    return False


def _remove_transitive_edges(edges: list[tuple[str, str]], protected_target: str) -> list[tuple[str, str]]:
    reduced = list(edges)
    for edge in list(edges):
        if edge[1] == protected_target:
            continue
        if _path_exists(reduced, edge[0], edge[1], ignored_edge=edge):
            reduced.remove(edge)
    return reduced


def _pick_forward_target(
    rng: random.Random,
    ordered: list[ProgressionNode],
    source_index: int,
    minimum_jump: int,
    maximum_jump: int,
    fallback: ProgressionNode,
) -> ProgressionNode:
    start = min(len(ordered) - 1, source_index + minimum_jump)
    end = min(len(ordered) - 1, source_index + maximum_jump)
    if start > end:
        return fallback
    return ordered[rng.randint(start, end)]



def _pick_starter_node(ordinary: list[ProgressionNode]) -> ProgressionNode:
    candidates = [
        node for node in ordinary
        if node.kind == "reception" and node.chapter <= 2 and node.req_librarians <= 1
    ]
    if not candidates:
        candidates = [node for node in ordinary if node.kind == "reception" and node.req_librarians <= 1]
    if not candidates:
        candidates = ordinary
    return min(candidates, key=lambda node: (node.progression_weight, node.chapter, node.id))


def _valid_source_candidates(
    edges: list[tuple[str, str]],
    connected: list[ProgressionNode],
    target: ProgressionNode,
) -> list[ProgressionNode]:
    return [
        source for source in connected
        if source.progression_weight < target.progression_weight
        and _can_connect_chapters(source, target)
        and _outgoing_count(edges, source.key) < max(1, source.source.checks)
    ]


def _choose_edge_source(
    rng: random.Random,
    edges: list[tuple[str, str]],
    connected: list[ProgressionNode],
    target: ProgressionNode,
) -> ProgressionNode | None:
    candidates = _valid_source_candidates(edges, connected, target)
    if not candidates:
        return None

    candidates.sort(key=lambda node: (
        abs(node.progression_weight - target.progression_weight),
        abs(node.chapter - target.chapter),
        node.id,
    ))
    return rng.choice(candidates[:min(6, len(candidates))])


def _build_branchy_edges(rng: random.Random, first: ProgressionNode, ordinary: list[ProgressionNode], last: ProgressionNode) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    if not ordinary:
        if not _add_edge(edges, first, last):
            raise Exception(f"LORAP could not create edge {first.key} -> {last.key}")
        return edges

    starter = _pick_starter_node(ordinary)
    remaining = [node for node in ordinary if node is not starter]
    if not _add_edge(edges, first, starter):
        raise Exception(f"LORAP could not create starter edge {first.key} -> {starter.key}")

    lanes_count = min(rng.randint(3, 5), max(2, starter.source.checks))
    for index, node in enumerate(sorted(remaining, key=lambda node: node.progression_weight)):
        lane_index = min(lanes_count - 1, int(index * lanes_count / max(1, len(remaining))))
        lane_index = max(0, min(lanes_count - 1, lane_index + rng.choice([-1, 0, 0, 1])))
        node.branch_side = lane_index - (lanes_count // 2)

    connected: list[ProgressionNode] = [starter]
    pending = sorted(remaining, key=lambda node: (node.progression_weight, node.chapter, node.id))

    while pending:
        connectable = [node for node in pending if _valid_source_candidates(edges, connected, node)]
        if not connectable:
            sample = ", ".join(f"{node.key}:ch{node.chapter}" for node in pending[:8])
            raise Exception(f"LORAP could not connect pending nodes within chapter jump limits: {sample}")

        connectable.sort(key=lambda node: (node.progression_weight, rng.random(), node.id))
        target = rng.choice(connectable[:min(4, len(connectable))])
        source = _choose_edge_source(rng, edges, connected, target)
        if source is None or not _add_edge(edges, source, target):
            raise Exception(f"LORAP could not create branchy edge into {target.key}")

        connected.append(target)
        pending.remove(target)

    last_sources = _valid_source_candidates(edges, connected, last)
    if not last_sources:
        raise Exception("LORAP could not connect Oliver within chapter jump limits")

    last_sources.sort(key=lambda node: (abs(node.chapter - last.chapter), abs(node.progression_weight - last.progression_weight), node.id))
    if not _add_edge(edges, last_sources[0], last):
        raise Exception(f"LORAP could not create final edge {last_sources[0].key} -> {last.key}")

    ordered = sorted(connected[1:], key=lambda node: node.progression_weight)
    for index, source in enumerate(ordered):
        if rng.random() > 0.20:
            continue
        if _outgoing_count(edges, source.key) >= max(1, source.source.checks):
            continue

        possible_targets = [
            target for target in ordered[index + 2:] + [last]
            if target.progression_weight > source.progression_weight
            and _can_connect_chapters(source, target)
        ]
        if not possible_targets:
            continue

        possible_targets.sort(key=lambda node: (
            abs(node.progression_weight - source.progression_weight),
            abs(node.chapter - source.chapter),
            node.id,
        ))
        _add_edge(edges, source, rng.choice(possible_targets[:min(10, len(possible_targets))]))

    return edges

#def _assign_visual_layout(
#    rng: random.Random,
#    ordered: list[ProgressionNode],
#    edges: list[tuple[str, str]],
#    first: ProgressionNode,
#    last: ProgressionNode,
#    branchy: bool,
#) -> None:
#    for index, node in enumerate(ordered):
#        node.order_index = index
#
#    ordinary = [node for node in ordered if node.key not in {first.key, last.key}]
#    ordinary.sort(key=lambda node: (node.order_index, node.progression_weight, node.id))
#
#    # Compact grid. Do not push rows down to satisfy every visual edge: branchy
#    # DAGs contain many cross-links, and row-pushing can expand the map into an
#    # unusably tall column. The graph still controls AP logic; this is only a
#    # readable clickable projection of that graph.
#    columns = 7 if branchy else 6
#    x_spacing = 330.0 if branchy else 350.0
#    y_spacing = 220.0 if branchy else 240.0
#    max_abs_x = 1320.0
#
#    first.visual_x = 0.0
#    first.visual_y = 0.0
#
#    rows: list[list[ProgressionNode]] = []
#    for index in range(0, len(ordinary), columns):
#        rows.append(ordinary[index:index + columns])
#
#    for row_index, row in enumerate(rows, start=1):
#        row_size = len(row)
#        for col_index, node in enumerate(row):
#            centered_col = col_index - (row_size - 1) / 2.0
#            node.visual_x = centered_col * x_spacing
#            node.visual_y = row_index * y_spacing
#            node.visual_x = max(-max_abs_x, min(max_abs_x, node.visual_x))
#
#    last.visual_x = 0.0
#    last.visual_y = (len(rows) + 1) * y_spacing
#
#    for node in ordered:
#        node.visual_x = round(node.visual_x, 2)
#        node.visual_y = round(node.visual_y, 2)



def _make_progression_nodes(tree: ReceptionTree, floors: list[Floor]) -> tuple[ProgressionNode, list[ProgressionNode], ProgressionNode]:
    stage_floors = _stage_to_floor_lookup(floors)
    nodes_by_key: dict[str, ProgressionNode] = {}

    def add_reception(reception: ReceptionNode) -> ProgressionNode:
        key = f"reception:{reception.id}"
        if key not in nodes_by_key:
            nodes_by_key[key] = ProgressionNode(key, reception.name, reception.id, reception.chapter, reception.req_librarians, "reception", reception)
        return nodes_by_key[key]

    def add_stage(stage: FloorStage) -> ProgressionNode:
        key = f"stage:{stage.id}"
        if key not in nodes_by_key:
            nodes_by_key[key] = ProgressionNode(key, stage.name, stage.id, max(1, min(7, stage.chapter)), stage.req_librarians, "stage", stage, stage_floors[stage.id])
        return nodes_by_key[key]

    first = add_reception(tree.get_node(tree.first_reception))
    last = add_reception(tree.get_node(tree.last_reception))

    for reception in tree.reception_nodes:
        if reception.id not in (tree.first_reception, tree.last_reception):
            add_reception(reception)

    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            add_stage(stage)

    ordinary = [node for node in nodes_by_key.values() if node.key not in {first.key, last.key}]
    return first, ordinary, last


def build_mixed_battle_graph(
    rng: random.Random,
    tree: ReceptionTree,
    floors: list[Floor],
) -> tuple[list[ProgressionNode], list[tuple[str, str]], dict[int, int]]:
    first, ordinary, last = _make_progression_nodes(tree, floors)
    _assign_progression_weights(rng, ordinary)
    first.progression_weight = -1000.0
    last.progression_weight = 1000.0
    ordinary.sort(key=lambda node: _node_sort_key(rng, node))

    edges = _build_branchy_edges(rng, first, ordinary, last)
    edges = _remove_transitive_edges(edges, last.key)

    nodes_by_key = {node.key: node for node in [first, *ordinary, last]}
    ordered = _topological_order(nodes_by_key, edges)
    # _assign_visual_layout(rng, ordered, edges, first, last, branchy=True)
    stage_chapters = {node.id: node.chapter for node in ordered if node.kind == "stage"}
    return ordered, edges, stage_chapters


def assign_archipelago_book_requirements(
    rng: random.Random,
    progression_nodes: list[ProgressionNode],
    progression_edges: list[tuple[str, str]],
    options: LOROptions,
) -> set[int]:
    require_receptions = _option_enabled(options, "receptions_require_books")
    require_floors = _option_enabled(options, "floors_require_books")
    balance_books = _option_enabled(options, "balance_book_requirements") if hasattr(options, "balance_book_requirements") else True
    density = max(1, min(100, _option_value(options, "book_requirement_density", 100)))

    used_books: set[int] = set()
    max_index = max(1, len(progression_nodes) - 1)
    bootstrap_count = 2
    bootstrap_keys = {node.key for node in progression_nodes[:bootstrap_count]}

    def accepts_books(node: ProgressionNode) -> bool:
        return (node.kind == "reception" and require_receptions) or (node.kind == "stage" and require_floors)

    def progress(node: ProgressionNode) -> float:
        return max(0.0, min(1.0, node.order_index / max_index))

    def desired_count(node: ProgressionNode) -> int:
        if not accepts_books(node) or node.key in bootstrap_keys:
            return 0

        p = progress(node)
        if p < 0.55:
            return 1
        if p < 0.82:
            return 2 if rng.random() < 0.20 else 1
        return 2 if rng.random() < 0.55 else 1

    def candidate_books(node: ProgressionNode, selected: set[int]) -> list[BookInfo]:
        if not balance_books:
            return [book for book in books if book.id not in selected]

        p = progress(node)
        target_chapter = max(1, min(7, round(1 + p * 6)))
        drift = 1 if p < 0.70 else 2
        if rng.random() < 0.25:
            drift += 1
        candidates = [
            book for book in books
            if book.id not in selected and abs(_book_chapter(book) - target_chapter) <= drift
        ]
        return candidates or [book for book in books if book.id not in selected]

    lockable_nodes = [
        node for node in progression_nodes
        if accepts_books(node) and node.key not in bootstrap_keys
    ]
    if not lockable_nodes:
        return used_books

    neighbors: dict[str, set[str]] = {node.key: set() for node in progression_nodes}
    for source, target in progression_edges:
        neighbors[source].add(target)
        neighbors[target].add(source)

    cluster_count = 1 + round((len(lockable_nodes) - 1) * (density - 1) / 99)
    if cluster_count == 1:
        seeds = [lockable_nodes[len(lockable_nodes) // 2]]
    else:
        seed_indices = [
            round(index * (len(lockable_nodes) - 1) / (cluster_count - 1))
            for index in range(cluster_count)
        ]
        seeds = [lockable_nodes[index] for index in seed_indices]

    node_order = {node.key: index for index, node in enumerate(progression_nodes)}
    owner: dict[str, str] = {seed.key: seed.key for seed in seeds}
    queue = deque(seed.key for seed in seeds)
    while queue:
        key = queue.popleft()
        for neighbor in sorted(neighbors[key], key=lambda neighbor_key: node_order[neighbor_key]):
            if neighbor in owner:
                continue
            owner[neighbor] = owner[key]
            queue.append(neighbor)

    clusters: dict[str, list[ProgressionNode]] = {seed.key: [] for seed in seeds}
    for node in lockable_nodes:
        clusters[owner[node.key]].append(node)

    cluster_specs: list[tuple[list[ProgressionNode], ProgressionNode, int]] = []
    for seed in sorted(seeds, key=lambda node: node_order[node.key]):
        cluster = clusters[seed.key]
        representative = min(cluster, key=lambda node: node_order[node.key])
        cluster_specs.append((cluster, representative, desired_count(representative)))

    for cluster, representative, count in cluster_specs:
        selected: set[int] = set()
        while len(selected) < count:
            balanced_pool = candidate_books(representative, selected)
            fresh_pool = [book for book in balanced_pool if book.id not in used_books]
            if not fresh_pool:
                fresh_pool = [book for book in books if book.id not in selected and book.id not in used_books]
            pool = fresh_pool or balanced_pool
            if not pool:
                break
            selected.add(rng.choice(pool).id)

        requirement = sorted(selected)
        used_books.update(selected)
        for node in cluster:
            node.req_books[:] = requirement

    return used_books


def validate_setup_result(result: LORSetupResult) -> None:
    nodes_by_key = {node.key: node for node in result.progression_nodes}
    outgoing: dict[str, list[str]] = {key: [] for key in nodes_by_key}
    indegree: dict[str, int] = {key: 0 for key in nodes_by_key}

    for source, target in result.progression_edges:
        if source == target:
            raise Exception(f"LORAP graph has a self-cycle on {source}")
        if source not in nodes_by_key or target not in nodes_by_key:
            raise Exception(f"LORAP graph edge references an unknown node: {source} -> {target}")
        if nodes_by_key[target].progression_weight <= nodes_by_key[source].progression_weight and target != f"reception:{result.tree.last_reception}":
            raise Exception(f"LORAP graph has a backwards edge: {source} -> {target}")
        if not _can_connect_chapters(nodes_by_key[source], nodes_by_key[target]):
            raise Exception(f"LORAP graph has an invalid chapter jump: {source} -> {target}")
        outgoing[source].append(target)
        indegree[target] += 1

    first_key = f"reception:{result.tree.first_reception}"
    last_key = f"reception:{result.tree.last_reception}"
    roots = [key for key, degree in indegree.items() if degree == 0]
    if roots != [first_key]:
        raise Exception(f"LORAP graph must start only from Rats, got roots: {roots}")

    first_children = outgoing[first_key]
    if len(first_children) != 1:
        raise Exception(f"LORAP Rats must have exactly one child, got {len(first_children)}: {first_children}")

    reached: set[str] = set()
    queue = deque([first_key])
    while queue:
        key = queue.popleft()
        if key in reached:
            continue
        reached.add(key)
        queue.extend(outgoing[key])

    if len(reached) != len(nodes_by_key):
        missing = sorted(set(nodes_by_key) - reached)
        raise Exception(f"LORAP graph has unreachable nodes: {missing[:8]}")
    if last_key not in reached:
        raise Exception("LORAP Oliver is unreachable")

    for edge in result.progression_edges:
        if edge[1] == last_key:
            continue
        if _path_exists(result.progression_edges, edge[0], edge[1], ignored_edge=edge):
            raise Exception(f"LORAP graph has a transitive edge: {edge[0]} -> {edge[1]}")

    for node in result.progression_nodes:
        if node.kind == "stage" and node.floor is None:
            raise Exception(f"LORAP stage node has no assigned floor: {node.key}")
        for book_id in node.req_books:
            if book_id not in books_dict:
                raise Exception(f"LORAP node {node.key} requires unknown book {book_id}")
            if book_id not in result.used_book_requirements:
                raise Exception(f"LORAP node {node.key} requires non-progression book {book_id}")


def _shuffle_floor_content(rng: random.Random, floors: list[Floor], options: LOROptions) -> None:
    if options.shuffle_abnos:
        abnos_per_chapter: list[list[FloorStage]] = [[] for _ in range(7)]
        for floor in floors:
            for stage in floor.abno_stages:
                abnos_per_chapter[max(0, min(6, stage.chapter - 1))].append(stage)
            floor.abno_stages = [None] * len(floor.abno_stages)

        all_abnos: list[FloorStage] = []
        for chapter_list in abnos_per_chapter:
            rng.shuffle(chapter_list)
            all_abnos.extend(chapter_list)

        while all_abnos:
            candidates = [floor for floor in floors if None in floor.abno_stages]
            floor = rng.choice(candidates)
            floor.abno_stages[floor.abno_stages.index(None)] = all_abnos.pop(0)

    if options.shuffle_realizations:
        realizations = [floor.realization_stage for floor in floors]
        rng.shuffle(realizations)
        for floor in floors:
            floor.realization_stage = realizations.pop(0)


def setup_locations(rng: random.Random, options: LOROptions) -> LORSetupResult:
    last_error: Exception | None = None

    for _ in range(150):
        try:
            tree = ReceptionTree()
            tree.reception_nodes = _clone_reception_nodes()
            tree.first_reception = tree.reception_nodes[0].id
            tree.last_reception = tree.reception_nodes[-1].id

            floors = _clone_floors()
            _reset_req_books(tree, floors)
            _shuffle_floor_content(rng, floors, options)

            progression_nodes, progression_edges, abno_stage_chapters = build_mixed_battle_graph(rng, tree, floors)
            used_book_requirements = assign_archipelago_book_requirements(rng, progression_nodes, progression_edges, options)

            result = LORSetupResult(
                tree=tree,
                floors=floors,
                progression_nodes=progression_nodes,
                progression_edges=progression_edges,
                abno_stage_chapters=abno_stage_chapters,
                used_book_requirements=used_book_requirements,
            )
            validate_setup_result(result)

            return result
        except Exception as error:
            #if error.__traceback__:
            #    print(f"Expection: {error}; At: {error.__traceback__.tb_lineno}")
            last_error = error

    raise Exception(f"LORAP failed to generate a valid progression graph: {last_error};")
