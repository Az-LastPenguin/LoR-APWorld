from dataclasses import dataclass, field
from typing import Literal

# Floor contains all stages with abnos/realization, abnos and realizations can be randomized individually
# Stage requirements can also be randomized

@dataclass
class Floor:
    floor_id: int # id of the floor this class represents (1-9 are Malkuth-Hokma, 10 is Keter)
    floor_name: str
    abno_stages: list['FloorStage'] # stages with abnormalities
    realization_stage: 'FloorStage' # stage with floor's realization

@dataclass
class FloorStage:
    id: int # in-game stage id
    name: str # name of the stage (will be used for location names)
    checks: int # amount of checks this stage will yield as a location
    chapter: int # in which chapter this stage is playble in vanilla
    req_librarians: int = 1 # amount of librarians floor has to have before unlocking this stage
    req_books: list[int] = field(default_factory=list) # what books player has to have to be able to access this stage

vanilla_floors: list[Floor] = [
    # Malkuth
    Floor(
        floor_id=1,
        floor_name="Malkuth Floor",
        abno_stages=[
            FloorStage(id=201001, name="Scorched Girl", checks=3, chapter=1),
            FloorStage(id=201002, name="Happy Teddy Bear", checks=3, chapter=3),
            FloorStage(id=201003, name="Fairy Festival", checks=3, chapter=4),
            FloorStage(id=201004, name="Queen Bee", checks=3, chapter=5),
        ],
        realization_stage=FloorStage(id=201005, name="Malkuth Realization", checks=8, chapter=5),
    ),

    # Yesod
    Floor(
        floor_id=2,
        floor_name="Yesod Floor",
        abno_stages=[
            FloorStage(id=202001, name="Forsaken Murderer", checks=3, chapter=2),
            FloorStage(id=202002, name="All-Around Helper", checks=3, chapter=3),
            FloorStage(id=202003, name="Singing Machine", checks=3, chapter=4),
            FloorStage(id=202004, name="The Funeral of the Dead Butterflies", checks=3, chapter=5),
        ],
        realization_stage=FloorStage(id=202005, name="Yesod Realization", checks=8, chapter=5),
    ),

    # Hod
    Floor(
        floor_id=3,
        floor_name="Hod Floor",
        abno_stages=[
            FloorStage(id=203001, name="Today's Shy Look", checks=3, chapter=2),
            FloorStage(id=203002, name="The Red Shoes", checks=3, chapter=3),
            FloorStage(id=203003, name="Spider Bud", checks=3, chapter=4),
            FloorStage(id=203004, name="Laetitia", checks=3, chapter=5),
        ],
        realization_stage=FloorStage(id=203005, name="Hod Realization", checks=8, chapter=6),
    ),

    # Netzach
    Floor(
        floor_id=4,
        floor_name="Netzach Floor",
        abno_stages=[
            FloorStage(id=204001, name="Fragment of the Universe", checks=3, chapter=3),
            FloorStage(id=204002, name="Child of the Galaxy", checks=3, chapter=3),
            FloorStage(id=204003, name="Porccubus", checks=3, chapter=4),
            FloorStage(id=204004, name="Alriune", checks=3, chapter=5),
        ],
        realization_stage=FloorStage(id=204005, name="Netzach Realization", checks=8, chapter=5),
    ),

    # Tiphereth
    Floor(
        floor_id=5,
        floor_name="Tiphereth Floor",
        abno_stages=[
            FloorStage(id=205001, name="The Queen of Hatred", checks=3, chapter=4),
            FloorStage(id=205002, name="The Knight of Despair", checks=3, chapter=4),
            FloorStage(id=205003, name="The King of Greed", checks=3, chapter=5),
            FloorStage(id=205004, name="The Servant of Wrath", checks=3, chapter=6),
        ],
        realization_stage=FloorStage(id=205005, name="Tiphereth Realization", checks=8, req_librarians=4, chapter=6),
    ),

    # Gebura
    Floor(
        floor_id=6,
        floor_name="Gebura Floor",
        abno_stages=[
            FloorStage(id=206001, name="Little Red Riding Hooded Mercenary", checks=3, chapter=5),
            FloorStage(id=206002, name="Big and Will be Bad Wolf", checks=3, chapter=5),
            FloorStage(id=206003, name="Mountain of Smiling Bodies", checks=3, chapter=6),
            FloorStage(id=206004, name="Nosferatu", checks=3, chapter=6),
        ],
        realization_stage=FloorStage(id=206005, name="Gebura Realization", checks=8, chapter=6),
    ),

    # Chesed
    Floor(
        floor_id=7,
        floor_name="Chesed Floor",
        abno_stages=[
            FloorStage(id=207001, name="Scarecrow Searching for Wisdom", checks=3, chapter=5),
            FloorStage(id=207002, name="Warm-hearted Woodsman", checks=3, chapter=5),
            FloorStage(id=207003, name="The Road Home & Scaredy Cat", checks=3, req_librarians=4, chapter=6),
            FloorStage(id=207004, name="Ozma", checks=3, chapter=6),
        ],
        realization_stage=FloorStage(id=207005, name="Chesed Realization", checks=8, req_librarians=5, chapter=6),
    ),

    # Binah
    Floor(
        floor_id=8,
        floor_name="Binah Floor",
        abno_stages=[
            FloorStage(id=208001, name="Big Bird", checks=3, req_librarians=2, chapter=6),
            FloorStage(id=208002, name="Punishing Bird", checks=3, chapter=6),
            FloorStage(id=208003, name="Judgement Bird", checks=3, chapter=7),
        ],
        realization_stage=FloorStage(id=208004, name="Binah Realization", checks=11, chapter=7),
    ),

    # Hokma
    Floor(
        floor_id=9,
        floor_name="Hokma Floor",
        abno_stages=[
            FloorStage(id=209001, name="The Burrowing Heaven", checks=3, chapter=6),
            FloorStage(id=209002, name="The Price of Silence", checks=3, req_librarians=2, chapter=6),
            FloorStage(id=209003, name="Blue Star", checks=3, chapter=7),
        ],
        realization_stage=FloorStage(id=209004, name="Hokma Realization", checks=11, chapter=7),
    ),

    # Keter
    Floor(
        floor_id=10,
        floor_name="Keter Floor",
        abno_stages=[
            FloorStage(id=210001, name="Bloodbath", checks=3, chapter=1),
            FloorStage(id=210002, name="Heart of Aspiration", checks=3, chapter=3),
            FloorStage(id=210003, name="Pinocchio", checks=3, chapter=5),
            FloorStage(id=210004, name="The Snow Queen", checks=3, chapter=6),
        ],
        realization_stage=FloorStage(id=210009, name="Keter Realization", checks=8, chapter=7),
    ),
]
vanilla_floors_dict: dict[int, Floor] = {floor.floor_id: floor for floor in vanilla_floors}
vanilla_floor_stages = [stage for floor in vanilla_floors for stage in [*floor.abno_stages, floor.realization_stage]]