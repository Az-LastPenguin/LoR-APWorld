from BaseClasses import Location
from typing import NamedTuple
import random

class LORLocation(Location):
    game: str = "Library of Ruina"


class StageInfo:
    id: int
    name: str
    checks: int
    chapter: int
    next: list[int] # For the vanilla map
    librarians: int

    locations: dict[str, int]

    def __init__(self, id: int, name: str, checks: int = 1, chapter: int = 0, next: list[int] = [], librarians: int = 1):
        self.id = id
        self.name = name
        self.checks = checks
        self.chapter = chapter
        self.next = next
        self.librarians = librarians

        self.locations = {}
        
        for i in range(self.checks):
            self.locations[self.name+" ("+str(i+1)+")"] = self.id | (i << 28)


canard: list[StageInfo] = [
    # Receptions
    StageInfo(2, "Rats", 2, 1, [3]),
    StageInfo(3, "Yun's Office Fixers", 2, 1, [4]),
    StageInfo(4, "Yun's Office Rookie", 2, 1, [5]),
    StageInfo(5, "Yun's Office", 2, 1, [6]),
    StageInfo(6, "Brotherhood of Iron", 2, 1, [7]),
    StageInfo(7, "Hook Office", 2, 1, [10001, 100001, 100002, 100003]),
]

myth: list[StageInfo] = [
    # Receptions
    StageInfo(10001, "Pierre's Bistro", 2, 2, [10002]),
    StageInfo(10002, "Streetlight Office", 2, 2, [10003]),
    StageInfo(10003, "Lulu of Streetlight", 2, 2, [20001, 100004, 100005, 100006, 100007, 100008]),

    # General Receptions
    StageInfo(100003, "Urban Myth-class Syndicate", 2, 2),
    StageInfo(100002, "Hook Office Remnants", 2, 2),
    StageInfo(100001, "Backstreets Butchers", 2, 2),
]

legend: list[StageInfo] = [
    # Receptions
    StageInfo(20001, "Zwei Crewmembers", 2, 3, [20002]),
    StageInfo(20002, "Zwei Association Ⅰ", 2, 3, [20003]),
    StageInfo(20003, "Zwei Association Ⅱ", 2, 3, [20004, 20005, 30002, 30003, 100009, 100010, 100014]),
    StageInfo(20004, "Molar Office", 2, 3, [30004, 100009, 100010, 100014]),
    StageInfo(20005, "Stray Dogs", 2, 3, [30001, 100009, 100010, 100014]),

    # General Receptions
    StageInfo(100004, "Grade 8 Fixers", 2, 3),
    StageInfo(100005, "Grade 7 Fixers", 2, 3),
    StageInfo(100006, "Urban Legend-class Office", 2, 3),
    StageInfo(100007, "Urban Legend-class Syndicate", 2, 3),
    StageInfo(100008, "Axe Gang", 2, 3),
]

plague: list[StageInfo] = [
    # Receptions
    StageInfo(30001, "The Carnival", 2, 4, [30006]),
    StageInfo(30002, "Full-Stop Office", 2, 4, [30007]),
    StageInfo(30003, "Dawn Office", 2, 4, [30008]),
    StageInfo(30004, "Gaze Office", 2, 4, [30005]),
    StageInfo(30005, "Tomerry", 3, 4, [40002, 100011, 100012]),
    StageInfo(30006, "Kurokumo Clan", 2, 4, [40004, 100011, 100012]),
    StageInfo(30007, "Musicians of Bremen", 2, 4, [40001, 100011, 100012]),
    StageInfo(30008, "Wedge Office", 3, 4, [40003, 100011, 100012]),

    # General Receptions
    StageInfo(100009, "Rusted Chains", 2, 4),
    StageInfo(100010, "Workshop-affiliated Fixers", 2, 4),
    StageInfo(100014, "Jeong’s Office", 2, 4),
]

