from dataclasses import dataclass
from typing import Literal

# Floor contains all stages with abnos/realization, abnos and realizations can be randomized individually
# Stage requirements can also be randomized

@dataclass
class Floor:
    floor_id: int # id of the floor this class represents (1-9 are Malkuth-Hokma, 10 is Keter)
    abno_stages: list['FloorStage'] # stages with abnormalities
    realization_stage: 'FloorStage' # stage with floor's realization

@dataclass
class FloorStage:
    id: int # in-game stage id
    name: str # name of the stage (will be used for location names)
    checks: int # amount of checks this stage will yield as a location
    requirements: list['FloorStageRequirement'] # Requirements in order to access the stage

# This list is for converting types to int to send to clients
requirement_types = ["Librarians", "Chapter", "Receptions", "Checks"]
class FloorStageRequirement:
    type: Literal["Librarians", "Chapter", "Receptions", "Checks"]

@dataclass
class LibrarianRequirement(FloorStageRequirement):
    type = "Librarians" # Have X librarians in order to access 
    librarians: int = 1

@dataclass
class ChapterRequirement(FloorStageRequirement):
    type = "Chapter" # Unlock any reception of chapter X to access
    chapter: int = 1

@dataclass
class ReceptionRequirement(FloorStageRequirement):
    receptions: list[int]
    type = "Receptions" # Complete certain receptions to access (Pretty much same as obtaining certain books to access)

@dataclass
class ChecksRequirement(FloorStageRequirement):
    checks: list[int]
    type = "Checks" # Receive certain items from other's checks to access


