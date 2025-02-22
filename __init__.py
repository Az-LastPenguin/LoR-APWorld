import typing
import random
from .options import LOROptions  # the options we defined earlier
from .items import LORItem, item_table
from .locations import location_table, LORLocation  # same as above
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_item_rule, set_rule
from BaseClasses import Entrance, ItemClassification, Region, Tutorial

from Utils import visualize_regions

class LORWebWorld(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Library of Ruina with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["fragger"]
    )]

class LORWorld(World):
    game = "Library of Ruina"  # name of the game/world
    options_dataclass = LOROptions  # options the player can set
    options: LOROptions  # typing hints for option results
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    item_name_groups = { 
        "Floor": {name for name, data in item_table.items() if data.category == "Floor"},
        "AbnoPages": {name for name, data in item_table.items() if data.category == "AbnoPages"},
        "Librarians": {name for name, data in item_table.items() if data.category == "Librarian"},
        "EGOPage": {name for name, data in item_table.items() if data.category == "EGOPage"},
        "Receptions": {name for name, data in item_table.items() if data.category == "Reception"},
        "Progression": {name for name, data in item_table.items() if data.category == "Progression"},
    }
    location_name_to_id = {data.name: data.address for data in location_table}

    def generate_early(self) -> None:
        pass

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        main_region = Region("Game", self.player, self.multiworld)
        for data in location_table: # TODO: Add or remove "clear" locations depending on the goal
            main_region.locations.append(LORLocation(self.player, data.name, data.address, main_region))
        self.multiworld.regions.append(main_region)

        # TODO: Logic
        # I think one way is to make it like:
        #               -> ...
        #               |-> Keter suppressions -> Keter Realization (endgoal)
        # Menu -> Canard|
        #               |-> Story line A (Stray Dogs to Carnival, etc) -> Other endgoals
        #               -> ...

        #end_region = Region("End", self.player, self.multiworld)
        #end_event = LORLocation(self.player, "End  Condition", None, end_region)
        #end_event.place_locked_item(LORItem("End Condition Beaten", ItemClassification.progression, None, self.player))
        #end_region.locations.append(end_event)
        #self.multiworld.regions.append(end_region)
        #self.multiworld.completion_condition[self.player] = lambda state: state.has("End Condition Beaten", self.player)

        menu_region.connect(main_region)
        #main_region.connect(end_region)

    def create_item(self, item: str) -> LORItem:
        data = item_table[item]
        return LORItem(item, data.item_type, self.item_name_to_id[item], self.player)
    
    def create_items(self) -> None:
        itempool: list[str] = []

        #Open floors items
        #for name in self.item_name_groups["FloorOpen"]:
        #    itempool.append(name)
        

        #Abno pages items
        for name in self.item_name_groups["AbnoPages"]:
            itempool += [name]*5


        #Librarians (Binah 3 librarians because 2 are open from the start: the locked binah and another librarian)
        for name in self.item_name_groups["Librarians"]:
            if name == "Floor of Philosophy Librarian":
                itempool += [name]*3
            else:
                itempool += [name]*4


        #EGO
        for name in self.item_name_groups["EGOPage"]:
            itempool += [name]*5


        #Receptions
        for name in self.item_name_groups["Receptions"]:
            itempool.append(name)
        

        #Mandatory Librarian upgrades
        itempool += ["Bonus Passive Attribute Point"]*8
        itempool += ["Binah"]
        itempool += ["Black Silence"]

        itempool += ["Book of Everything"]*(len(location_table)-len(itempool))

        self.multiworld.itempool += map(self.create_item, itempool)

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        total = 0
        for i in self.multiworld.itempool:
            if i.name == "Book of Everything":
                total += 1

        return {
            # Seed
            "seed": random.randint(0, 2147483647).__str__(),

            # Settings
            "fillers": self.options.fillers.value,
            "traps": self.options.traps.value,
            "traps_difficulty": self.options.traps_difficulty.value,
            "locked_floors": self.options.locked_floors.value,
            "random_first_floor": self.options.random_first_floor.value,
            "end_goals": ",".join(self.options.end_goals.value),
            "ensemble_battles": self.options.ensemble_battles.value,
            "abno_page_balance": self.options.abno_page_balance.value,
            "drop_system": self.options.drop_system.value,
            "randomize_pages": self.options.randomize_pages.value,
            
            # Data
            "books_of_everything": total,
        }