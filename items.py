from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification

class LORItem(Item):
    game: str = "Library of Ruina"

class LORItemData(NamedTuple):
    category: str
    code: int
    item_type: ItemClassification = ItemClassification.filler
    weight: Optional[int] = None

base_offset: int = 143000

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
 
 
    # Receptions (Currently not used, was used before) 
    # Story Receptions - 31 
    "Reception of Zwei Office":                                         "Reception",
    "Reception of Molar Office":                                        "Reception",
    "Reception of Stray Dogs":                                          "Reception",
 
    "Reception of The Carnival":                                        "Reception",
    "Reception of Kurokumo Clan":                                       "Reception",
    "Reception of Full-Stop Office":                                    "Reception",
    "Reception of Musicians of Bremen":                                 "Reception",
    "Reception of Dawn Office":                                         "Reception",
    "Reception of Wedge Office":                                        "Reception",
    "Reception of Gaze Office":                                         "Reception",
    "Reception of Tomerry":                                             "Reception",
 
    "Reception of Sweepers":                                            "Reception",
    "Reception of Index Proselytes":                                    "Reception",
    "Reception of Shi Association":                                     "Reception",
    "Reception of Smiling Faces":                                       "Reception",
    "Reception of The 8 o'Clock Circus":                                "Reception",
    "Reception of The Crying Children":                                 "Reception",
    "Reception of Puppets":                                             "Reception",
    "Reception of WARP Cleanup Crew":                                   "Reception",
 
    "Reception of The Thumb":                                           "Reception",
    "Reception of Index Proxies":                                       "Reception",
    "Reception of 얀샋ㄷ요무":                                           "Reception",
    "Reception of The Blue Reverberation":                              "Reception",
    "Reception of The Red Mist":                                        "Reception",
    "Reception of The Purple Tear":                                     "Reception",
    "Reception of Liu Association Section 2":                           "Reception",
    "Reception of Liu Association Section 1":                           "Reception",
    "Reception of Xiao":                                                "Reception",
    "Reception of Cane Office":                                         "Reception",
    "Reception of R Corp.":                                             "Reception",
    "Reception of R Corp. II":                                          "Reception",
 
    "Reception of The Hana Association":                                "Reception",
 
    # General Receptions - 16
    "Grade 8 Fixers Reception":                                         "Reception",
    "Grade 7 Fixers Reception":                                         "Reception",
    "Urban Legend-class Office Reception":                              "Reception",
    "Urban Legend-class Syndicate Reception":                           "Reception",
    "Axe Gang Reception":                                               "Reception",
 
    "Rusted Chains Reception":                                          "Reception",
    "Workshop-affiliated Fixers Reception":                             "Reception",
    "Jeong's Office Reception":                                         "Reception",
 
    "Seven Association Reception":                                      "Reception",
    "Blade Lineage Reception":                                          "Reception",
 
    "Dong-hwan the Grade 1 Fixer Reception":                            "Reception",
    "Night Awls Reception":                                             "Reception",
    "The Udjat Reception":                                              "Reception",
    "Mirae Life Insurance Reception":                                   "Reception",
    "Leaflet Workshop Reception":                                       "Reception",
    "Bayard Reception":                                                 "Reception",
 
 
    # Progression Stuff
    # Total - Configurable (8 by default)
    "Bonus Passive Attribute Point":                                    "Progression",
    # Total - All other free spaces
    "Book of Everything":                                               "Progression",
    "Binah":                                                            "Progression",
    "Black Silence":                                                    "Progression",
}

item_table = {}

i = 0
for j, v in items.items():
    item_table[j] = LORItemData(v, base_offset + i, ItemClassification.progression)
    i += 1