floors: list[Floor] = [
    # Malkuth
    Floor(
        floor_id=0,
        abno_stages=[
            FloorStage(id=201001, name="Scorched Girl", checks=3, requirements=[ReceptionRequirement([6])]),
            FloorStage(id=201002, name="Happy Teddy Bear", checks=3, requirements=[ReceptionRequirement([20003])]),
            FloorStage(id=201003, name="Fairy Festival", checks=3, requirements=[ReceptionRequirement([30001, 30004])]),
            FloorStage(id=201004, name="Queen Bee", checks=3, requirements=[ReceptionRequirement([40004, 40005])]),
        ],
        realization_stage=FloorStage(id=201005, name="Malkuth Realization", checks=8, requirements=[]),
    ),

    # Yesod
    Floor(
        floor_id=1,
        abno_stages=[
            FloorStage(id=202001, name="Forsaken Murderer", checks=3, requirements=[ReceptionRequirement([10001])]),
            FloorStage(id=202002, name="All-Around Helper", checks=3, requirements=[ReceptionRequirement([20003])]),
            FloorStage(id=202003, name="Singing Machine", checks=3, requirements=[ReceptionRequirement([30002, 30004])]),
            FloorStage(id=202004, name="The Funeral of the Dead Butterflies", checks=3, requirements=[ReceptionRequirement([30002, 40005, 40006])]),
        ],
        realization_stage=FloorStage(id=202005, name="Yesod Realization", checks=8, requirements=[]),
    ),

    # Hod
    Floor(
        floor_id=2,
        abno_stages=[
            FloorStage(id=203001, name="Today's Shy Look", checks=3, requirements=[ReceptionRequirement([10003])]),
            FloorStage(id=203002, name="The Red Shoes", checks=3, requirements=[ReceptionRequirement([20004])]),
            FloorStage(id=203003, name="Spider Bud", checks=3, requirements=[ReceptionRequirement([30001, 30003])]),
            FloorStage(id=203004, name="Laetitia", checks=3, requirements=[ReceptionRequirement([40001, 40007])]),
        ],
        realization_stage=FloorStage(id=203005, name="Hod Realization", checks=8, requirements=[]),
    ),

    # Netzach
    Floor(
        floor_id=3,
        abno_stages=[
            FloorStage(id=204001, name="Fragment of the Universe", checks=3, requirements=[ReceptionRequirement([20001])]),
            FloorStage(id=204002, name="Child of the Galaxy", checks=3, requirements=[ReceptionRequirement([20005])]),
            FloorStage(id=204003, name="Porccubus", checks=3, requirements=[ReceptionRequirement([30002, 30003])]),
            FloorStage(id=204004, name="Alriune", checks=3, requirements=[ReceptionRequirement([30008, 40003, 40008])]),
        ],
        realization_stage=FloorStage(id=204005, name="Netzach Realization", checks=8, requirements=[]),
    ),

    # Tiphereth
    Floor(
        floor_id=4,
        abno_stages=[
            FloorStage(id=205001, name="The Queen of Hatred", checks=3, requirements=[ReceptionRequirement([30006, 30007])]),
            FloorStage(id=205002, name="The Knight of Despair", checks=3, requirements=[ReceptionRequirement([30005, 30008])]),
            FloorStage(id=205003, name="The King of Greed", checks=3, requirements=[ReceptionRequirement([40008])]),
            FloorStage(id=205004, name="The Servant of Wrath", checks=3, requirements=[ReceptionRequirement([50008])]),
        ],
        realization_stage=FloorStage(id=205005, name="Tiphereth Realization", checks=8, requirements=[LibrarianRequirement(4)]),
    ),

    # Gebura
    Floor(
        floor_id=5,
        abno_stages=[
            FloorStage(id=206001, name="Little Red Riding Hooded Mercenary", checks=3, requirements=[ReceptionRequirement([40001, 40004])]),
            FloorStage(id=206002, name="Big and Will be Bad Wolf", checks=3, requirements=[ReceptionRequirement([40005, 40007])]),
            FloorStage(id=206003, name="Mountain of Smiling Bodies", checks=3, requirements=[ReceptionRequirement([50006])]),
            FloorStage(id=206004, name="Nosferatu", checks=3, requirements=[ReceptionRequirement([50009])]),
        ],
        realization_stage=FloorStage(id=206005, name="Gebura Realization", checks=8, requirements=[]),
    ),

    # Chesed
    Floor(
        floor_id=6,
        abno_stages=[
            FloorStage(id=207001, name="Scarecrow Searching for Wisdom", checks=3, requirements=[ReceptionRequirement([40002, 40003])]),
            FloorStage(id=207002, name="Warm-hearted Woodsman", checks=3, requirements=[ReceptionRequirement([40005, 40006])]),
            FloorStage(id=207003, name="The Road Home & Scaredy Cat", checks=3, requirements=[ReceptionRequirement([50005]), LibrarianRequirement(4)]),
            FloorStage(id=207004, name="Ozma", checks=3, requirements=[ReceptionRequirement([50007, 50010])]),
        ],
        realization_stage=FloorStage(id=207005, name="Chesed Realization", checks=8, requirements=[LibrarianRequirement(5)]),
    ),

    # Binah
    Floor(
        floor_id=7,
        abno_stages=[
            FloorStage(id=208001, name="Big Bird", checks=3, requirements=[ReceptionRequirement([50002]), LibrarianRequirement(2)]),
            FloorStage(id=208002, name="Punishing Bird", checks=3, requirements=[ReceptionRequirement([50008])]),
            FloorStage(id=208003, name="Judgement Bird", checks=3, requirements=[ReceptionRequirement([50009, 50010])]),
        ],
        realization_stage=FloorStage(id=208004, name="Binah Realization", checks=11, requirements=[ReceptionRequirement([50012, 50013])]),
    ),

    # Hokma
    Floor(
        floor_id=8,
        abno_stages=[
            FloorStage(id=209001, name="The Burrowing Heaven", checks=3, requirements=[ReceptionRequirement([50004])]),
            FloorStage(id=209002, name="The Price of Silence", checks=3, requirements=[ReceptionRequirement([50007]), LibrarianRequirement(2)]),
            FloorStage(id=209003, name="Blue Star", checks=3, requirements=[ReceptionRequirement([50010])]),
        ],
        realization_stage=FloorStage(id=209004, name="Hokma Realization", checks=11, requirements=[ReceptionRequirement([50011, 50014])]),
    ),

    # Keter
    Floor(
        floor_id=9,
        abno_stages=[
            FloorStage(id=210001, name="Bloodbath", checks=3, requirements=[ReceptionRequirement([5])]),
            FloorStage(id=210002, name="Heart of Aspiration", checks=3, requirements=[ChapterRequirement(3)]),
            FloorStage(id=210003, name="Pinocchio", checks=3, requirements=[ChapterRequirement(5)]),
            FloorStage(id=210004, name="The Snow Queen", checks=3, requirements=[ChapterRequirement(6)]),
        ],
        realization_stage=FloorStage(id=210009, name="Keter Realization", checks=8, requirements=[ReceptionRequirement([60002])]),
    ),
]
floors_dict: dict[int, Floor] = {floor.floor_id: floor for floor in floors}
floor_stages = [stage for floor in floors for stage in [*floor.abno_stages, floor.realization_stage]]