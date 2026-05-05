import copy
import random
from dataclasses import dataclass
from BaseClasses import Location, ItemClassification
from .options import LOROptions
from .gamedata.receptions import ReceptionNode, reception_nodes, receptions_dict
from .gamedata.floors import Floor, FloorStage, vanilla_floors, vanilla_floor_stages
from .gamedata.books import BookInfo, books, books_dict
from .items import items_by_name


class LORLocation(Location):
    game: str = "Library of Ruina"


@dataclass
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
    visual_x: float = 0.0
    visual_y: float = 0.0

    @property
    def req_books(self) -> list[int]:
        return self.source.req_books


reception_locations: list[LORLocationData] = []
for _, r in receptions_dict.items():
    for j in range(r.checks):
        reception_locations.append(LORLocationData(r.id | (j << 28), r.name + " (" + str(j + 1) + ")"))

abno_locations: list[LORLocationData] = []
for s in vanilla_floor_stages:
    for i in range(s.checks):
        abno_locations.append(LORLocationData(s.id | (i << 28), s.name + " (" + str(i + 1) + ")"))

all_locations = [*reception_locations, *abno_locations]
locations_id_to_name = {location.id: location.name for location in all_locations}
locations_name_to_id = {location.name: location.id for location in all_locations}


class ReceptionTree:
    reception_nodes: list[ReceptionNode] = []
    first_reception: int
    last_reception: int

    def get_node(self, id: int) -> ReceptionNode:
        nodes_dict = {node.id: node for node in self.reception_nodes}
        return nodes_dict[id]


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


def _clone_reception_nodes() -> list[ReceptionNode]:
    return copy.deepcopy(reception_nodes)


def _clone_floors() -> list[Floor]:
    return copy.deepcopy(vanilla_floors)


def _reset_book_classifications() -> None:
    for book in books:
        items_by_name[book.name].copies = 0
        items_by_name[book.name].type = ItemClassification.filler


