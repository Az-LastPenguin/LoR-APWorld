from BaseClasses import Location

class LORLocation(Location):
    game: str = "Library of Ruina"


class Node:
    id: int
    name: str
    checks: int

    def __init__(self, id: int, name: str, checks: int):
        self.id = id
        self.name = name
        self.checks = checks

class ChapterModel:
    prev: 'ChapterModel'
    next: 'ChapterModel'

    receptions: list[Node]

    def __init__(self, *args):
        self.receptions = []
        for i in args:
            self.receptions.append(i)

    def chain(self, next: 'ChapterModel'):
        self.next = next
        next.prev = self

class FloorAbnoModel:
    abnos: list[Node]
    realization: Node

    def __init__(self, realization: Node, *args):
        self.realization = realization
        self.abnos = []
        for i in args:
            self.abnos.append(i)

canard = ChapterModel(
    # Receptions
    Node(2, "Rats", 2),
    Node(5, "Yun's Office", 2),
    Node(6, "Brotherhood of Iron", 2),
    Node(7, "Hook Office", 2),
)

myth = ChapterModel(
    # Receptions
    Node(10001, "Pierre's Bistro", 2),
    Node(10003, "Streetlight Office", 2),

    # General Receptions
    Node(100003, "Urban Myth-class Syndicate", 2),
    Node(100002, "Hook Office Remnants", 2),
    Node(100001, "Backstreets Butchers", 2),
)

legend = ChapterModel(
    # Receptions
    Node(20005, "Stray Dogs", 2),
    Node(20003, "Zwei Office", 3),
    Node(20004, "Molar Office", 2),

    # General Receptions
    Node(100004, "Grade 8 Fixers", 2),
    Node(100005, "Grade 7 Fixers", 2),
    Node(100006, "Urban Legend-class Office", 2),
    Node(100007, "Urban Legend-class Syndicate", 2),
    Node(100008, "Axe Gang", 2),
)

plague = ChapterModel(
    # Receptions
    Node(30001, "The Carnival", 2),
    Node(30002, "Full-Stop Office", 2),
    Node(30003, "Dawn Office", 2),
    Node(30004, "Gaze Office", 2),
    Node(30005, "Tomerry", 3),
    Node(30006, "Kurokumo Clan", 2),
    Node(30007, "Musicians of Bremen", 2),
    Node(30008, "Wedge Office", 3),

    # General Receptions
    Node(100009, "Rusted Chains", 2),
    Node(100010, "Workshop-affiliated Fixers", 2),
    Node(100014, "Jeong’s Office", 2),
)

nightmare = ChapterModel(
    # Receptions
    Node(40001, "Shi Association", 3),
    Node(40002, "Puppets", 3),
    Node(40003, "The 8 o’Clock Circus", 3),
    Node(40004, "Sweepers", 3),
    Node(40005, "Index Proselytes", 3),
    Node(40006, "WARP Cleanup Crew", 3),
    Node(40007, "Smiling Faces", 3),
    Node(40008, "The Crying Children", 4),
    
    # General Receptions
    Node(100011, "Seven Association", 2),
    Node(100012, "Blade Lineage", 2),
)

sotc = ChapterModel(
    # Receptions
    Node(50002, "Liu Association Section 2", 3),
    Node(50004, "The Thumb", 3),
    Node(50005, "Cane Office", 3),
    Node(50006, "The Blue Reverberation", 3),
    Node(50007, "Index Proxies", 3),
    Node(50008, "Liu Association Section 1", 3),
    Node(50009, "The Red Mist", 4),
    Node(50010, "R Corp.", 3),
    Node(50011, "R Corp. II", 3),
    Node(50012, "The Purple Tear", 3),
    Node(50013, "Xiao", 4),
    Node(50014, "얀샋ㄷ요무", 4),

    # General Receptions
    Node(100013, "Dong-hwan the Grade 1 Fixer", 2),
    Node(100015, "Night Awls", 2),
    Node(100016, "The Udjat", 2),
    Node(100017, "Mirae Life Insurance", 2),
    Node(100018, "Leaflet Workshop", 2),
    Node(100019, "Bayard", 2),
)

impurity = ChapterModel(
    # Receptions
    Node(60002, "Oliver", 5),
)

chapter_models = [
    canard,
    myth,
    legend,
    plague,
    nightmare,
    sotc,
    impurity
]



