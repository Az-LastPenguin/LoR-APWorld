import random, math
from dataclasses import dataclass
from BaseClasses import Location, ItemClassification
from .options import LOROptions
from .util import box_muller_constraint
from .gamedata.receptions import ReceptionNode, reception_nodes, receptions_dict
from .gamedata.abnormalities import Floor, FloorStage, floors, floor_stages
from .gamedata.books import BookInfo, books
from .items import items_by_name

class LORLocation(Location):
    game: str = "Library of Ruina"

@dataclass
class LORLocationData:
    id: int
    name: str
 
reception_locations: list[LORLocationData] = []
for i, r in receptions_dict.items():
    for j in range(r.checks):
        reception_locations.append(LORLocationData(r.id | (j << 28), r.name+" ("+str(j+1)+")"))

abno_locations: list[LORLocationData] = []
for s in floor_stages:
    for i in range(s.checks):
        abno_locations.append(LORLocationData(r.id | (i << 28), s.name+" ("+str(i+1)+")"))

all_locations = [location for location in [*reception_locations, *abno_locations]]
locations_id_to_name = {location.id: location.name for location in all_locations}
locations_name_to_id = {location.name: location.id for location in all_locations}


class ReceptionTree:
    reception_nodes: list[ReceptionNode] = []
    node_depths: dict[int, int] = {}
    first_reception: int
    last_reception: int

    def get_node(self, id: int) -> ReceptionNode:
        nodes_dict = {node.id: node for node in self.reception_nodes}

        return nodes_dict[id]
    
    def get_prev_nodes(self, id: int) -> list[ReceptionNode]:
        return [node for node in self.reception_nodes if id in node.next]

    def get_depth(self, id: int) -> int:
        return self.node_depths[id]
    
    def get_nodes_of_depth(self, depth: int) -> list[ReceptionNode]:
        return [node for node in self.reception_nodes if self.get_depth(node.id) == depth]

    def calc_depth(self):
        def depth(node: ReceptionNode, prev: int):
            self.node_depths[node.id] = min(self.node_depths.get(node.id, 200), prev + 1)

            for n in node.next:
                depth(self.get_node(n), self.node_depths[node.id])

        depth(self.get_node(self.first_reception), -1)

        
def setup_locations(random: random.Random, options: LOROptions):
    # Create the reception tree
    tree = ReceptionTree()
    tree.reception_nodes = reception_nodes if options.randomize_reception_tree.value == 0 else generate_reception_tree(random)
    tree.first_reception = tree.reception_nodes[0].id
    tree.last_reception = tree.reception_nodes[-1].id
    tree.calc_depth()

    # Randomize abnos/realizations if needed
    run_floors = floors.copy()
    if options.abno_randomization.value == 1:
        for f in run_floors:
            random.shuffle(f.abno_stages)
    elif options.abno_randomization == 2:
        stages = []
        for f in run_floors:
            stages.extend(f.abno_stages)
        
        random.shuffle(stages)

        for f in run_floors:
            abnos = len(f.abno_stages)
            f.abno_stages.clear()

            for i in range(abnos):
                f.abno_stages.append(stages.pop(0))

    if options.shuffle_realizations == 1:
        stages = []
        for f in run_floors:
            stages.append(f.realization_stage)
        
        random.shuffle(stages)

        for f in run_floors:
            f.realization_stage = stages.pop(0)

    # Set book requirements
    if options.receptions_progression == 2 or options.receptions_progression == 3 or options.floor_progression == 1:
        book_pool: list[BookInfo] = books.copy()

        # Remove ~10% of the books from the pool, frees up the space for misc items
        for i in range(len(book_pool)//10):
            book = book_pool.pop(random.randint(0, len(book_pool)-1))
            # Also change them from progression to filler since they're no longer required in the progression
            items_by_name[book.name].type = ItemClassification.filler

        # One book for each reception/abno
        stages: list[ReceptionNode | FloorStage] = []
        if options.receptions_progression == 2 or options.receptions_progression == 3:
            for n in tree.reception_nodes:
                if n.id == tree.first_reception: continue

                n.req_books.append(book_pool.pop(random.randint(0, len(book_pool)-1)).id)

                if tree.get_depth(n.id) > 2:
                    stages.append(n)

        if options.floor_progression == 1:
            for stage in floor_stages:
                stage.req_books.append(book_pool.pop(random.randint(0, len(book_pool)-1)).id)
                stages.append(stage)

        # Require leftover books in random stages
        while len(book_pool) > 0:
            stage: ReceptionNode | FloorStage = stages[random.randint(0, len(stages)-1)]

            stage.req_books.append(book_pool.pop(random.randint(0, len(book_pool)-1)).id)

            if len(stage.req_books) > 2:
                stages.remove(stage)

        # If somehow there are still books, we make them filler items
        for book in book_pool:
            items_by_name[book.name].type = ItemClassification.filler
    else:
        for book in books:
            items_by_name[book.name].type = ItemClassification.filler

    return tree, run_floors

## RECEPTION RANDOMIZATON
def generate_reception_tree(random: random.Random):
    # Before everything, shuffle receptions in their chapters to make things worse
    copy = reception_nodes.copy()
    first_node = copy.pop(0)
    last_node = copy.pop()
    all_nodes: list[ReceptionNode] = []

    for i in range(1, 8):
        chapter_nodes = [n for n in copy if n.chapter == i]
        random.shuffle(chapter_nodes)
        all_nodes = [*all_nodes, *chapter_nodes]

    # Select height and amounts of nodes per each height level
    height = random.randint(18, 25)
    node_amounts = {i: 1 for i in range(height)}

    i = len(all_nodes) - height
    while True:
        y = round(box_muller_constraint(random, 1, height-1))
        if node_amounts[y] >= 6:
           continue

        node_amounts[y] += 1
        i -= 1

        if i <= 0:
            break
    
    # Distribute receptions
    nodes: list[list[ReceptionNode]] = [[] for i in range(height)]

    first_node.y = 0
    first_node.next = []
    last_node.y = height-1

    nodes[0] = [first_node]
    nodes[-1] = [last_node]
    for i, v in node_amounts.items():
        if i == 0 or i == height-1:
            continue
        
        nodes[i] = []
        for _ in range(v):
            ri = 0
            while ri < len(all_nodes)-1 and random.random() >= 0.5:
                ri += 1

            node = all_nodes.pop(ri)
            node.y = i
            node.next = []

            nodes[i].append(node)
    
    # DEBUG
    for i in range(len(nodes)):
        print(f"[{i}] {"-"*len(nodes[i])}")

    # Create connections
    for i in range(1, height):
        for node in nodes[i]:
            candidates = nodes[i-1].copy()
            j = 0
            while True:
                random.shuffle(candidates)
                candidate = candidates.pop(0)
                candidate.next.append(node.id)
                j += 1

                if len(candidates) <= 0 or j >= 2 or random.random() < 0.80:
                    break
            
            print(f"[{j}] Node: {node.id}, connections: {i}")

    # Put everything in a list
    result_nodes_list = []
    for v in nodes:
        for n in v:
            print(f"{n.name} - {len(n.next)}")
            result_nodes_list.append(n)

    return result_nodes_list