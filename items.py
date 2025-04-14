from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification

class LORItem(Item):
    game: str = "Library of Ruina"

class LORItemData:
    name: str
    amount: int
    type: ItemClassification
    id: int

    def __init__(self, name: str, amount: int = 1, type: ItemClassification = ItemClassification.progression, id: int = None):
        self.name = name
        self.amount = amount
        self.type = type
        self.id = id
        

# All those types of items have a "type id" (in brackets) that is put in their ids to differentiate on the client
# Reception unlock items have a fixed type id of 15 (Created in run-time)

# [0] Floor unlocks. Total - 10. Up to 9 in a run.
floors: list[LORItemData] = [
    LORItemData("Floor of History"),
    LORItemData("Floor of Technological Sciences"),
    LORItemData("Floor of Literature"),
    LORItemData("Floor of Art"),
    LORItemData("Floor of Natural Sciences"),
    LORItemData("Floor of Language"),
    LORItemData("Floor of Social Sciences"),
    LORItemData("Floor of Philosophy"),
    LORItemData("Floor of Religion"),
    LORItemData("Floor of General Works"),
]

# [1] Respective Floor's Abno Pages. Total - 50. 5 per Floor.
abno_pages: list[LORItemData] = [
    LORItemData("Malkuth Abnormality Pages", 5),
    LORItemData("Yesod Abnormality Pages", 5),
    LORItemData("Hod Abnormality Pages", 5),
    LORItemData("Netzach Abnormality Pages", 5),
    LORItemData("Tiphereth Abnormality Pages", 5),
    LORItemData("Gebura Abnormality Pages", 5),
    LORItemData("Chesed Abnormality Pages", 5),
    LORItemData("Binah Abnormality Pages", 5),
    LORItemData("Hokma Abnormality Pages", 5),
    LORItemData("Keter Abnormality Pages", 5),
]

# [2] Respective Floor's EGO Pages. Total - 50. 5 per Floor.
ego: list[LORItemData] = [
    LORItemData("Malkuth EGO Page", 5),
    LORItemData("Yesod EGO Page", 5),
    LORItemData("Hod EGO Page", 5),
    LORItemData("Netzach EGO Page", 5),
    LORItemData("Tiphereth EGO Page", 5),
    LORItemData("Gebura EGO Page", 5),
    LORItemData("Chesed EGO Page", 5),
    LORItemData("Binah EGO Page", 5),
    LORItemData("Hokma EGO Page", 5),
    LORItemData("Keter EGO Page", 5),
]

# [3] Respective Floor's Librarians. Total - 39. 4 per Floor. 3 for Binah Floor, as it starts with locked Binah and a nugget
librarians: list[LORItemData] = [
    LORItemData("Malkuth Librarian", 4),
    LORItemData("Yesod Librarian", 4),
    LORItemData("Hod Librarian", 4),
    LORItemData("Netzach Librarian", 4),
    LORItemData("Tiphereth Librarian", 4),
    LORItemData("Gebura Librarian", 4),
    LORItemData("Chesed Librarian", 4),
    LORItemData("Binah Librarian", 3),
    LORItemData("Hokma Librarian", 4),
    LORItemData("Keter Librarian", 4),
]

# [4] Book items that player can get
books: list[LORItemData] = [
    LORItemData("Book of Everything", 0, id=123456, type=ItemClassification.skip_balancing)
]

# Those are each own list just for the automation purposes
passive = [LORItemData("Passive Attribution Point", 0)] # [5]
binah = [LORItemData("Binah")] # [6]
roland = [LORItemData("The Black Silence's Page")] # [7]



# Compile everything into one list
item_list: list[LORItemData] = []
item_dict: dict[str, LORItemData] = {}

t = 0
for l in [floors, abno_pages, ego, librarians, books, passive, binah, roland]:
    id = 0
    for i in l:
        i.id = (t << 28 | (i.id if i.id != None else id))
        item_list.append(i)
        item_dict[i.name] = i
        id += 1
    
    t += 1