malkuth = FloorAbnoModel(
    Node(201005, "Floor of Technological Sciences Realization", 8),

    Node(201001, "Scorched Girl", 3),
    Node(201002, "Happy Teddy Bear", 3),
    Node(201003, "Fairy Festival", 3),
    Node(201004, "Queen Bee", 3)
)

yesod = FloorAbnoModel(
    Node(202005, "Floor of History Realization", 8),

    Node(202001, "Forsaken Murderer", 3),
    Node(202002, "All-Around Helper", 3),
    Node(202003, "Singing Machine", 3),
    Node(202004, "The Funeral of the Dead Butterflies", 3)
)

hod = FloorAbnoModel(
    Node(203005, "Floor of Literature Realization", 8),

    Node(203001, "Today’s Shy Look", 3),
    Node(203002, "The Red Shoes", 3),
    Node(203003, "Spider Bud", 3),
    Node(203004, "Laetitia", 3)
)

netzach = FloorAbnoModel(
    Node(204005, "Floor of Art Realization", 8),

    Node(204001, "Fragment of the Universe", 3),
    Node(204002, "Child of the Galaxy", 3),
    Node(204003, "Porccubus", 3),
    Node(204004, "Alriune", 3)
)

tiphereth = FloorAbnoModel(
    Node(205005, "Floor of Natural Sciences Realization", 8),

    Node(205001, "The Queen of Hatred", 3),
    Node(205002, "The Knight of Despair", 3),
    Node(205003, "The King of Greed", 3),
    Node(205004, "The Servant of Wrath", 3)
)

gebura = FloorAbnoModel(
    Node(206005, "Floor of Language Realization", 8),

    Node(206001, "Little Red Riding Hooded Mercenary", 3),
    Node(206002, "Big and Will be Bad Wolf", 3),
    Node(206003, "Mountain of Smiling Bodies", 3),
    Node(206004, "Nosferatu", 3)
)

chesed = FloorAbnoModel(
    Node(207005, "Floor of Social Sciences Realization", 8),

    Node(207001, "Scarecrow Searching for Wisdom", 3),
    Node(207002, "Warm-hearted Woodsman", 3),
    Node(207003, "The Road Home & Scaredy Cat", 3),
    Node(207004, "Ozma", 3)
)

binah = FloorAbnoModel(
    Node(208004, "Floor of Philosophy Realization", 11),

    Node(208001, "Big Bird", 3),
    Node(208002, "Punishing Bird", 3),
    Node(208003, "Judgement Bird", 3),
)

hokma = FloorAbnoModel(
    Node(209004, "Floor of Religion Realization", 11),

    Node(209001, "The Burrowing Heaven", 3),
    Node(209002, "The Price of Silence", 3),
    Node(209003, "Blue Star", 3),
)

keter = FloorAbnoModel(
    Node(210009, "Floor of General Works Realization", 8),

    Node(210001, "Bloodbath", 3),
    Node(210002, "Heart of Aspiration", 3),
    Node(210003, "Pinocchio", 3),
    Node(210004, "The Snow Queen", 3)
)

floor_models = [
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
    Node(70001, "[Ensemble] The Crying Children", 2),
    Node(70002, "[Ensemble] The Church of Gears", 2),
    Node(70003, "[Ensemble] The Eighth Chef", 2),
    Node(70004, "[Ensemble] The Musicians of Bremen", 2),
    Node(70005, "[Ensemble] The 8 o’Clock Circus", 2),
    Node(70006, "[Ensemble] L’heure du Loup", 2),
    Node(70007, "[Ensemble] The Puppeteer", 2),
    Node(70008, "[Ensemble] The Blood-red Night", 2),
    Node(70009, "[Ensemble] Yesterday’s Promise", 2),
    Node(70010, "[Ensemble] The Blue Reverberation", 2),

    Node(60003, "The Black Silence", 5),
    Node(60004, "The Reverberation Ensemble Distorted", 5),
]


all_nodes = [
    # Every floors abno fight + realization
    *[l for sub in ([*floor.abnos, floor.realization] for floor in floor_models) for l in sub],

    # Every Reception
    *[l for sub in (chapter.receptions for chapter in chapter_models) for l in sub],

    # End Goals
    *endgoals
]



all_locations: dict[str, int] = {}

for l in all_nodes:
    for i in range(l.checks):
        all_locations[l.name+" ("+str(i+1)+")"] = l.id | (i << 18)