nightmare: list[StageInfo] = [
    # Receptions
    StageInfo(40001, "Shi Association", 3, 5, [40007]),
    StageInfo(40002, "Puppets", 3, 5, [40006]),
    StageInfo(40003, "The 8 o’Clock Circus", 3, 5, [40008]),
    StageInfo(40004, "Sweepers", 3, 5, [40005]),
    StageInfo(40005, "Index Proselytes", 3, 5, [50003, 100013, 100015, 100016, 100017, 100018, 100019]),
    StageInfo(40006, "WARP Cleanup Crew", 3, 5, [50005, 100013, 100015, 100016, 100017, 100018, 100019]),
    StageInfo(40007, "Smiling Faces", 3, 5, [50006, 100013, 100015, 100016, 100017, 100018, 100019]),
    StageInfo(40008, "The Crying Children", 4, 5, [50001, 100013, 100015, 100016, 100017, 100018, 100019], librarians=2),
    
    # General Receptions
    StageInfo(100011, "Seven Association", 2, 5),
    StageInfo(100012, "Blade Lineage", 2, 5),
]

sotc: list[StageInfo] = [
    # Receptions
    StageInfo(50001, "Liu Association Section 2", 2, 6, [50002]),
    StageInfo(50002, "Liu Association Section 2 II", 2, 6, [50008]),
    StageInfo(50003, "The Thumb", 2, 6, [50004]),
    StageInfo(50004, "The Thumb II", 2, 6, [50007]),
    StageInfo(50005, "Cane Office", 3, 6, [50010]),
    StageInfo(50006, "The Blue Reverberation", 3, 6, [50009]),
    StageInfo(50007, "Index Proxies", 3, 6, [50014]),
    StageInfo(50008, "Liu Association Section 1", 3, 6, [50013]),
    StageInfo(50009, "The Red Mist", 4, 6, [50012]),
    StageInfo(50010, "R Corp.", 3, 6, [50011]),
    StageInfo(50011, "R Corp. II", 3, 6, [60001]),
    StageInfo(50012, "The Purple Tear", 3, 6, [60001]),
    StageInfo(50013, "Xiao", 4, 6, [60001]),
    StageInfo(50014, "얀샋ㄷ요무", 4, 6, [60001]),

    # General Receptions
    StageInfo(100013, "Dong-hwan the Grade 1 Fixer", 2, 6),
    StageInfo(100015, "Night Awls", 2, 6),
    StageInfo(100016, "The Udjat", 2, 6),
    StageInfo(100017, "Mirae Life Insurance", 2, 6),
    StageInfo(100018, "Leaflet Workshop", 2, 6),
    StageInfo(100019, "Bayard", 2, 6),
]

impurity: list[StageInfo] = [
    # Receptions
    StageInfo(60001, "Hana Association", 3, 7, [60002]),
    StageInfo(60002, "Oliver", 4, 7),
]

chapters: list[list[StageInfo]] = [
    canard,
    myth,
    legend,
    plague,
    nightmare,
    sotc,
    impurity
]


class FloorInfo:
    abnos: list[StageInfo]
    realization: StageInfo

    def __init__(self, abnos: list[StageInfo], realization: StageInfo):
        self.abnos = abnos
        self.realization = realization

malkuth = FloorInfo(
    [
        StageInfo(201001, "Scorched Girl", 3),
        StageInfo(201002, "Happy Teddy Bear", 3),
        StageInfo(201003, "Fairy Festival", 3),
        StageInfo(201004, "Queen Bee", 3)
    ],

    StageInfo(201005, "Malkuth Realization", 8)
)

yesod = FloorInfo(
    [
        StageInfo(202001, "Forsaken Murderer", 3),
        StageInfo(202002, "All-Around Helper", 3),
        StageInfo(202003, "Singing Machine", 3),
        StageInfo(202004, "The Funeral of the Dead Butterflies", 3)
    ],

    StageInfo(202005, "Yesod Realization", 8)
)

