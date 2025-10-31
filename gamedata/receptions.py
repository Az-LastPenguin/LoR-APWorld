from dataclasses import dataclass, field

# ReceptionNode is used to store info about a reception (it's id, name, amount of checks, next reception required books and librians).
# reception_nodes list contains all vanilla receptions in their original order

@dataclass
class ReceptionNode:
    id: int # in-game reception id
    name: str # in-game name of the reception (will be used for location names)
    checks: int # amount of checks this reception will yield
    next: list[int] # ids of next receptions
    req_books: list[int] = field(default_factory=list) # ids of books this reception requires (only set during generation)
    req_librarians: int = 1 # minimum amount of librarians in any floor required to consider reception completable

reception_nodes: list[ReceptionNode] = [
    # Canard
    ReceptionNode(id=2, name="Rats", checks=2, next=[3]),
    ReceptionNode(id=3, name="Yun's Office Fixers", checks=2, next=[4]),
    ReceptionNode(id=4, name="Yun's Office Rookie", checks=2, next=[5]),
    ReceptionNode(id=5, name="Yun's Office", checks=3, next=[6]),
    ReceptionNode(id=6, name="Brotherhood of Iron", checks=5, next=[7]),
    ReceptionNode(id=7, name="Hook Office", checks=5, next=[10001, 100001, 100002, 100003]),

    # Urban Myth
    ReceptionNode(id=10001, name="Pierre's Bistro", checks=2, next=[10002]),
    ReceptionNode(id=10002, name="Streetlight Office", checks=2, next=[10003]),
    ReceptionNode(id=10003, name="Lulu of Streetlight", checks=2, next=[20001, 100004, 100005, 100006, 100007, 100008]),

    ReceptionNode(id=100001, name="Backstreets Butchers", checks=2, next=[]),
    ReceptionNode(id=100002, name="Hook Office Remnants", checks=2, next=[]),
    ReceptionNode(id=100003, name="Urban Myth-class Syndicate", checks=2, next=[]),

    # Urban Legend
    ReceptionNode(id=20001, name="Zwei Crewmembers", checks=4, next=[20002]),
    ReceptionNode(id=20002, name="Zwei Association I", checks=5, next=[20003]),
    ReceptionNode(id=20003, name="Zwei Association II", checks=5, next=[20004, 20005, 30002, 30003, 100009, 100010, 100014]),
    ReceptionNode(id=20004, name="Molar Office", checks=6, next=[30004, 100009, 100010, 100014]),
    ReceptionNode(id=20005, name="Stray Dogs", checks=6, next=[30001, 100009, 100010, 100014]),

    ReceptionNode(id=100004, name="Grade 8 Fixers", checks=4, next=[]),
    ReceptionNode(id=100005, name="Grade 7 Fixers", checks=4, next=[]),
    ReceptionNode(id=100006, name="Urban Legend-class Office", checks=4, next=[]),
    ReceptionNode(id=100007, name="Urban Legend-class Syndicate", checks=4, next=[]),
    ReceptionNode(id=100008, name="Axe Gang", checks=4, next=[]),

    # Urban Plague
    ReceptionNode(id=30001, name="The Carnival", checks=5, next=[30006]),
    ReceptionNode(id=30002, name="Full-Stop Office", checks=5, next=[30007]),
    ReceptionNode(id=30003, name="Dawn Office", checks=5, next=[30008]),
    ReceptionNode(id=30004, name="Gaze Office", checks=5, next=[30005]),
    ReceptionNode(id=30005, name="Tomerry", checks=7, next=[40002, 100011, 100012]),
    ReceptionNode(id=30006, name="Kurokumo Clan", checks=6, next=[40004, 100011, 100012]),
    ReceptionNode(id=30007, name="Musicians of Bremen", checks=6, next=[40001, 100011, 100012]),
    ReceptionNode(id=30008, name="Wedge Office", checks=6, next=[40003, 100011, 100012]),

    ReceptionNode(id=100009, name="Rusted Chains", checks=5, next=[]),
    ReceptionNode(id=100010, name="Workshop-affiliated Fixers", checks=5, next=[]),
    ReceptionNode(id=100014, name="Jeong's Office", checks=5, next=[]),

    # Urban Nightmare
    ReceptionNode(id=40001, name="Shi Association", checks=5, next=[40007]),
    ReceptionNode(id=40002, name="Puppets", checks=5, next=[40006]),
    ReceptionNode(id=40003, name="The 8 o'Clock Circus", checks=5, next=[40008]),
    ReceptionNode(id=40004, name="Sweepers", checks=5, next=[40005]),
    ReceptionNode(id=40005, name="Index Proselytes", checks=6, next=[50003, 100013, 100015, 100016, 100017, 100018, 100019]),
    ReceptionNode(id=40006, name="WARP Cleanup Crew", checks=6, next=[50005, 100013, 100015, 100016, 100017, 100018, 100019]),
    ReceptionNode(id=40007, name="Smiling Faces", checks=6, next=[50006, 100013, 100015, 100016, 100017, 100018, 100019]),
    ReceptionNode(id=40008, name="The Crying Children", checks=8, next=[50001, 100013, 100015, 100016, 100017, 100018, 100019], req_librarians=2),

    ReceptionNode(id=100011, name="Seven Association", checks=5, next=[]),
    ReceptionNode(id=100012, name="Blade Lineage", checks=5, next=[]),

    # Star of the City
    ReceptionNode(id=50001, name="Liu Association Section 2", checks=5, next=[50002]),
    ReceptionNode(id=50002, name="Liu Association Section 2 II", checks=5, next=[50008]),
    ReceptionNode(id=50003, name="The Thumb", checks=5, next=[50004]),
    ReceptionNode(id=50004, name="The Thumb II", checks=5, next=[50007]),
    ReceptionNode(id=50005, name="Cane Office", checks=5, next=[50010]),
    ReceptionNode(id=50006, name="The Blue Reverberation", checks=5, next=[50009]),
    ReceptionNode(id=50007, name="Index Proxies", checks=6, next=[50014]),
    ReceptionNode(id=50008, name="Liu Association Section 1", checks=6, next=[50013]),
    ReceptionNode(id=50009, name="The Red Mist", checks=8, next=[50012]),
    ReceptionNode(id=50010, name="R Corp.", checks=6, next=[50011]),
    ReceptionNode(id=50011, name="R Corp. II", checks=6, next=[60001]),
    ReceptionNode(id=50012, name="The Purple Tear", checks=8, next=[60001]),
    ReceptionNode(id=50013, name="Xiao", checks=9, next=[60001]),
    ReceptionNode(id=50014, name="얀샋ㄷ요무", checks=9, next=[60001]),

    ReceptionNode(id=100013, name="Dong-hwan the Grade 1 Fixer", checks=5, next=[]),
    ReceptionNode(id=100015, name="Night Awls", checks=5, next=[]),
    ReceptionNode(id=100016, name="The Udjat", checks=5, next=[]),
    ReceptionNode(id=100017, name="Mirae Life Insurance", checks=5, next=[]),
    ReceptionNode(id=100018, name="Leaflet Workshop", checks=5, next=[]),
    ReceptionNode(id=100019, name="Bayard", checks=5, next=[]),
    
    # Impurity
    ReceptionNode(id=60001, name="Hana Association", checks=6, next=[60002]),
    ReceptionNode(id=60002, name="Oliver", checks=6, next=[]),
]

