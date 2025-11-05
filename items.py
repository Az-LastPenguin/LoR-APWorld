from dataclasses import dataclass
from typing import Literal
from BaseClasses import Item, ItemClassification
from .gamedata.books import books

# Items have types (denoted by different classes with type_ids). Some items have fixed amount of copies
# type_ids are converted to ints when creating ids for them to then send to clients

class LORItem(Item):
    game: str = "Library of Ruina"

item_types = ["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"]
@dataclass
class LORItemData:
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"]
    copies: int = 1
    type: ItemClassification = ItemClassification.progression

    def __post_init__(self):
        self.id = (item_types.index(self.type_id) << 28 | self.id)

@dataclass
class FloorUnlockItem(LORItemData):
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "FloorUnlock"
    copies = 1
    type = ItemClassification.progression

@dataclass
class AbnoPagesItem(LORItemData):
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "AbnoPages"
    copies = 5
    type = ItemClassification.progression_skip_balancing

@dataclass
class EgoPageItem(LORItemData):
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "EgoPage"
    copies = 5
    type = ItemClassification.progression_skip_balancing

@dataclass
class LibrarianItem(LORItemData):
    id: int
    name: str
    copies: int
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "Librarian"
    type = ItemClassification.progression

@dataclass
class BookItem(LORItemData):
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "Book"
    copies: int = 0
    type = ItemClassification.progression_skip_balancing

@dataclass
class OtherItem(LORItemData):
    id: int
    name: str
    type_id: Literal["FloorUnlock", "AbnoPages", "EgoPage", "Librarian", "Book", "Other"] = "Other"
    copies: int = 0
    type = ItemClassification.filler


item_list: list[LORItemData] = [
    # Floor Unlocks. Total - 10. Up to 9 per run.
    FloorUnlockItem(id=1, name="Floor of History"),
    FloorUnlockItem(id=2, name="Floor of Technological Sciences"),
    FloorUnlockItem(id=3, name="Floor of Literature"),
    FloorUnlockItem(id=4, name="Floor of Art"),
    FloorUnlockItem(id=5, name="Floor of Natural Sciences"),
    FloorUnlockItem(id=6, name="Floor of Language"),
    FloorUnlockItem(id=7, name="Floor of Social Sciences"),
    FloorUnlockItem(id=8, name="Floor of Philosophy"),
    FloorUnlockItem(id=9, name="Floor of Religion"),
    FloorUnlockItem(id=10, name="Floor of General Works"),

    # Floor Abno Pages. Total - 50. 5 per Floor.
    AbnoPagesItem(id=1, name="Malkuth Abnormality Pages"),
    AbnoPagesItem(id=2, name="Yesod Abnormality Pages"),
    AbnoPagesItem(id=3, name="Hod Abnormality Pages"),
    AbnoPagesItem(id=4, name="Netzach Abnormality Pages"),
    AbnoPagesItem(id=5, name="Tiphereth Abnormality Pages"),
    AbnoPagesItem(id=6, name="Gebura Abnormality Pages"),
    AbnoPagesItem(id=7, name="Chesed Abnormality Pages"),
    AbnoPagesItem(id=8, name="Binah Abnormality Pages"),
    AbnoPagesItem(id=9, name="Hokma Abnormality Pages"),
    AbnoPagesItem(id=10, name="Keter Abnormality Pages"),

    # Floor EGO Pages. Total - 50. 5 per Floor.
    EgoPageItem(id=1, name="Malkuth EGO Page"),
    EgoPageItem(id=2, name="Yesod EGO Page"),
    EgoPageItem(id=3, name="Hod EGO Page"),
    EgoPageItem(id=4, name="Netzach EGO Page"),
    EgoPageItem(id=5, name="Tiphereth EGO Page"),
    EgoPageItem(id=6, name="Gebura EGO Page"),
    EgoPageItem(id=7, name="Chesed EGO Page"),
    EgoPageItem(id=8, name="Binah EGO Page"),
    EgoPageItem(id=9, name="Hokma EGO Page"),
    EgoPageItem(id=10, name="Keter EGO Page"),

    # Floor Librarians. Total - 40. 4 per Floor. 3 for Binah.
    LibrarianItem(id=1, name="Malkuth Librarian", copies=4),
    LibrarianItem(id=2, name="Yesod Librarian", copies=4),
    LibrarianItem(id=3, name="Hod Librarian", copies=4),
    LibrarianItem(id=4, name="Netzach Librarian", copies=4),
    LibrarianItem(id=5, name="Tiphereth Librarian", copies=4),
    LibrarianItem(id=6, name="Gebura Librarian", copies=4),
    LibrarianItem(id=7, name="Chesed Librarian", copies=4),
    LibrarianItem(id=8, name="Binah Librarian", copies=3),
    LibrarianItem(id=9, name="Hokma Librarian", copies=4),
    LibrarianItem(id=10, name="Keter Librarian", copies=4),

    # Books. Total Amount varies.
    BookItem(id=123456, name="Book of Everything", type=ItemClassification.filler), # Could i interest you in everything all of the time?
    # Vanilla Books, always one of each
    *[BookItem(id=book.id, name=book.name, copies=1) for book in books],

    # Other. Total amount varies.
    OtherItem(id=0, name="Passive Attribution Points"), # Amount predefined & configurable
    OtherItem(id=1, name="Passive Limits Break"), # Amount predefined & configurable
    OtherItem(id=2, name="Emotion Limits Break"), # Amount predefined & configurable

    OtherItem(id=3, name="Binah", copies=1, type=ItemClassification.progression_skip_balancing), # Fixed amount
    OtherItem(id=4, name="The Black Silence's Page", copies=1, type=ItemClassification.progression_skip_balancing), # Fixed amount
]

items_by_category: dict[str, list[LORItemData]] = {item_type: [item for item in item_list if item.type_id == item_type] for item_type in item_types}
items_by_id: dict[int, LORItemData] = {item.id: item for item in item_list}
items_by_name: dict[str, LORItemData] = {item.name: item for item in item_list}
items_name_to_id: dict[str, int] = {item.name: item.id for item in item_list}