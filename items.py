from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification

class LORItem(Item):
    game: str = "Library of Ruina"

class LORItemData(NamedTuple):
    category: str
    code: int
    item_type: ItemClassification = ItemClassification.filler
    weight: Optional[int] = None

items: Dict[str, str] = {
    # Library
    # Total - 10 (Up to 9 in a run)
    "Floor of General Works":                                           "Floor",
    "Floor of History":                                                 "Floor",
    "Floor of Technological Sciences":                                  "Floor",
    "Floor of Literature":                                              "Floor",
    "Floor of Art":                                                     "Floor",
    "Floor of Natural Sciences":                                        "Floor",
    "Floor of Language":                                                "Floor",
    "Floor of Social Sciences":                                         "Floor",
    "Floor of Philosophy":                                              "Floor",
    "Floor of Religion":                                                "Floor",
 
    # Total - 50 (10 x 5) 
    "Floor of General Works Abnormality Pages":                         "AbnoPages",
    "Floor of History Abnormality Pages":                               "AbnoPages",
    "Floor of Technological Sciences Abnormality Pages":                "AbnoPages",
    "Floor of Literature Abnormality Pages":                            "AbnoPages",
    "Floor of Art Abnormality Pages":                                   "AbnoPages",
    "Floor of Natural Sciences Abnormality Pages":                      "AbnoPages",
    "Floor of Language Abnormality Pages":                              "AbnoPages",
    "Floor of Social Sciences Abnormality Pages":                       "AbnoPages",
    "Floor of Philosophy Abnormality Pages":                            "AbnoPages",
    "Floor of Religion Abnormality Pages":                              "AbnoPages",
 
    # Total - 39 (10 x 4; Each floor starts with 1, Philosophy starts with 2, one of which is locked Binah)
    "Floor of General Works Librarian":                                 "Librarian",
    "Floor of History Librarian":                                       "Librarian",
    "Floor of Technological Sciences Librarian":                        "Librarian",
    "Floor of Literature Librarian":                                    "Librarian",
    "Floor of Art Librarian":                                           "Librarian",
    "Floor of Natural Sciences Librarian":                              "Librarian",
    "Floor of Language Librarian":                                      "Librarian",
    "Floor of Social Sciences Librarian":                               "Librarian",
    "Floor of Philosophy Librarian":                                    "Librarian",
    "Floor of Religion Librarian":                                      "Librarian",
 
    # Total - 50 (10 x 5) 
    "Floor of General Works EGO Page":                                  "EGOPage",
    "Floor of History EGO Page":                                        "EGOPage",
    "Floor of Technological Sciences EGO Page":                         "EGOPage",
    "Floor of Literature EGO Page":                                     "EGOPage",
    "Floor of Art EGO Page":                                            "EGOPage",
    "Floor of Natural Sciences EGO Page":                               "EGOPage",
    "Floor of Language EGO Page":                                       "EGOPage",
    "Floor of Social Sciences EGO Page":                                "EGOPage",
    "Floor of Philosophy EGO Page":                                     "EGOPage",
    "Floor of Religion EGO Page":                                       "EGOPage",
 
    # Progression Stuff
    "Binah":                                                            "Progression",
    "Black Silence":                                                    "Progression",
}

useful = {
    "Bonus Passive Attribute Point":                                    "Useful",
    "Book of Everything":                                               "Useful",
}

item_table = {}

i = 0
for j, v in items.items():
    item_table[j] = LORItemData(v, i, ItemClassification.progression)
    i += 1

for j, v in useful.items():
    item_table[j] = LORItemData(v, i, ItemClassification.useful)
    i += 1