hod = FloorInfo(
    [
        StageInfo(203001, "Today’s Shy Look", 3),
        StageInfo(203002, "The Red Shoes", 3),
        StageInfo(203003, "Spider Bud", 3),
        StageInfo(203004, "Laetitia", 3, librarians=2)
    ],

    StageInfo(203005, "Hod Realization", 8)
)

netzach = FloorInfo(
    [
        StageInfo(204001, "Fragment of the Universe", 3),
        StageInfo(204002, "Child of the Galaxy", 3),
        StageInfo(204003, "Porccubus", 3),
        StageInfo(204004, "Alriune", 3)
    ],

    StageInfo(204005, "Netzach Realization", 8)
)

tiphereth = FloorInfo(
    [
        StageInfo(205001, "The Queen of Hatred", 3),
        StageInfo(205002, "The Knight of Despair", 3),
        StageInfo(205003, "The King of Greed", 3),
        StageInfo(205004, "The Servant of Wrath", 3)
    ],

    StageInfo(205005, "Tiphereth Realization", 8, librarians=4)
)

gebura = FloorInfo(
    [
        StageInfo(206001, "Little Red Riding Hooded Mercenary", 3),
        StageInfo(206002, "Big and Will be Bad Wolf", 3),
        StageInfo(206003, "Mountain of Smiling Bodies", 3),
        StageInfo(206004, "Nosferatu", 3)
    ],

    StageInfo(206005, "Gebura Realization", 8)
)

chesed = FloorInfo(
    [
        StageInfo(207001, "Scarecrow Searching for Wisdom", 3),
        StageInfo(207002, "Warm-hearted Woodsman", 3),
        StageInfo(207003, "The Road Home & Scaredy Cat", 3, librarians=2),
        StageInfo(207004, "Ozma", 3)
    ],

    StageInfo(207005, "Chesed Realization", 8, librarians=5)
)

binah = FloorInfo(
    [
        StageInfo(208001, "Big Bird", 3, librarians=2),
        StageInfo(208002, "Punishing Bird", 3),
        StageInfo(208003, "Judgement Bird", 3),
    ],

    StageInfo(208004, "Binah Realization", 11)
)

hokma = FloorInfo(
    [
        StageInfo(209001, "The Burrowing Heaven", 3),
        StageInfo(209002, "The Price of Silence", 3, librarians=2),
        StageInfo(209003, "Blue Star", 3),
    ],

    StageInfo(209004, "Hokma Realization", 11)
)

keter = FloorInfo(
    [
        StageInfo(210001, "Bloodbath", 3),
        StageInfo(210002, "Heart of Aspiration", 3),
        StageInfo(210003, "Pinocchio", 3),
        StageInfo(210004, "The Snow Queen", 3)
    ],

    StageInfo(210009, "Keter Realization", 8)
)

floors = [
    malkuth,
    yesod,
    hod,
    netzach,
    tiphereth,
    gebura,
    chesed,
    binah,
    hokma,
    keter
]



endgoals = [ # NO progression items
    StageInfo(70001, "[Ensemble] The Crying Children", 2),
    StageInfo(70002, "[Ensemble] The Church of Gears", 2),
    StageInfo(70003, "[Ensemble] The Eighth Chef", 2),
    StageInfo(70004, "[Ensemble] The Musicians of Bremen", 2),
    StageInfo(70005, "[Ensemble] The 8 o’Clock Circus", 2),
    StageInfo(70006, "[Ensemble] L’heure du Loup", 2),
    StageInfo(70007, "[Ensemble] The Puppeteer", 2),
    StageInfo(70008, "[Ensemble] The Blood-red Night", 2),
    StageInfo(70009, "[Ensemble] Yesterday’s Promise", 2),
    StageInfo(70010, "[Ensemble] The Blue Reverberation", 2),

    StageInfo(60003, "The Black Silence", 5),
    StageInfo(60004, "The Reverberation Ensemble Distorted", 5),
]


