import random
from dataclasses import dataclass
from BaseClasses import Location, ItemClassification
from .gamedata.receptions import ReceptionGroupInfo, vanilla_reception_groups, receptions, receptions_dict
from .gamedata.abnormalities import Floor, FloorStage, floors, floor_stages
from .gamedata.books import books
from .items import items_by_name

class LORLocation(Location):
    game: str = "Library of Ruina"

@dataclass
class LORLocationData:
    id: int
    name: str

reception_locations: list[LORLocationData] = []
for r in receptions:
    for i in range(r.checks):
        reception_locations.append(LORLocationData(r.id | (i << 28), r.name+" ("+str(i+1)+")"))

abno_locations: list[LORLocationData] = []
for s in floor_stages:
    for i in range(s.checks):
        abno_locations.append(LORLocationData(r.id | (i << 28), s.name+" ("+str(i+1)+")"))

all_locations = [location for location in [*reception_locations, *abno_locations]]
locations_id_to_name = {location.id: location.name for location in all_locations}
locations_name_to_id = {location.name: location.id for location in all_locations}

def setup_locations(random: random.Random, reception_option: int, abno_option: int, realization_option: int):
    reception_groups = []
    reception_tree = []
    floors_list = []

    # Setup Receptions
    if reception_option == 0:
        reception_groups = vanilla_reception_groups.copy()
    elif reception_option == 1:
        reception_groups, reception_tree = generate_reception_tree(random)
        reception_groups.extend([group for group in vanilla_reception_groups if group.chapter == 8])


    # Randomize books required for the receptions if needed
    book_list = books.copy()
    # Each reception requires atleast one book
    for g in reception_groups:
        for r in g.receptions:
            if r == 2:
                continue
            
            reception = receptions_dict[r]
            reception.req_books.append(book_list.pop(random.randint(0, len(book_list)-1)).id)

    # Cut down like 10% of the books that will be required just to make some more free space in the item pool
    for i in range(len(book_list)//10):
        book = book_list.pop(random.randint(0, len(book_list)-1))
        # Also change them from progression to filler since they're no longer required in the progression
        items_by_name[book.name].type = ItemClassification.filler

    # Some receptions may require more than one book
    receptions = []
    for g in [group for group in reception_groups if group.chapter > 2]:
        receptions.extend(g.receptions)

    while len(book_list) > 0:
        rid = receptions[random.randint(0, len(receptions)-1)]
        reception = receptions_dict[rid]
        reception.req_books.append(book_list.pop(random.randint(0, len(book_list)-1)).id)

        if len(reception.req_books) == 3:
            receptions.remove(rid)


    # Abnos
    floors_list = floors.copy()
    if abno_option == 1:
        for f in floors_list:
            random.shuffle(f.abno_stages)
    elif abno_option == 2:
        stages = []
        for f in floors_list:
            stages.extend(f.abno_stages)
        
        random.shuffle(stages)

        for f in floors_list:
            abnos = len(f.abno_stages)
            f.abno_stages.clear()

            for i in range(abnos):
                f.abno_stages.append(stages.pop(0))
    
    # Realization
    if realization_option == 1:
        stages = []
        for f in floors_list:
            stages.append(f.realization_stage)
        
        random.shuffle(stages)

        for f in floors_list:
            f.realization_stage = stages.pop(0)

    return (reception_groups, reception_tree, floors_list)

# For reception tree randomization
class MapNode():
    chapter: int # Node's chapter (used in generation only)
    receptions: list[int] # Receptions in this node
    expect_receptions: int # How much receptions is expected to be put in this node (used in generation only)
    prev: list['MapNode'] # Nodes that go after this one
    next: list['MapNode'] # Nodes that go before this one
    X: int # aka Column
    Y: int # aka Row / Depth

    def __init__(self, chapter: int, X: int, Y: int):
        self.chapter = chapter
        self.receptions = []
        self.expect_receptions = 0
        self.prev = []
        self.next = []
        self.X = X
        self.Y = Y

    def addprev(self, prev: 'MapNode') -> 'MapNode':
        prev.next.append(self)
        self.prev.append(prev)

        return self

    def addnext(self, next: 'MapNode') -> 'MapNode':
        next.prev.append(self)
        self.next.append(next)

        return self
    
    def getdata(self) -> bytes:
        # result bigint with size of 14 containing all the data
        intdata = 0

        # 9 byte bigint containing list of receptions in the node
        receptions = 0
        for i in range(len(self.receptions)):
            receptions = (self.receptions[i].id << 24 * i) | receptions
        
        # 2 byte + 5 bit int containing list of nodes that come after this one (connections)
        next = 0
        for i in range(len(self.next)):
            next = (self.next[i].id << 7 * i) | next
        
        # 1 byte + 2 bit short containing X and Y of the node
        pos = (self.X << 5) | self.Y

        intdata = (receptions << 38) | (next << 17) | (pos << 7) | self.id 

        return intdata.to_bytes(14, byteorder='big')
    
@dataclass
class ChapterSettings:
    chapter: int
    max_width: int
    min_height: int
    max_height: int
    branch_chance: int

def generate_reception_tree(random: random.Random):
    #print("------------[GENERATION START]------------")
    #print("------------[GENERATING BRANCHES]------------")
    # ---[STEP 1]---
    # Generate tree of max width. Height is randomized and depends on each chapter's possible height.
    # Main Branch at X = 0 nodes always have a connection to a node above itself if any
    chapter_settings = [
        ChapterSettings(chapter=1, max_width=3, min_height=2, max_height=3, branch_chance=30),
        ChapterSettings(chapter=2, max_width=3, min_height=2, max_height=3, branch_chance=35),
        ChapterSettings(chapter=3, max_width=5, min_height=2, max_height=3, branch_chance=50),
        ChapterSettings(chapter=4, max_width=5, min_height=3, max_height=4, branch_chance=40),
        ChapterSettings(chapter=5, max_width=5, min_height=3, max_height=4, branch_chance=30),
        ChapterSettings(chapter=6, max_width=5, min_height=4, max_height=5, branch_chance=50),
        ChapterSettings(chapter=7, max_width=3, min_height=2, max_height=3, branch_chance=30),
    ]
    start_node: MapNode = MapNode(1, 0, 0)
    cur_x: int = 0
    cur_y: int = 0
    tree: list[MapNode] = [start_node]
    all_receptions: list[int] = [r.id for r in receptions if r.chapter != 8]
    total_receptions = len(all_receptions)

    for cs in chapter_settings:
        chapter_height = random.randint(cs.min_height, cs.max_height)
        for i in range(chapter_height):
            cur_y += 1
            cur_x = -(cs.max_width // 2)
            for j in range(cs.max_width):
                new = MapNode(cs.chapter, cur_x, cur_y)
                prev_layer_nodes = [node for node in tree if node.X == 0 and node.Y == cur_y - 1] # Always either 0 or 1
                if cur_x == 0 and len(prev_layer_nodes) > 0:
                    prev_layer_nodes[0].addnext(new)
                cur_x += 1
                tree.append(new)


    #print("------------[GENERATING CONNECTIONS]------------")
    # ---[STEP 2]---
    # Generate random connections between nodes
    for n in tree:
        possible_nodes = [node for node in tree if (node.X >= n.X - 1 and node.X <= n.X + 1) and node.Y == n.Y + 1]

        for i in possible_nodes:
            if not n in i.prev and random.random() <= chapter_settings[n.chapter - 1].branch_chance * 0.01:
                n.addnext(i)

    #print("------------[REMOVING BAD NODES]------------")
    # ---[STEP 3]---
    # 3.1. Remove nodes that have no path going to them
    for n in tree.copy():
        if (n.X != 0 and n. Y != 0) and len(n.prev) == 0:
            for i in n.next:
                i.prev.remove(n)
            tree.remove(n)


    # 3.2. Remove dead-end nodes at max Y level (except the node at X = 0)
    for n in [node for node in tree if node.Y == cur_y and node.X != 0]:
        for i in n.prev:
            i.next.remove(n)
        tree.remove(n)


    # 3.3. If there is more than total_receptions nodes (65 is total amount of unique receptions in vanilla game) remove as much dead-end nodes as needed to get to total_receptions total nodes.
    if len(tree) > total_receptions:
        #print("------------[REMOVING EXCESS NODES]------------")
        for i in range(len(tree) - total_receptions):
            # Get all dead-end nodes
            dead_ends = [node for node in tree if len(node.next) == 0 and node.X != 0]
            # Select random dead-end node and remove it
            n = dead_ends[random.randint(0, len(dead_ends) - 1)]
            for j in n.prev:
                j.next.remove(n)
            tree.remove(n)


    #print("------------[POPULATING]------------")
    # ---[STEP 4]---
    # Decide how much receptions should be put into each node and put them in
    # 4.1. Set expected receptions to 1 for each node
    for n in tree:
        n.expect_receptions = 1

    # 4.2. If there is less than total_receptions nodes then we can put more receptions in random nodes
    if len(tree) < total_receptions:
        for i in range (total_receptions - len(tree)):
            nodes = [node for node in tree if node.expect_receptions < 3]
            nodes[random.randint(0, len(nodes) - 1)].expect_receptions += 1

    # 4.3. Put Rats Reception into the first node
    tree[0].receptions.append(2)
    all_receptions.remove(2)

    # 4.4. Put receptions into every other node
    queue: list[MapNode] = [tree[0], *tree[0].next]

    while len(queue) > 0:
        # Get current Node
        node = queue.pop(0)

        # Put receptions there
        if len(node.receptions) < node.expect_receptions:
            for i in range(node.expect_receptions - len(node.receptions)):
                i = 0
                while i < len(all_receptions)-1 and random.random() >= 0.5:
                    i += 1

                reception = all_receptions.pop(i)

                node.receptions.append(reception)
                queue.extend(node.next)

    # Convert randomized tree into ReceptionGroupInfos for the server to process
    queue: list[MapNode] = tree[0]
    converted: dict[MapNode, ReceptionGroupInfo] = {}
    i = 1
    for n in tree:
        converted[n] = ReceptionGroupInfo(id=i, chapter=n.chapter, prev_groups=[], next_groups=[], receptions=n.receptions)
        i += 1

    for n in tree:
        converted[n].next_groups = [converted[node].id for node in n.next]
        converted[n].prev_groups = [converted[node].id for node in n.prev]
        
        # Set next group of the last group in the tree to 999 (workaround for finding last reception in the tree for logic)
        if n.X == 0 and n.Y == cur_y:
            converted[n].next_groups.append(999)

    # Return cconverted tree and the tree itself
    return (list(converted.values()), tree)