endgoal_receptions: list[ReceptionNode] = [
    # Ensemble
    ReceptionNode(id=70001, name="[Ensemble] The Crying Children", checks=5, next=[]),
    ReceptionNode(id=70002, name="[Ensemble] The Church of Gears", checks=5, next=[]),
    ReceptionNode(id=70003, name="[Ensemble] The Eighth Chef", checks=5, next=[]),
    ReceptionNode(id=70004, name="[Ensemble] The Musicians of Bremen", checks=5, next=[]),
    ReceptionNode(id=70005, name="[Ensemble] The 8 o'Clock Circus", checks=5, next=[]),
    ReceptionNode(id=70006, name="[Ensemble] L'heure du Loup", checks=5, next=[]),
    ReceptionNode(id=70007, name="[Ensemble] The Puppeteer", checks=5, next=[]),
    ReceptionNode(id=70008, name="[Ensemble] The Blood-red Night", checks=5, next=[]),
    ReceptionNode(id=70009, name="[Ensemble] Yesterday's Promise", checks=5, next=[]),
    ReceptionNode(id=70010, name="[Ensemble] The Blue Reverberation", checks=5, next=[]),

    # Black Silence
    ReceptionNode(id=60003, name="The Black Silence", checks=10, next=[]),

    ReceptionNode(id=60004, name="The Reverberation Ensemble Distorted", checks=10, next=[]),
]


receptions_by_name: dict[str, ReceptionNode] = {reception.name: reception for reception in [*reception_nodes, *endgoal_receptions]}
receptions_dict: dict[int, ReceptionNode] = {reception.id: reception for reception in [*reception_nodes, *endgoal_receptions]}