all_nodes = [
    # Every floors abno fight + realization
    *[l for sub in ([*floor.abnos, floor.realization] for floor in floors) for l in sub],

    # Every Reception
    *[r for sub in (chapter for chapter in chapters) for r in sub],

    # End Goals
    *endgoals
]


location_list: dict[str, int] = {}

for n in all_nodes:
    location_list.update(n.locations)






# This part is the randomization of suppressions
def randomize_suppresions(option: int, random: random.Random) -> list[FloorInfo]:
    result_floors = floors.copy()

    if option == 1:
        for f in result_floors:
            random.shuffle(f.abnos)
    elif option == 2 or option == 3:
        all_abnos = []
        for f in result_floors:
            all_abnos.extend(f.abnos)
        
        random.shuffle(all_abnos)

        for f in result_floors:
            total = len(f.abnos)
            f.abnos.clear()

            for i in range(total):
                f.abnos.append(all_abnos.pop(0))
            
        if option == 3:
            all_realizations = []
            for f in result_floors:
                all_realizations.append(f.realization)
            
            random.shuffle(all_realizations)

            for f in result_floors:
                f.realization = all_realizations.pop(0)

    return result_floors


# This part is the generation of the reception tree
class MapNode():
    id: int # Node's id
    receptions: list[StageInfo] # Receptions in this node
    prev: list['MapNode'] # Nodes that go after this one
    next: list['MapNode'] # Nodes that go before this one

    # Other stuff used for generation
    X: int # aka Column
    Y: int # aka Row / Depth

    def __init__(self, id: int, X: int = 0, Y: int = 0):
        self.id = id
        self.receptions = []
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

    def addreception(self, reception: StageInfo) -> 'MapNode':
        self.receptions.append(reception)

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


def generate_reception_tree(option: int, random: random.Random) -> list[MapNode]:
    if option == 2 or option == 3:
        return generate_random_tree(random)
    else:
        return generate_vanilla_tree()

def generate_vanilla_tree() -> list[MapNode]:
    # The tree created here is not 1:1 vanilla as i don't want to add more properties to recereate it 1:1,
    # but the connection order is still 1:1 behaviour (Some receptions like zwei aren't nested in single node)
    all_receptions: list[StageInfo] = [r for sub in (chapter for chapter in chapters) for r in sub]
    first = MapNode(0)
    first.addreception(canard[0])
    map: list[MapNode] = [first]
    next: list[MapNode] = [first]
    id = 1

    while len(next) != 0:
        cur: MapNode = next.pop(0)

        for i in cur.receptions[0].next:
            existing = [n for n in map if n.receptions[0].id == i]

            if len(existing) == 0:
                new = MapNode(id)
                id += 1
                new.addreception([r for r in all_receptions if r.id == i][0])
                new.addprev(cur)
                map.append(new)
                next.append(new)
            else:
                existing[0].addprev(cur)
    
    #for n in map:
    #    print("Node "+str(n.id)+" - Reception: "+str(n.receptions[0].id)+"; Next: "+", ".join([str(r.id) for r in n.next]))

    return map

