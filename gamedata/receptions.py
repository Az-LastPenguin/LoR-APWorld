from dataclasses import dataclass, field

# ReceptionInfo is used to store vanilla reception information.
# ReceptionGroupInfo is used to store reception group information. (Vanilla or not, used in run generation)

@dataclass
class ReceptionGroupInfo:
    id: int # custom id used specifically in this randomizer
    chapter: int # in-game chapter this ReceptionGroup is in 
    prev_groups: list[int] # ids of the previous ReceptionGroups
    next_groups: list[int] # ids of the next ReceptionGroups
    receptions: list[int] # ids of Receptions in this ReceptionGroup

@dataclass
class ReceptionInfo:
    id: int # in-game reception id
    chapter: int # in-game chapter this Reception is in
    name: str # name of the reception (will be used for location names)
    checks: int # amount of checks this reception will yield as a location
    req_books: list[int] = field(default_factory=list) # ids of books this reception requires (only set during generation)
    req_librarians: int = 1 # amount of librarians in any floor required to consider reception completable

# make those specifically vanilla groups
vanilla_reception_groups: list[ReceptionGroupInfo] = [
    # Chapter 1 [Canard]
    ReceptionGroupInfo(id=1, chapter=1, prev_groups=[ ], next_groups=[2], receptions=[2]),
    ReceptionGroupInfo(id=2, chapter=1, prev_groups=[1], next_groups=[3], receptions=[3, 4, 5]),
    ReceptionGroupInfo(id=3, chapter=1, prev_groups=[2], next_groups=[4], receptions=[6]),
    ReceptionGroupInfo(id=4, chapter=1, prev_groups=[3], next_groups=[5,  7, 8, 9], receptions=[7]),


    # Chapter 2 [Urban Myth] (Main)
    ReceptionGroupInfo(id=5, chapter=2, prev_groups=[4], next_groups=[6], receptions=[10001]),
    ReceptionGroupInfo(id=6, chapter=2, prev_groups=[5], next_groups=[10,  13, 14, 15, 16, 17], receptions=[10002, 10003]),

    # Chapter 2 [Urban Myth] (General)
    ReceptionGroupInfo(id=7, chapter=2, prev_groups=[4], next_groups=[ ], receptions=[100001]),
    ReceptionGroupInfo(id=8, chapter=2, prev_groups=[4], next_groups=[ ], receptions=[100002]),
    ReceptionGroupInfo(id=9, chapter=2, prev_groups=[4], next_groups=[ ], receptions=[100003]),


    # Chapter 3 [Urban Legend] (Main)
    ReceptionGroupInfo(id=10, chapter=3, prev_groups=[6], next_groups=[11, 12,  19, 20,  26, 27, 28], receptions=[20001, 20002, 20003]),
    ReceptionGroupInfo(id=11, chapter=3, prev_groups=[10], next_groups=[21,  26, 27, 28], receptions=[20004]),
    ReceptionGroupInfo(id=12, chapter=3, prev_groups=[10], next_groups=[18,  26, 27, 28], receptions=[20005]),

    # Chapter 3 [Urban Legend] (General)
    ReceptionGroupInfo(id=13, chapter=3, prev_groups=[6], next_groups=[ ], receptions=[100004]),
    ReceptionGroupInfo(id=14, chapter=3, prev_groups=[6], next_groups=[ ], receptions=[100005]),
    ReceptionGroupInfo(id=15, chapter=3, prev_groups=[6], next_groups=[ ], receptions=[100006]),
    ReceptionGroupInfo(id=16, chapter=3, prev_groups=[6], next_groups=[ ], receptions=[100007]),
    ReceptionGroupInfo(id=17, chapter=3, prev_groups=[6], next_groups=[ ], receptions=[100008]),


    # Chapter 4 [Urban Plague] (Main)
    ReceptionGroupInfo(id=18, chapter=4, prev_groups=[12], next_groups=[22], receptions=[30001]),
    ReceptionGroupInfo(id=19, chapter=4, prev_groups=[10], next_groups=[23], receptions=[30002]),
    ReceptionGroupInfo(id=20, chapter=4, prev_groups=[10], next_groups=[24], receptions=[30003]),
    ReceptionGroupInfo(id=21, chapter=4, prev_groups=[11], next_groups=[25], receptions=[30004]),

    ReceptionGroupInfo(id=22, chapter=4, prev_groups=[18], next_groups=[29,  37, 38], receptions=[30006]),
    ReceptionGroupInfo(id=23, chapter=4, prev_groups=[19], next_groups=[30,  37, 38], receptions=[30007]),
    ReceptionGroupInfo(id=24, chapter=4, prev_groups=[20], next_groups=[31,  37, 38], receptions=[30008]),
    ReceptionGroupInfo(id=25, chapter=4, prev_groups=[21], next_groups=[32,  37, 38], receptions=[30005]),

    # Chapter 4 [Urban Plague] (General)
    ReceptionGroupInfo(id=26, chapter=4, prev_groups=[10, 11, 12], next_groups=[ ], receptions=[100009]),
    ReceptionGroupInfo(id=27, chapter=4, prev_groups=[10, 11, 12], next_groups=[ ], receptions=[100010]),
    ReceptionGroupInfo(id=28, chapter=4, prev_groups=[10, 11, 12], next_groups=[ ], receptions=[100014]),

    
    # Chaper 5 [Urban Nightmare] (Main)
    ReceptionGroupInfo(id=29, chapter=5, prev_groups=[22], next_groups=[33], receptions=[40004]),
    ReceptionGroupInfo(id=30, chapter=5, prev_groups=[23], next_groups=[34], receptions=[40001]),
    ReceptionGroupInfo(id=31, chapter=5, prev_groups=[24], next_groups=[35], receptions=[40003]),
    ReceptionGroupInfo(id=32, chapter=5, prev_groups=[25], next_groups=[36], receptions=[40002]),

    ReceptionGroupInfo(id=33, chapter=5, prev_groups=[29], next_groups=[39,  51, 52, 53, 54, 55, 56], receptions=[40005]),
    ReceptionGroupInfo(id=34, chapter=5, prev_groups=[30], next_groups=[40,  51, 52, 53, 54, 55, 56], receptions=[40007]),
    ReceptionGroupInfo(id=35, chapter=5, prev_groups=[31], next_groups=[41,  51, 52, 53, 54, 55, 56], receptions=[40008]),
    ReceptionGroupInfo(id=36, chapter=5, prev_groups=[32], next_groups=[42,  51, 52, 53, 54, 55, 56], receptions=[40006]),

    # Chapter 5 [Urban Nightmare] (General)
    ReceptionGroupInfo(id=37, chapter=5, prev_groups=[22, 23, 24, 25], next_groups=[ ], receptions=[100011]),
    ReceptionGroupInfo(id=38, chapter=5, prev_groups=[22, 23, 24, 25], next_groups=[ ], receptions=[100012]),
    

    # Chapter 6 [Star of the City] (Main)
    ReceptionGroupInfo(id=39, chapter=6, prev_groups=[33], next_groups=[43], receptions=[50003, 50004]),
    ReceptionGroupInfo(id=40, chapter=6, prev_groups=[34], next_groups=[44], receptions=[50006]),
    ReceptionGroupInfo(id=41, chapter=6, prev_groups=[35], next_groups=[45], receptions=[50001, 50002]),
    ReceptionGroupInfo(id=42, chapter=6, prev_groups=[36], next_groups=[46], receptions=[50005]),

    ReceptionGroupInfo(id=43, chapter=6, prev_groups=[39], next_groups=[47], receptions=[50007]),
    ReceptionGroupInfo(id=44, chapter=6, prev_groups=[40], next_groups=[48], receptions=[50009]),
    ReceptionGroupInfo(id=45, chapter=6, prev_groups=[41], next_groups=[49], receptions=[50008]),
    ReceptionGroupInfo(id=46, chapter=6, prev_groups=[42], next_groups=[50], receptions=[50010]),

    ReceptionGroupInfo(id=47, chapter=6, prev_groups=[43], next_groups=[57], receptions=[50014]),
    ReceptionGroupInfo(id=48, chapter=6, prev_groups=[44], next_groups=[57], receptions=[50012]),
    ReceptionGroupInfo(id=49, chapter=6, prev_groups=[45], next_groups=[57], receptions=[50013]),
    ReceptionGroupInfo(id=50, chapter=6, prev_groups=[46], next_groups=[57], receptions=[50011]),

    # Chapter 6 [Star of the City] (General)
    ReceptionGroupInfo(id=51, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100013]),
    ReceptionGroupInfo(id=52, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100015]),
    ReceptionGroupInfo(id=53, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100016]),
    ReceptionGroupInfo(id=54, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100017]),
    ReceptionGroupInfo(id=55, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100018]),
    ReceptionGroupInfo(id=56, chapter=6, prev_groups=[33, 34, 35, 36], next_groups=[ ], receptions=[100019]),


    # Chapter 7 [Impurity] (next group 999 is a hacky thing i decided to use to mark last reception in the tree)
    ReceptionGroupInfo(id=57, chapter=7, prev_groups=[47, 48, 49, 50], next_groups=[999], receptions=[60001, 60002]),


    # Endgoal Receptions (Chapter 8 is a fake chapter to simplyfy work with randomization)
    ReceptionGroupInfo(id=100, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70001]),
    ReceptionGroupInfo(id=101, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70002]),
    ReceptionGroupInfo(id=102, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70003]),
    ReceptionGroupInfo(id=103, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70004]),
    ReceptionGroupInfo(id=104, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70005]),
    ReceptionGroupInfo(id=105, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70006]),
    ReceptionGroupInfo(id=106, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70007]),
    ReceptionGroupInfo(id=107, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70008]),
    ReceptionGroupInfo(id=108, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70009]),
    ReceptionGroupInfo(id=109, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[70010]),

    ReceptionGroupInfo(id=110, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[60003]),
 
    ReceptionGroupInfo(id=111, chapter=8, prev_groups=[ ], next_groups=[ ], receptions=[60004]),
]