def _book_chapter(book: BookInfo) -> int:
    chapter = (book.id // 10000) - 19
    return max(1, min(7, chapter))


def _reset_req_books(tree: ReceptionTree, floors: list[Floor]) -> None:
    for node in tree.reception_nodes:
        node.req_books = []

    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            stage.req_books = []


def _stage_to_floor_lookup(floors: list[Floor]) -> dict[int, Floor]:
    lookup: dict[int, Floor] = {}
    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            lookup[stage.id] = floor
    return lookup


def _outdegree(edges: list[tuple[str, str]], node: ProgressionNode) -> int:
    return sum(1 for src, _ in edges if src == node.key)


def _edge_respects_chapter_sanity(source: ProgressionNode, target: ProgressionNode) -> bool:
    if target.name == "Oliver":
        return True

    return source.chapter <= target.chapter + 1


def _add_edge_once(edges: list[tuple[str, str]], source: ProgressionNode, target: ProgressionNode) -> bool:
    if source.key == target.key:
        return False

    if not _edge_respects_chapter_sanity(source, target):
        return False

    edge = (source.key, target.key)
    if edge in edges:
        return True

    if _outdegree(edges, source) >= source.source.checks:
        return False

    edges.append(edge)
    return True


def _topological_order(nodes_by_key: dict[str, ProgressionNode], edges: list[tuple[str, str]]) -> list[ProgressionNode]:
    outgoing: dict[str, list[str]] = {key: [] for key in nodes_by_key}
    indegree: dict[str, int] = {key: 0 for key in nodes_by_key}

    for src, dst in edges:
        if src not in nodes_by_key or dst not in nodes_by_key:
            raise Exception(f"LORAP graph edge references an unknown node: {src} -> {dst}")
        outgoing[src].append(dst)
        indegree[dst] += 1

    def sort_key(key: str) -> tuple[float, int]:
        node = nodes_by_key[key]
        return node.progression_weight, node.id

    queue = sorted([key for key, degree in indegree.items() if degree == 0], key=sort_key)
    ordered_keys: list[str] = []

    while queue:
        key = queue.pop(0)
        ordered_keys.append(key)

        for child in sorted(outgoing.get(key, []), key=sort_key):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
                queue.sort(key=sort_key)

    if len(ordered_keys) != len(nodes_by_key):
        raise Exception("LORAP integrated progression graph contains a cycle")

    return [nodes_by_key[key] for key in ordered_keys]


def _candidate_by_weight(
    rng: random.Random,
    candidates: list[ProgressionNode],
    target_weight: float,
    lower: bool,
    fallback: ProgressionNode,
) -> ProgressionNode:
    if lower:
        pool = [node for node in candidates if node.progression_weight < target_weight]
    else:
        pool = [node for node in candidates if node.progression_weight > target_weight]

    if not pool:
        return fallback

    pool.sort(key=lambda n: abs(n.progression_weight - target_weight))
    window = pool[:min(len(pool), rng.randint(3, 7))]
    return rng.choice(window)


def _assign_progression_weights(rng: random.Random, nodes: list[ProgressionNode], randomized: bool) -> None:
    for node in nodes:
        base = node.chapter * 10.0
        if node.kind == "stage":
            base += 1.2
        if "Realization" in node.name:
            base += 6.5
        base += max(0, node.req_librarians - 1) * 2.6
        base += min(node.source.checks, 11) * 0.18

        if randomized:
            base += rng.gauss(0.0, 8.0)
        else:
            base += (0.35 if node.kind == "stage" else 0.0)

        node.progression_weight = base


def _assign_procedural_visual_layout(
    rng: random.Random,
    ordered: list[ProgressionNode],
    edges: list[tuple[str, str]],
    first: ProgressionNode,
    last: ProgressionNode,
    randomized: bool,
) -> None:
    nodes_by_key = {node.key: node for node in ordered}
    parents: dict[str, list[str]] = {node.key: [] for node in ordered}
    children: dict[str, list[str]] = {node.key: [] for node in ordered}

    for src, dst in edges:
        parents[dst].append(src)
        children[src].append(dst)

    y_step = 175.0 if randomized else 150.0
    min_dy = 80.0
    branch_step = 280.0 if randomized else 220.0
    max_y_jitter = 70.0 if randomized else 20.0
    max_x_jitter = 115.0 if randomized else 20.0

    first.visual_x = 0.0
    first.visual_y = 0.0

    for node in ordered:
        if node.key == first.key:
            continue

        parent_nodes = [nodes_by_key[key] for key in parents.get(node.key, []) if key in nodes_by_key]
        if parent_nodes:
            parent_avg_x = sum(parent.visual_x for parent in parent_nodes) / len(parent_nodes)
            min_parent_y = max(parent.visual_y for parent in parent_nodes)
        else:
            parent_avg_x = 0.0
            min_parent_y = -y_step

        base_y = node.order_index * y_step
        if randomized:
            base_y += rng.uniform(-max_y_jitter, max_y_jitter)
        node.visual_y = max(base_y, min_parent_y + min_dy)

        if node.backbone:
            center_bias = rng.uniform(-75.0, 75.0) if randomized else 0.0
            node.visual_x = parent_avg_x * 0.45 + center_bias
        elif len(parent_nodes) >= 2:
            node.visual_x = parent_avg_x + rng.uniform(-max_x_jitter * 0.45, max_x_jitter * 0.45)
        else:
            side = node.branch_side if node.branch_side != 0 else (-1 if rng.random() < 0.5 else 1)
            node.visual_x = parent_avg_x + side * rng.uniform(branch_step * 0.65, branch_step * 1.35)
            node.visual_x += rng.uniform(-max_x_jitter, max_x_jitter)

    last.visual_x *= 0.35
    last.visual_y = max(last.visual_y, max(node.visual_y for node in ordered if node.key != last.key) + min_dy)

    for _ in range(6):
        for src, dst in edges:
            source = nodes_by_key[src]
            target = nodes_by_key[dst]
            if target.visual_y <= source.visual_y + min_dy:
                target.visual_y = source.visual_y + min_dy

    min_distance_x = 185.0
    min_distance_y = 120.0
    for _ in range(10):
        moved = False
        by_band: dict[int, list[ProgressionNode]] = {}
        for node in ordered:
            band = int(round(node.visual_y / min_distance_y))
            by_band.setdefault(band, []).append(node)

        for band_nodes in by_band.values():
            band_nodes.sort(key=lambda n: n.visual_x)
            for i in range(1, len(band_nodes)):
                left = band_nodes[i - 1]
                right = band_nodes[i]
                diff = right.visual_x - left.visual_x
                if diff < min_distance_x:
                    push = (min_distance_x - diff) / 2.0
                    left.visual_x -= push
                    right.visual_x += push
                    moved = True
        if not moved:
            break

    for node in ordered:
        node.visual_x = round(node.visual_x, 2)
        node.visual_y = round(node.visual_y, 2)


def build_mixed_battle_graph(
    rng: random.Random,
    tree: ReceptionTree,
    floors: list[Floor],
    randomized: bool,
) -> tuple[list[ProgressionNode], list[tuple[str, str]], dict[int, int]]:
    stage_floors = _stage_to_floor_lookup(floors)
    nodes_by_key: dict[str, ProgressionNode] = {}

    def add_reception(node: ReceptionNode) -> ProgressionNode:
        key = f"reception:{node.id}"
        if key not in nodes_by_key:
            nodes_by_key[key] = ProgressionNode(
                key=key,
                name=node.name,
                id=node.id,
                chapter=node.chapter,
                req_librarians=node.req_librarians,
                kind="reception",
                source=node,
            )
        return nodes_by_key[key]

    def add_stage(stage: FloorStage) -> ProgressionNode:
        key = f"stage:{stage.id}"
        if key not in nodes_by_key:
            nodes_by_key[key] = ProgressionNode(
                key=key,
                name=stage.name,
                id=stage.id,
                chapter=max(1, min(7, stage.chapter)),
                req_librarians=stage.req_librarians,
                kind="stage",
                source=stage,
                floor=stage_floors[stage.id],
            )
        return nodes_by_key[key]

    first = add_reception(tree.get_node(tree.first_reception))
    last = add_reception(tree.get_node(tree.last_reception))

    for reception in tree.reception_nodes:
        if reception.id not in (tree.first_reception, tree.last_reception):
            add_reception(reception)

    for floor in floors:
        for stage in [*floor.abno_stages, floor.realization_stage]:
            add_stage(stage)

    ordinary_nodes = [node for node in nodes_by_key.values() if node.key not in {first.key, last.key}]
    _assign_progression_weights(rng, ordinary_nodes, randomized)
    first.progression_weight = -1000.0
    last.progression_weight = 1000.0
    ordinary_nodes.sort(key=lambda node: (node.progression_weight, rng.random() if randomized else node.id))

    total = len(ordinary_nodes)
    if randomized:
        backbone_count = max(10, min(total, int(total * rng.uniform(0.36, 0.50))))
    else:
        backbone_count = max(12, min(total, int(total * 0.62)))

    backbone: list[ProgressionNode] = []
    if backbone_count > 0:
        for i in range(backbone_count):
            index = round((i + 1) * (total + 1) / (backbone_count + 1)) - 1
            if randomized:
                index += rng.randint(-2, 2)
            index = max(0, min(total - 1, index))
            candidate = ordinary_nodes[index]
            if candidate not in backbone:
                backbone.append(candidate)

    while len(backbone) < backbone_count:
        candidate = rng.choice(ordinary_nodes) if randomized else ordinary_nodes[len(backbone)]
        if candidate not in backbone:
            backbone.append(candidate)

    backbone.sort(key=lambda node: node.progression_weight)
    for node in backbone:
        node.backbone = True
        node.branch_side = 0

    edges: list[tuple[str, str]] = []
    main_path = [first, *backbone, last]
    for source, target in zip(main_path, main_path[1:]):
        if not _add_edge_once(edges, source, target):
            raise Exception(f"LORAP could not connect main path edge {source.key} -> {target.key}")

    side_pool = [node for node in ordinary_nodes if node not in backbone]
    cursor = 0
    side_seed = -1
    while cursor < len(side_pool):
        if randomized:
            branch_len = 1
            if cursor + 1 < len(side_pool) and rng.random() < 0.42:
                branch_len += 1
            if cursor + 2 < len(side_pool) and rng.random() < 0.16:
                branch_len += 1
        else:
            branch_len = 1 if cursor % 3 else 2

        branch = side_pool[cursor:cursor + branch_len]
        cursor += branch_len
        if not branch:
            continue

        side_seed *= -1
        for node in branch:
            node.branch_side = side_seed

        source_candidates = [
            node for node in [first, *backbone]
            if _outdegree(edges, node) < node.source.checks
            and _edge_respects_chapter_sanity(node, branch[0])
            and node.progression_weight < branch[0].progression_weight
        ]
        source = _candidate_by_weight(rng, source_candidates, branch[0].progression_weight, True, first)
        if not _add_edge_once(edges, source, branch[0]):
            raise Exception(f"LORAP could not attach side branch {branch[0].key}")

        for parent, child in zip(branch, branch[1:]):
            _add_edge_once(edges, parent, child)

        merge_chance = 0.48 if randomized else 0.25
        if rng.random() < merge_chance:
            target_candidates = [*backbone, last]
            target = _candidate_by_weight(rng, target_candidates, branch[-1].progression_weight, False, last)
            if target.progression_weight > branch[-1].progression_weight:
                _add_edge_once(edges, branch[-1], target)

    if randomized:
        extra_edges = rng.randint(3, 7)
        all_nodes = [node for node in [first, *ordinary_nodes] if _outdegree(edges, node) < node.source.checks]
        for _ in range(extra_edges):
            if not all_nodes:
                break
            source = rng.choice(all_nodes)
            target_pool = [
                node for node in [*ordinary_nodes, last]
                if node.progression_weight > source.progression_weight + 4.0
                and _edge_respects_chapter_sanity(source, node)
            ]
            if not target_pool:
                continue
            target_pool.sort(key=lambda node: abs(node.progression_weight - source.progression_weight))
            target = rng.choice(target_pool[:min(len(target_pool), 10)])
            _add_edge_once(edges, source, target)

    ordered = _topological_order(nodes_by_key, edges)
    for index, node in enumerate(ordered):
        node.order_index = index

    _assign_procedural_visual_layout(rng, ordered, edges, first, last, randomized)
    stage_chapters = {node.id: node.chapter for node in nodes_by_key.values() if node.kind == "stage"}
    return ordered, edges, stage_chapters


def assign_archipelago_book_requirements(
    rng: random.Random,
    progression_nodes: list[ProgressionNode],
    progression_edges: list[tuple[str, str]],
    options: LOROptions,
) -> set[int]:
    _reset_book_classifications()

    require_receptions = _option_enabled(options, "receptions_require_books")
    require_floors = _option_enabled(options, "floors_require_books")
    chaotic_books = _option_enabled(options, "chaotic_book_progression") if hasattr(options, "chaotic_book_progression") else False

    used_books: set[int] = set()
    max_index = max(1, len(progression_nodes) - 1)
    first_key = progression_nodes[0].key if progression_nodes else ""
    bootstrap_bookless_count = rng.randint(3, 4)
    bootstrap_keys = {node.key for node in progression_nodes[:bootstrap_bookless_count]}
    bootstrap_keys.update(dst for src, dst in progression_edges if src == first_key)

    def node_accepts_books(node: ProgressionNode) -> bool:
        if node.kind == "reception":
            return require_receptions
        if node.kind == "stage":
            return require_floors
        return False

    def progress_fraction(node: ProgressionNode) -> float:
        return max(0.0, min(1.0, node.order_index / max_index))

    def desired_book_count(node: ProgressionNode) -> int:
        if not node_accepts_books(node) or node.key in bootstrap_keys:
            return 0

        progress = progress_fraction(node)
        if progress <= 0.35:
            return 1
        if progress <= 0.70:
            return 2 if rng.random() < 0.38 else 1

        count = 2 if rng.random() < 0.68 else 1
        if count < 3 and rng.random() < 0.34:
            count += 1
        return min(3, count)

    def candidate_books_for_node(node: ProgressionNode, already_selected: set[int]) -> list[BookInfo]:
        if chaotic_books:
            return [book for book in books if book.id not in already_selected]

        drift = 2 if progress_fraction(node) > 0.65 and rng.random() < 0.25 else 1
        min_chapter = max(1, node.chapter - drift)
        max_chapter = min(7, node.chapter + (1 if rng.random() < 0.20 else 0))
        candidates = [
            book for book in books
            if book.id not in already_selected and min_chapter <= _book_chapter(book) <= max_chapter
        ]
        return candidates or [book for book in books if book.id not in already_selected]

    def mark_book_as_progression(book: BookInfo) -> None:
        if book.id not in used_books:
            used_books.add(book.id)
            items_by_name[book.name].copies = 1
            items_by_name[book.name].type = ItemClassification.progression

    recent_books_by_index: dict[int, list[int]] = {}
    for node in progression_nodes:
        target_count = desired_book_count(node)
        if target_count <= 0:
            continue

        selected: set[int] = set(node.req_books)
        recent_pool = [book_id for i in range(max(0, node.order_index - 12), node.order_index) for book_id in recent_books_by_index.get(i, [])]
        if recent_pool and rng.random() < 0.18:
            selected.add(rng.choice(recent_pool))

        while len(selected) < target_count:
            candidates = [book for book in candidate_books_for_node(node, selected) if book.id not in used_books]
            if not candidates:
                candidates = candidate_books_for_node(node, selected)
            if not candidates:
                break
            selected.add(rng.choice(candidates).id)

        recent_books_by_index[node.order_index] = []
        for book_id in selected:
            book = books_dict[book_id]
            mark_book_as_progression(book)
            if book_id not in node.req_books:
                node.req_books.append(book_id)
            recent_books_by_index[node.order_index].append(book_id)

    return used_books


def validate_setup_result(result: LORSetupResult) -> None:
    nodes_by_key = {node.key: node for node in result.progression_nodes}
    outgoing: dict[str, list[str]] = {key: [] for key in nodes_by_key}
    indegree: dict[str, int] = {key: 0 for key in nodes_by_key}

    for src, dst in result.progression_edges:
        if src == dst:
            raise Exception(f"LORAP graph has a self-cycle on {src}")
        if src not in nodes_by_key or dst not in nodes_by_key:
            raise Exception(f"LORAP graph edge references an unknown node: {src} -> {dst}")
        outgoing[src].append(dst)
        indegree[dst] += 1
        if nodes_by_key[dst].progression_weight <= nodes_by_key[src].progression_weight and dst != f"reception:{result.tree.last_reception}":
            raise Exception(f"LORAP graph has a backwards edge: {src} -> {dst}")

    first_key = f"reception:{result.tree.first_reception}"
    last_key = f"reception:{result.tree.last_reception}"
    for key, child_keys in outgoing.items():
        node = nodes_by_key[key]
        if len(child_keys) > node.source.checks:
            raise Exception(f"LORAP node {key} has {len(child_keys)} children but only {node.source.checks} locations")

    roots = [key for key, degree in indegree.items() if degree == 0]
    if roots != [first_key]:
        raise Exception(f"LORAP graph must start only from Rats, got roots: {roots}")

    for child_key in outgoing.get(first_key, []):
        if nodes_by_key[child_key].req_books:
            raise Exception(f"LORAP immediate Rats child has book requirements: {child_key}")

    queue = [first_key]
    reached: set[str] = set()
    while queue:
        key = queue.pop(0)
        if key in reached:
            continue
        reached.add(key)
        queue.extend(outgoing.get(key, []))

    if len(reached) != len(nodes_by_key):
        missing = sorted(set(nodes_by_key) - reached)
        raise Exception(f"LORAP graph has unreachable nodes: {missing[:5]}")

    if last_key not in reached:
        raise Exception("LORAP Oliver is unreachable")

    for node in result.progression_nodes:
        if node.key == first_key and node.req_books:
            raise Exception("LORAP Rats has book requirements")
        if node.kind == "stage" and node.floor is None:
            raise Exception(f"LORAP stage node has no assigned floor: {node.key}")
        for book_id in node.req_books:
            if book_id not in books_dict:
                raise Exception(f"LORAP node {node.key} requires unknown book {book_id}")
            if book_id not in result.used_book_requirements:
                raise Exception(f"LORAP node {node.key} requires book {book_id} that was not marked as progression")

    for src, dst in result.progression_edges:
        if nodes_by_key[dst].visual_y <= nodes_by_key[src].visual_y:
            raise Exception(f"LORAP visual layout has a backwards edge: {src} -> {dst}")


def setup_locations(rng: random.Random, options: LOROptions) -> LORSetupResult:
    tree = ReceptionTree()
    tree.reception_nodes = _clone_reception_nodes()
    tree.first_reception = tree.reception_nodes[0].id
    tree.last_reception = tree.reception_nodes[-1].id

    floors = _clone_floors()
    _reset_req_books(tree, floors)

    if options.shuffle_abnos:
        abnos_per_chapter = [[] for _ in range(7)]
        for floor in floors:
            for stage in floor.abno_stages:
                abnos_per_chapter[stage.chapter - 1].append(stage)
            floor.abno_stages = [None] * len(floor.abno_stages)

        all_abnos = []
        for chapter_list in abnos_per_chapter:
            rng.shuffle(chapter_list)
            all_abnos.extend(chapter_list)

        while all_abnos:
            floors_to_fill = [floor for floor in floors if None in floor.abno_stages]
            floor = rng.choice(floors_to_fill)
            floor.abno_stages[floor.abno_stages.index(None)] = all_abnos.pop(0)

    if options.shuffle_realizations:
        realizations = [floor.realization_stage for floor in floors]
        rng.shuffle(realizations)
        for floor in floors:
            floor.realization_stage = realizations.pop(0)

    last_error: Exception | None = None

    for _ in range(100):
        try:
            _reset_req_books(tree, floors)
            progression_nodes, progression_edges, abno_stage_chapters = build_mixed_battle_graph(rng, tree, floors, True)
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
            last_error = error

    raise Exception(f"LORAP failed to generate a valid procedural progression graph: {last_error}")
