import copy
import random
from collections import deque
from dataclasses import dataclass
from BaseClasses import Location
from .options import LOROptions
from .gamedata.receptions import ReceptionNode, reception_nodes, endgoal_receptions, receptions_dict
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
    sphere: int = 0
    sphere_layer: int = 0
    global_layer: int = 0
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
    transition_edges: set[tuple[str, str]]
    shortcut_connections: bool
    boe_layers_mode: bool
    abno_stage_chapters: dict[int, int]
    used_book_requirements: set[int]
    layer_count: int
    selected_goal_nodes: list[ProgressionNode]


def _option_enabled(options: LOROptions, option_name: str) -> bool:
    option = getattr(options, option_name)
    return bool(getattr(option, "value", option))


def _option_value(options: LOROptions, option_name: str, default: int) -> int:
    option = getattr(options, option_name, default)
    return int(getattr(option, "value", option))



def _clone_reception_nodes() -> list[ReceptionNode]:
    return copy.deepcopy(reception_nodes)


def _goal_receptions(goal_names: set[str]) -> list[ReceptionNode]:
    selected_nodes: list[ReceptionNode] = []

    for node in endgoal_receptions:
        if 70001 <= node.id <= 70010:
            if "Reverberation Ensemble" in goal_names:
                selected_nodes.append(node)
            continue

        if node.id == 60003 and "Black Silence" in goal_names:
            selected_nodes.append(node)
            continue

        if node.id == 60004 and "Distorted Ensemble" in goal_names:
            selected_nodes.append(node)

    return selected_nodes


def get_selected_endgoal_receptions(options: LOROptions) -> list[ReceptionNode]:
    return _goal_receptions(set(options.endgoals.value))


def _clone_persistent_goal_receptions(options: LOROptions) -> list[ReceptionNode]:
    persistent_only = set(options.persistent_goals.value) - set(options.endgoals.value)
    return copy.deepcopy(_goal_receptions(persistent_only))


def _include_keter_realization(options: LOROptions) -> bool:
    return (
        "Keter Realization" in set(options.persistent_goals.value)
        and "Keter Realization" not in set(options.endgoals.value)
    )


def _make_selected_goal_nodes(options: LOROptions, floors: list[Floor]) -> list[ProgressionNode]:
    selected_nodes = [
        ProgressionNode(
            key=f"endgoal:{reception.id}",
            name=reception.name,
            id=reception.id,
            chapter=reception.chapter,
            req_librarians=reception.req_librarians,
            kind="reception",
            source=reception,
        )
        for reception in copy.deepcopy(get_selected_endgoal_receptions(options))
    ]

    if "Keter Realization" in set(options.endgoals.value):
        stage_floors = _stage_to_floor_lookup(floors)
        keter_stage = next(
            stage for floor in floors for stage in [*floor.abno_stages, floor.realization_stage]
            if stage.id == 210009
        )
        selected_nodes.append(ProgressionNode(
            key="endgoal:210009",
            name=keter_stage.name,
            id=keter_stage.id,
            chapter=max(1, min(7, keter_stage.chapter)),
            req_librarians=keter_stage.req_librarians,
            kind="stage",
            source=keter_stage,
            floor=stage_floors[keter_stage.id],
        ))

    return selected_nodes


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


def _add_edge(edges: list[tuple[str, str]], source: ProgressionNode, target: ProgressionNode) -> bool:
    if source.key == target.key:
        return False
    edge = (source.key, target.key)
    if edge in edges:
        return True
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