receptions: list[ReceptionInfo] = [
    # Chapter 1 [Canard]
    ReceptionInfo(id=2, chapter=1, name="Rats", checks=2),

    ReceptionInfo(id=3, chapter=1, name="Yun's Office Fixers", checks=2),
    ReceptionInfo(id=4, chapter=1, name="Yun's Office Rookie", checks=2),
    ReceptionInfo(id=5, chapter=1, name="Yun's Office", checks=3),

    ReceptionInfo(id=6, chapter=1, name="Brotherhood of Iron", checks=5),
    ReceptionInfo(id=7, chapter=1, name="Hook Office", checks=5),


    # Chapter 2 [Urban Myth] (Main)
    ReceptionInfo(id=10001, chapter=2, name="Pierre's Bistro", checks=4),

    ReceptionInfo(id=10002, chapter=2, name="Streetlight Office", checks=3),
    ReceptionInfo(id=10003, chapter=2, name="Lulu of Streetlight", checks=5),

    # Chapter 2 [Urban Myth] (General)
    ReceptionInfo(id=100001, chapter=2, name="Backstreets Butchers", checks=3),
    ReceptionInfo(id=100002, chapter=2, name="Hook Office Remnants", checks=3),
    ReceptionInfo(id=100003, chapter=2, name="Urban Myth-class Syndicate", checks=3),

    
    # Chapter 3 [Urban Legend] (Main)
    ReceptionInfo(id=20001, chapter=3, name="Zwei Crewmembers", checks=4),
    ReceptionInfo(id=20002, chapter=3, name="Zwei Association I", checks=5),
    ReceptionInfo(id=20003, chapter=3, name="Zwei Association II", checks=5),

    ReceptionInfo(id=20004, chapter=3, name="Molar Office", checks=6),

    ReceptionInfo(id=20005, chapter=3, name="Stray Dogs", checks=6),

    # Chapter 3 [Urban Legend] (General)
    ReceptionInfo(id=100004, chapter=3, name="Grade 8 Fixers", checks=4),
    ReceptionInfo(id=100005, chapter=3, name="Grade 7 Fixers", checks=4),
    ReceptionInfo(id=100006, chapter=3, name="Urban Legend-class Office", checks=4),
    ReceptionInfo(id=100007, chapter=3, name="Urban Legend-class Syndicate", checks=4),
    ReceptionInfo(id=100008, chapter=3, name="Axe Gang", checks=4),


    # Chapter 4 [Urban Plague] (Main)
    ReceptionInfo(id=30001, chapter=4, name="The Carnival", checks=5),

    ReceptionInfo(id=30002, chapter=4, name="Full-Stop Office", checks=5),

    ReceptionInfo(id=30003, chapter=4, name="Dawn Office", checks=5),

    ReceptionInfo(id=30004, chapter=4, name="Gaze Office", checks=5),

    ReceptionInfo(id=30005, chapter=4, name="Tomerry", checks=7),

    ReceptionInfo(id=30006, chapter=4, name="Kurokumo Clan", checks=6),

    ReceptionInfo(id=30007, chapter=4, name="Musicians of Bremen", checks=6),

    ReceptionInfo(id=30008, chapter=4, name="Wedge Office", checks=6),

    # Chapter 4 [Urban Plague] (General)
    ReceptionInfo(id=100009, chapter=4, name="Rusted Chains", checks=5),
    ReceptionInfo(id=100010, chapter=4, name="Workshop-affiliated Fixers", checks=5),
    ReceptionInfo(id=100014, chapter=4, name="Jeong's Office", checks=5),


    # Chapter 5 [Urban Nightmare] (Main)
    ReceptionInfo(id=40001, chapter=5, name="Shi Association", checks=5),

    ReceptionInfo(id=40002, chapter=5, name="Puppets", checks=5),

    ReceptionInfo(id=40003, chapter=5, name="The 8 o'Clock Circus", checks=5),

    ReceptionInfo(id=40004, chapter=5, name="Sweepers", checks=5),

    ReceptionInfo(id=40005, chapter=5, name="Index Proselytes", checks=6),

    ReceptionInfo(id=40006, chapter=5, name="WARP Cleanup Crew", checks=6),

    ReceptionInfo(id=40007, chapter=5, name="Smiling Faces", checks=6),

    ReceptionInfo(id=40008, chapter=5, name="The Crying Children", checks=8, req_librarians=2),

    # Chapter 5 [Urban Nightmare] (General)
    ReceptionInfo(id=100011, chapter=5, name="Seven Association", checks=5),
    ReceptionInfo(id=100012, chapter=5, name="Blade Lineage", checks=5),


    # Chapter 6 [Star of the City] (Main)
    ReceptionInfo(id=50001, chapter=6, name="Liu Association Section 2", checks=5),
    ReceptionInfo(id=50002, chapter=6, name="Liu Association Section 2 II", checks=5),

    ReceptionInfo(id=50003, chapter=6, name="The Thumb", checks=5),
    ReceptionInfo(id=50004, chapter=6, name="The Thumb II", checks=5),

    ReceptionInfo(id=50005, chapter=6, name="Cane Office", checks=5),
    
    ReceptionInfo(id=50006, chapter=6, name="The Blue Reverberation", checks=5),

    ReceptionInfo(id=50007, chapter=6, name="Index Proxies", checks=6),

    ReceptionInfo(id=50008, chapter=6, name="Liu Association Section 1", checks=6),

    ReceptionInfo(id=50009, chapter=6, name="The Red Mist", checks=8),

    ReceptionInfo(id=50010, chapter=6, name="R Corp.", checks=6),

    ReceptionInfo(id=50011, chapter=6, name="R Corp. II", checks=6),

    ReceptionInfo(id=50012, chapter=6, name="The Purple Tear", checks=8),

    ReceptionInfo(id=50013, chapter=6, name="Xiao", checks=9),

    ReceptionInfo(id=50014, chapter=6, name="얀샋ㄷ요무", checks=9),

    # Chapter 6 [Star of the City] (General)
    ReceptionInfo(id=100013, chapter=6, name="Dong-hwan the Grade 1 Fixer", checks=5),
    ReceptionInfo(id=100015, chapter=6, name="Night Awls", checks=5),
    ReceptionInfo(id=100016, chapter=6, name="The Udjat", checks=5),
    ReceptionInfo(id=100017, chapter=6, name="Mirae Life Insurance", checks=5),
    ReceptionInfo(id=100018, chapter=6, name="Leaflet Workshop", checks=5),
    ReceptionInfo(id=100019, chapter=6, name="Bayard", checks=5),


    # Chapter 7 [Impurity]
    ReceptionInfo(id=60001, chapter=7, name="Hana Association", checks=6),
    ReceptionInfo(id=60002, chapter=7, name="Oliver", checks=6),


    # Endgoal Receptions
    ReceptionInfo(id=70001, chapter=8, name="[Ensemble] The Crying Children", checks=5),
    ReceptionInfo(id=70002, chapter=8, name="[Ensemble] The Church of Gears", checks=5),
    ReceptionInfo(id=70003, chapter=8, name="[Ensemble] The Eighth Chef", checks=5),
    ReceptionInfo(id=70004, chapter=8, name="[Ensemble] The Musicians of Bremen", checks=5),
    ReceptionInfo(id=70005, chapter=8, name="[Ensemble] The 8 o'Clock Circus", checks=5),
    ReceptionInfo(id=70006, chapter=8, name="[Ensemble] L'heure du Loup", checks=5),
    ReceptionInfo(id=70007, chapter=8, name="[Ensemble] The Puppeteer", checks=5),
    ReceptionInfo(id=70008, chapter=8, name="[Ensemble] The Blood-red Night", checks=5),
    ReceptionInfo(id=70009, chapter=8, name="[Ensemble] Yesterday's Promise", checks=5),
    ReceptionInfo(id=70010, chapter=8, name="[Ensemble] The Blue Reverberation", checks=5),

    ReceptionInfo(id=60003, chapter=8, name="The Black Silence", checks=10),

    ReceptionInfo(id=60004, chapter=8, name="The Reverberation Ensemble Distorted", checks=10),
]
receptions_by_name: dict[str, ReceptionInfo] = {reception.name: reception for reception in receptions}
receptions_dict: dict[int, ReceptionInfo] = {reception.id: reception for reception in receptions}