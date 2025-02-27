import typing
from .options import LOROptions
from .items import LORItem, item_table
from .locations import floor_models, all_locations, chapter_models, LORLocation
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
    game = "Library of Ruina" 
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True  # show path to required location checks in spoiler

    run_seed: int

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    item_name_groups = { 
        "Floor": {name for name, data in item_table.items() if data.category == "Floor"},
        "AbnoPages": {name for name, data in item_table.items() if data.category == "AbnoPages"},
        "Librarians": {name for name, data in item_table.items() if data.category == "Librarian"},
        "EGOPage": {name for name, data in item_table.items() if data.category == "EGOPage"},
        "Receptions": {name for name, data in item_table.items() if data.category == "Reception"},
        "Progression": {name for name, data in item_table.items() if data.category == "Progression"},
    }
    location_name_to_id = all_locations

    def generate_early(self) -> None:
        self.random.seed()

        # Randomize Abnos if needed 
        if self.options.randomize_abnos.value == 1 or self.options.randomize_abnos.value == 2:
            all_abnos = []
            for i in floor_models:
                for j in i.abnos:
                    all_abnos.append(j)
            
            self.random.shuffle(all_abnos)

            for i in floor_models:
                abnos = len(i.abnos)
                print(abnos)
                i.abnos.clear()
                for j in range(abnos):
                    i.abnos.append(all_abnos.pop())
            
            if self.options.randomize_abnos.value == 2:
                all_realizations = []
                for i in floor_models:
                    all_realizations.append(i.realization)
                
                self.random.shuffle(all_realizations)

                for i in floor_models:
                    i.realization = all_realizations.pop()
        
        # Randomize Receptions if needed
        if self.options.randomize_receptions.value == 2:
            for i in chapter_models: # TODO: Somehow make client know how receptions were shuffled
                self.random.shuffle(i.receptions)
            
            

            

        
    # Fills region with location in dict's order, also making locations require previous ones
    def populate_region(self, region, locations, first_important = False):
        pass

    # Creates an exit from exit_region to enter_region with requirement of collecting item from last location of exit_region
    def connect_regions(self, exit_region, enter_region):
        pass

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        main_region = Region("Game", self.player, self.multiworld)

        print(all_locations.__len__())

        for l, i in all_locations.items():
            main_region.locations.append(LORLocation(self.player, l, i, main_region))


        self.multiworld.regions.append(main_region)
        menu.connect(main_region)

        # Receptions
        #canard = Region("Canard", self.player, self.multiworld)
        #self.populate_region(canard, location_table["Canard"])
        #menu.connect(canard)

        #urban_legend = Region("Urban Legend", self.player, self.multiworld)
        #self.populate_region(urban_legend, location_table["Urban Legend"])
        #self.connect_regions(canard, urban_legend)

        #story_A = Region("StoryA", self.player, self.multiworld)
        #self.populate_region(story_A, location_table["StoryA"])
        #self.connect_regions(urban_legend, story_A)

        #story_B = Region("StoryB", self.player, self.multiworld)
        #self.populate_region(story_A, location_table["StoryB"])
        #self.connect_regions(urban_legend, story_B)

        #story_C = Region("StoryC", self.player, self.multiworld)
        #self.populate_region(story_A, location_table["StoryC"])
        #self.connect_regions(urban_legend, story_C)

        #story_D = Region("StoryD", self.player, self.multiworld)
        #self.populate_region(story_A, location_table["StoryD"])
        #self.connect_regions(urban_legend, story_D)






        # main_region = Region("Game", self.player, self.multiworld)
        # for data in location_table: # TODO: Add or remove "clear" locations depending on the goal
        #     main_region.locations.append(LORLocation(self.player, data.name, data.address, main_region))
        # self.multiworld.regions.append(main_region)

        # TODO: Logic
        # I think one way is to make it like:
        #               -> ...
        #               |-> Keter suppressions -> Keter Realization (endgoal)
        # Menu -> Canard|
        #               |-> Story line A (Stray Dogs to Carnival, etc) -> Other endgoals
        #               -> ...

        # end_region = Region("End", self.player, self.multiworld)
        # end_event = LORLocation(self.player, "End  Condition", None, end_region)
        # end_event.place_locked_item(LORItem("End Condition Beaten", ItemClassification.progression, None, self.player))
        # end_region.locations.append(end_event)
        # self.multiworld.regions.append(end_region)
        # self.multiworld.completion_condition[self.player] = lambda state: state.has("End Condition Beaten", self.player)

        # menu_region.connect(main_region)
        # main_region.connect(end_region)

    def create_item(self, item: str) -> LORItem:
        data = item_table[item]
        return LORItem(item, data.item_type, self.item_name_to_id[item], self.player)
    
    def create_items(self) -> None:
        itempool: list[str] = []

        #Open floors items
        #for name in self.item_name_groups["FloorOpen"]:
        #    itempool.append(name)
        

        #Abno pages items
        #for name in self.item_name_groups["AbnoPages"]:
        #    itempool += [name]*5


        #Librarians (Binah 3 librarians because 2 are open from the start: the locked binah and another librarian)
        #for name in self.item_name_groups["Librarians"]:
        #    if name == "Floor of Philosophy Librarian":
        #        itempool += [name]*3
        #    else:
        #        itempool += [name]*4


        #EGO
        #for name in self.item_name_groups["EGOPage"]:
        #    itempool += [name]*5


        #Receptions
        #for name in self.item_name_groups["Receptions"]:
        #    itempool.append(name)
        

        #Mandatory Librarian upgrades
        #itempool += ["Bonus Passive Attribute Point"]*8
        #itempool += ["Binah"]
        #itempool += ["Black Silence"]
#
        itempool += ["Book of Everything"]*(len(all_locations)-len(itempool))

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
            "seed": str(self.random.randint(0, 2147483647)),

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
    