def _remove_transitive_edges(edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
    reduced = list(edges)
    for edge in list(edges):
        if _path_exists(reduced, edge[0], edge[1], ignored_edge=edge):
            reduced.remove(edge)
    return reduced


def _assign_spheres(rng: random.Random, ordinary: list[ProgressionNode]) -> None:
    for node in ordinary:
        candidates = [sphere for sphere in (node.chapter - 1, node.chapter, node.chapter + 1) if 1 <= sphere <= 7]
        weights = [80 if sphere == node.chapter else 10 for sphere in candidates]
        node.sphere = rng.choices(candidates, weights=weights, k=1)[0]

    sphere_counts = {
        sphere: sum(node.sphere == sphere for node in ordinary)
        for sphere in range(1, 8)
    }
    for sphere in range(1, 8):
        while sphere_counts[sphere] < 2:
            candidates = [
                node for node in ordinary
                if node.sphere != sphere
                and sphere_counts[node.sphere] > 2
                and abs(node.chapter - sphere) <= 1
            ]
            if not candidates:
                raise Exception(f"LORAP could not populate sphere {sphere}")
            moved = min(candidates, key=lambda node: (abs(node.chapter - sphere), node.progression_weight))
            sphere_counts[moved.sphere] -= 1
            moved.sphere = sphere
            sphere_counts[sphere] += 1


def _sphere_width_profile(sphere: int, rng: random.Random) -> tuple[int, int, int]:
    target_widths = {
        1: rng.randint(3, 4),
        2: rng.randint(4, 5),
        3: rng.randint(5, 6),
        4: rng.randint(6, 7),
        5: rng.randint(7, 8),
        6: rng.randint(7, 8),
        7: rng.randint(3, 4),
    }
    edge_caps = {
        1: 3,
        2: 4,
        3: 5,
        4: 5,
        5: 6,
        6: 6,
        7: 3,
    }
    middle_caps = {
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 8,
        6: 8,
        7: 5,
    }
    return target_widths[sphere], edge_caps[sphere], middle_caps[sphere]


def _layer_widths(rng: random.Random, sphere: int, node_count: int) -> list[int]:
    if node_count < 2:
        raise Exception("LORAP sphere does not have enough nodes for a layered graph")

    target_width, edge_cap, middle_cap = _sphere_width_profile(sphere, rng)
    layer_count = (node_count + target_width - 1) // target_width
    layer_count = max(1, min(layer_count, node_count // 2))
    while edge_cap * min(layer_count, 2) + middle_cap * max(0, layer_count - 2) < node_count:
        layer_count += 1
    if layer_count > node_count // 2:
        raise Exception(f"LORAP could not split {node_count} nodes into non-singleton layers")

    widths = [2] * layer_count
    remaining = node_count - sum(widths)
    center_order = sorted(range(layer_count), key=lambda index: (abs(index - (layer_count - 1) / 2), rng.random()))

    while remaining:
        candidates = [
            index for index in center_order
            if widths[index] < (edge_cap if index in (0, layer_count - 1) else middle_cap)
        ]
        if not candidates:
            raise Exception(f"LORAP could not fit {node_count} nodes into sphere layers")
        for index in candidates:
            if remaining == 0:
                break
            widths[index] += 1
            remaining -= 1
    return widths


def _make_sphere_layers(
    rng: random.Random,
    first: ProgressionNode,
    ordinary: list[ProgressionNode],
    last: ProgressionNode,
    boe_layers_mode: bool,
) -> list[list[list[ProgressionNode]]]:
    spheres: list[list[list[ProgressionNode]]] = []
    global_layer = 0
    for sphere in range(1, 8):
        nodes = [node for node in ordinary if node.sphere == sphere]
        if boe_layers_mode:
            rng.shuffle(nodes)
        else:
            nodes.sort(key=lambda node: _node_sort_key(rng, node))

        fixed_start = [first] if sphere == 1 else []
        fixed_end = [last] if sphere == 7 else []
        widths = _layer_widths(rng, sphere, len(nodes))
        if boe_layers_mode and sphere == 1:
            bootstrap_width = widths[0]
            bootstrap_candidates = [
                node for node in nodes
                if node.kind == "reception" and node.req_librarians <= 1
            ]
            if len(bootstrap_candidates) < bootstrap_width:
                raise Exception("LORAP could not build a reception-only bootstrap layer")
            bootstrap = bootstrap_candidates[:bootstrap_width]
            bootstrap_keys = {node.key for node in bootstrap}
            nodes = [*bootstrap, *(node for node in nodes if node.key not in bootstrap_keys)]
        layers: list[list[ProgressionNode]] = []
        if fixed_start:
            layers.append(fixed_start)
        offset = 0
        for width in widths:
            layer = nodes[offset:offset + width]
            rng.shuffle(layer)
            layers.append(layer)
            offset += width
        if fixed_end:
            layers.append(fixed_end)

        for layer_index, layer in enumerate(layers):
            for node in layer:
                node.sphere = sphere
                node.sphere_layer = layer_index
                logical_layer_index = layer_index
                if boe_layers_mode and sphere == 1 and layer_index > 0:
                    logical_layer_index -= 1
                node.global_layer = global_layer + logical_layer_index
                node.progression_weight = sphere * 1000.0 + layer_index * 10.0 + rng.random()
        spheres.append(layers)
        global_layer += len(layers) - (1 if boe_layers_mode and sphere == 1 else 0)
    return spheres


def _connect_adjacent_layers(
    rng: random.Random,
    edges: list[tuple[str, str]],
    sources: list[ProgressionNode],
    targets: list[ProgressionNode],
) -> None:
    shuffled_sources = list(sources)
    shuffled_targets = list(targets)
    rng.shuffle(shuffled_sources)
    rng.shuffle(shuffled_targets)

    for index, target in enumerate(shuffled_targets):
        _add_edge(edges, shuffled_sources[index % len(shuffled_sources)], target)
    for index, source in enumerate(shuffled_sources):
        if _outgoing_count(edges, source.key) == 0:
            _add_edge(edges, source, shuffled_targets[index % len(shuffled_targets)])

    for source in shuffled_sources:
        if rng.random() < 0.35:
            _add_edge(edges, source, rng.choice(shuffled_targets))


def _build_layered_edges(
    rng: random.Random,
    spheres: list[list[list[ProgressionNode]]],
    shortcut_connections: bool,
) -> tuple[list[tuple[str, str]], set[tuple[str, str]]]:
    edges: list[tuple[str, str]] = []
    transition_edges: set[tuple[str, str]] = set()

    for layers in spheres:
        for layer_index in range(len(layers) - 1):
            _connect_adjacent_layers(rng, edges, layers[layer_index], layers[layer_index + 1])

    for sphere_index in range(6):
        before = len(edges)
        _connect_adjacent_layers(rng, edges, spheres[sphere_index][-1], spheres[sphere_index + 1][0])
        transition_edges.update(edges[before:])

    if shortcut_connections:
        for layers in spheres:
            for layer_index, layer in enumerate(layers[:-2]):
                if rng.random() > 0.65:
                    continue
                jump = rng.choice([2, 2, 3])
                if layer_index + jump >= len(layers):
                    continue
                source = rng.choice(layer)
                candidates = [
                    target for target in layers[layer_index + jump]
                    if not _path_exists(edges, source.key, target.key)
                ]
                if candidates:
                    _add_edge(edges, source, rng.choice(candidates))

    return _remove_transitive_edges(edges), transition_edges

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



def _make_progression_nodes(
    tree: ReceptionTree,
    floors: list[Floor],
    include_keter_realization: bool,
) -> tuple[ProgressionNode, list[ProgressionNode], ProgressionNode]:
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
            if stage.id == 210009 and not include_keter_realization:
                continue
            add_stage(stage)

    ordinary = [node for node in nodes_by_key.values() if node.key not in {first.key, last.key}]
    return first, ordinary, last


def build_mixed_battle_graph(
    rng: random.Random,
    tree: ReceptionTree,
    floors: list[Floor],
    shortcut_connections: bool,
    boe_layers_mode: bool,
    include_keter_realization: bool,
) -> tuple[list[ProgressionNode], list[tuple[str, str]], set[tuple[str, str]], dict[int, int]]:
    first, ordinary, last = _make_progression_nodes(tree, floors, include_keter_realization)
    _assign_progression_weights(rng, ordinary)
    _assign_spheres(rng, ordinary)
    first.sphere = 1
    last.sphere = 7
    spheres = _make_sphere_layers(rng, first, ordinary, last, boe_layers_mode)
    edges, transition_edges = _build_layered_edges(rng, spheres, shortcut_connections)

    nodes_by_key = {node.key: node for node in [first, *ordinary, last]}
    ordered = _topological_order(nodes_by_key, edges)
    # _assign_visual_layout(rng, ordered, edges, first, last, branchy=True)
    stage_chapters = {node.id: node.chapter for node in ordered if node.kind == "stage"}
    return ordered, edges, transition_edges, stage_chapters


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
    bootstrap_count = 4
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

    layers_by_sphere: dict[int, dict[int, list[ProgressionNode]]] = {
        sphere: {} for sphere in range(1, 8)
    }
    for node in result.progression_nodes:
        if node.sphere not in layers_by_sphere:
            raise Exception(f"LORAP node has an invalid sphere: {node.key} -> {node.sphere}")
        if abs(node.chapter - node.sphere) > 1:
            raise Exception(f"LORAP node is too far from its vanilla chapter: {node.key}")
        layers_by_sphere[node.sphere].setdefault(node.sphere_layer, []).append(node)

    for sphere, layers in layers_by_sphere.items():
        if not layers:
            raise Exception(f"LORAP sphere {sphere} is empty")
        expected_layers = set(range(max(layers) + 1))
        if set(layers) != expected_layers:
            raise Exception(f"LORAP sphere {sphere} has a gap in its layers")
        for layer_index, layer in layers.items():
            is_rats_layer = sphere == 1 and layer_index == 0
            is_oliver_layer = sphere == 7 and layer_index == max(layers)
            if len(layer) < 2 and not (is_rats_layer or is_oliver_layer):
                raise Exception(f"LORAP sphere {sphere} has a singleton layer {layer_index}")

    global_layers = {node.global_layer for node in result.progression_nodes}
    if global_layers != set(range(result.layer_count)):
        raise Exception("LORAP global layers are not contiguous")

    expected_global_layer = 0
    for sphere in range(1, 8):
        for sphere_layer in sorted(layers_by_sphere[sphere]):
            layer = layers_by_sphere[sphere][sphere_layer]
            is_boe_bootstrap = result.boe_layers_mode and sphere == 1 and sphere_layer == 1
            layer_global = 0 if is_boe_bootstrap else expected_global_layer
            if {node.global_layer for node in layer} != {layer_global}:
                raise Exception(f"LORAP sphere {sphere} layer {sphere_layer} has an invalid global layer")
            if not is_boe_bootstrap:
                expected_global_layer += 1

    if result.boe_layers_mode:
        bootstrap = layers_by_sphere[1].get(1, [])
        if len(bootstrap) < 2:
            raise Exception("LORAP BoE bootstrap layer has fewer than two receptions")
        if any(node.kind != "reception" or node.req_librarians > 1 for node in bootstrap):
            raise Exception("LORAP BoE bootstrap layer contains a gated battle")

    for source, target in result.progression_edges:
        if source == target:
            raise Exception(f"LORAP graph has a self-cycle on {source}")
        if source not in nodes_by_key or target not in nodes_by_key:
            raise Exception(f"LORAP graph edge references an unknown node: {source} -> {target}")
        source_node = nodes_by_key[source]
        target_node = nodes_by_key[target]
        if target_node.progression_weight <= source_node.progression_weight:
            raise Exception(f"LORAP graph has a backwards edge: {source} -> {target}")
        if target_node.sphere == source_node.sphere:
            layer_jump = target_node.sphere_layer - source_node.sphere_layer
            if layer_jump < 1 or layer_jump > 3 or (not result.shortcut_connections and layer_jump != 1):
                raise Exception(f"LORAP graph has an invalid layer edge: {source} -> {target}")
            if (source, target) in result.transition_edges:
                raise Exception(f"LORAP internal edge is marked as a transition: {source} -> {target}")
        else:
            if target_node.sphere != source_node.sphere + 1:
                raise Exception(f"LORAP graph skips a sphere: {source} -> {target}")
            source_last_layer = max(layers_by_sphere[source_node.sphere])
            if source_node.sphere_layer != source_last_layer or target_node.sphere_layer != 0:
                raise Exception(f"LORAP transition does not connect sphere boundaries: {source} -> {target}")
            if (source, target) not in result.transition_edges:
                raise Exception(f"LORAP sphere edge is not marked as a transition: {source} -> {target}")
        outgoing[source].append(target)
        indegree[target] += 1

    first_key = f"reception:{result.tree.first_reception}"
    last_key = f"reception:{result.tree.last_reception}"
    roots = [key for key, degree in indegree.items() if degree == 0]
    if roots != [first_key]:
        raise Exception(f"LORAP graph must start only from Rats, got roots: {roots}")

    if nodes_by_key[first_key].sphere != 1 or nodes_by_key[first_key].sphere_layer != 0:
        raise Exception("LORAP Rats must start sphere 1")
    last_sphere_layer = max(layers_by_sphere[7])
    if nodes_by_key[last_key].sphere != 7 or nodes_by_key[last_key].sphere_layer != last_sphere_layer:
        raise Exception("LORAP Oliver must end sphere 7")

    unknown_transitions = result.transition_edges - set(result.progression_edges)
    if unknown_transitions:
        raise Exception(f"LORAP transition metadata references missing edges: {sorted(unknown_transitions)[:4]}")

    for sphere in range(1, 7):
        transitions = [
            edge for edge in result.transition_edges
            if nodes_by_key[edge[0]].sphere == sphere and nodes_by_key[edge[1]].sphere == sphere + 1
        ]
        if len(transitions) < 2:
            raise Exception(f"LORAP sphere {sphere} has fewer than two exits")

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

    dead_ends = [key for key, targets in outgoing.items() if not targets and key != last_key]
    if dead_ends:
        raise Exception(f"LORAP graph has dead ends before Oliver: {dead_ends[:8]}")

    for edge in result.progression_edges:
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
            regular_receptions = _clone_reception_nodes()
            tree.first_reception = regular_receptions[0].id
            tree.last_reception = regular_receptions[-1].id
            tree.reception_nodes = [*regular_receptions, *_clone_persistent_goal_receptions(options)]

            floors = _clone_floors()
            _reset_req_books(tree, floors)
            _shuffle_floor_content(rng, floors, options)
            selected_goal_nodes = _make_selected_goal_nodes(options, floors)

            progression_nodes, progression_edges, transition_edges, abno_stage_chapters = build_mixed_battle_graph(
                rng,
                tree,
                floors,
                _option_enabled(options, "shortcut_connections"),
                _option_value(options, "progression_mode", 0) == 1,
                _include_keter_realization(options),
            )
            boe_layers_mode = _option_value(options, "progression_mode", 0) == 1
            used_book_requirements = (
                set()
                if boe_layers_mode
                else assign_archipelago_book_requirements(rng, progression_nodes, progression_edges, options)
            )
            layer_count = max(node.global_layer for node in progression_nodes) + 1
            for goal_node in selected_goal_nodes:
                goal_node.sphere = 8
                goal_node.global_layer = layer_count - 1
                if goal_node.kind == "stage":
                    abno_stage_chapters[goal_node.id] = goal_node.chapter

            result = LORSetupResult(
                tree=tree,
                floors=floors,
                progression_nodes=progression_nodes,
                progression_edges=progression_edges,
                transition_edges=transition_edges,
                shortcut_connections=_option_enabled(options, "shortcut_connections"),
                boe_layers_mode=boe_layers_mode,
                abno_stage_chapters=abno_stage_chapters,
                used_book_requirements=used_book_requirements,
                layer_count=layer_count,
                selected_goal_nodes=selected_goal_nodes,
            )
            validate_setup_result(result)

            return result
        except Exception as error:
            #if error.__traceback__:
            #    print(f"Expection: {error}; At: {error.__traceback__.tb_lineno}")
            last_error = error

    raise Exception(f"LORAP failed to generate a valid progression graph: {last_error};")