def generate_random_tree(random: random.Random) -> list[MapNode]:
    print("------------[TREE GENERATION START]------------")
    print("------------[GENERATING BRANCHES]------------")
    # ---[STEP 1]---
    # Generate the branches. Main/Central branch is 30 in depth/height, everything to the left/right is -2 from previous
    # 1.1. Generate X = 0 branch (Central)
    id = 0
    map: list[MapNode] = []
    cur_x = 0
    cur_y = 0
    prev: MapNode = None
    height = 30
    for i in range(height):
        new = MapNode(id, cur_x, cur_y)
        id += 1
        cur_y += 1
        if prev != None:
            prev.addnext(new)
        prev = new
        map.append(new)

    # 1.2. Generate left/right branches
    while True:
        cur_x -= 1
        if height - 2 * -cur_x <= 0:
            break

        # To the left
        prev = None
        cur_y = -cur_x
        for i in range(height - 2 * -cur_x):
            new = MapNode(id, cur_x, cur_y)
            id += 1
            cur_y += 1
            if prev != None:
                prev.addnext(new)
            prev = new
            map.append(new)
        
        # To the right
        prev = None
        cur_x *= -1
        cur_y = cur_x
        for i in range(height - 2 * cur_x):
            new = MapNode(id, cur_x, cur_y)
            id += 1
            cur_y += 1
            if prev != None:
                prev.addnext(new)
            prev = new
            map.append(new)

        cur_x *= -1

    print("------------[GENERATING RANDOM CONNECTIONS]------------")
    # ---[STEP 2]---
    # Generate random connections
    for n in map:
        possible_nodes = [n1 for n1 in map if (n1.X == n.X - 1 or n1.X == n.X + 1) and n1.Y == n.Y + 1]

        for i in possible_nodes:
            if random.random() <= 0.20:
                n.addnext(i)


    print("------------[POPULATING]------------")
    # ---[STEP 3]---
    # Populate nodes (put receptions there)
    # 3.1. Put Rats as the first reception (forced)
    map[0].addreception(chapters[0].pop(0))

    # 3.2. Randomize all other receptions and put them in one list 
    all_stages: list[StageInfo] = []
    for i in chapters:
        random.shuffle(i)
        all_stages.extend(i)

    total = len(all_stages)
    print("TOTAL: "+str(total + 1))

    print("Put reception Rats in Node X: 0 Y: 0; Left: "+str(total))

    # 3.3. Walk through the tree and put receptions there
    queue: list[MapNode] = [map[0]]

    while len(queue) > 0:
        # Get current Node
        node = queue.pop(0)

        if len(all_stages) == 0:
            break

        # Put reception there
        if len(node.receptions) == 0:
            # If there is no receptions, put one there and repeat this node
            # Select a reception to be put on map
            i = 0
            while i < len(all_stages)-1 and random.random() >= 0.5:
                i += 1

            reception = all_stages.pop(i)

            node.addreception(reception)
            queue.append(node)
            print("Put reception "+reception.name+" in Node X: "+str(node.X)+" Y: "+str(node.Y)+"; Left: "+str(len(all_stages)))
        elif len(node.receptions) < 3 and random.random() <= 0.20:
            # If there is a reception already, not more than 3, and chance procs, put another there
            # Select a reception to be put on map
            i = 0
            while i < len(all_stages)-1 and random.random() >= 0.5:
                i += 1

            reception = all_stages.pop(i)

            node.addreception(reception)
            queue.append(node)
            print("Put reception "+reception.name+" in Node X: "+str(node.X)+" Y: "+str(node.Y)+"; Left: "+str(len(all_stages)))
        else:
            # Else simply go to next nodes
            for n in node.next:
                queue.append(n)

    # 3.4. Extension in case of not enough nodes?

        
    print("------------[CLEANING]------------")
    # ---[STEP 4]---
    # Remove garbage and stuff
    # 4.1. Remove every node without a reception
    for n in map.copy():
        if len(n.receptions) == 0:
            for i in n.prev:
                i.next.remove(n)

            for i in n.next:
                i.prev.remove(n)
            
            map.remove(n)

    # 4.2. Set IDs of nodes again, so it's not spaced out and takes less bits in final representation
    id = 0
    for n in map:
        n.id = id
        id += 1

    print("IDs after cleaning: "+str(id))

    # 4.2. Divide the tree into fake chapters that will be spheres
    maxY = max(map, key=lambda n: n.Y).Y
    chapterY = maxY / 7
    for n in map:
        for r in n.receptions:
            r.chapter = 1 + n.Y // chapterY

    print("------------[END]------------")

    return map