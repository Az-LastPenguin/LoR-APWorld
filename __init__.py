import typing, time

from Options import OptionError
from . import logic
from .options import LOROptions
from .items import LORItem, LORItemData, items_by_id, items_by_name, items_by_category, items_name_to_id
from .locations import LORLocation, ReceptionTree, setup_locations, locations_name_to_id
from .gamedata.receptions import ReceptionNode, receptions_dict, receptions_by_name, endgoal_receptions
from .gamedata.abnormalities import Floor, FloorStage
from .gamedata.books import books_dict, books_by_name
from .util import box_muller_constraint
from worlds.AutoWorld import World
from worlds.generic.Rules import add_item_rule, set_rule
from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Region, LocationProgressType
from Utils import visualize_regions

## TODO Webworld here?

class LORWorld(World):
    game = "Library of Ruina" 
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = items_name_to_id
    location_name_to_id = locations_name_to_id

    reception_tree: ReceptionTree = None
    floors: list[Floor] = []

    def generate_early(self) -> None:
        # Check for option conflicts # NOTE: Might be possible to implement, so commented out for now
        #if self.options.filler_items == 0 and (self.options.receptions_progression != 1 or self.options.receptions_progression != 3):
        #    raise OptionError(f"{self.player_name}'s Library of ruina has Book of Everything selected as a filler item, but"
        #                      f" Receptions Progreession is not set to Progression or ProgressionBooks!")

        # Set Randomization Seed
        if self.options.random_seed.value < 0:
            self.options.random_seed.value = int(time.time())

        self.random.seed(self.options.random_seed.value)

        # Setup Locations overall
        self.reception_tree, self.floors = setup_locations(self.random, self.options)

        # Precollect unlocked floors
        if self.options.lock_floors.value: # I am very fond of long-ass one-liners
            floor = items_by_category["FloorUnlock"][self.random.randint(0,9) if self.options.starting_floor.value >= 10 else self.options.starting_floor.value].name
            self.multiworld.push_precollected(self.create_item(floor))
            items_by_name[floor].copies = 0
        else:
            for fi in items_by_category["FloorUnlock"]:
                self.multiworld.push_precollected(self.create_item(fi.name))
                items_by_name[fi.name].copies = 0
        
        # Set amount of other items
        for i in items_by_name.values():
            if i.name == "Passive Attribution Points":
                i.copies = self.options.passive_points_items.value

            if i.name == "Passive Limits Break":
                i.copies = self.options.passive_limits_items.value

            if i.name == "Emotion Limits Break":
                i.copies = self.options.emotion_limits_items.value

        # Precollect "Passive Attribution Points" items
        for i in range(self.options.starting_passive_points_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Attribution Points"))

        # Precollect "Passive Limits Break" items
        for i in range(self.options.starting_passive_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Limits Break"))

        # Precollect "Emotion Limits Break" items
        for i in range(self.options.starting_emotion_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Emotion Limits Break"))

        # Precollect or add to the pool the "Combat Page Exclusiveness Remove" item
        if self.options.remove_exclusive == 1:
            items_by_name["Combat Page Exclusiveness Remove"].copies = 1
        else:
            self.multiworld.push_precollected(self.create_item("Combat Page Exclusiveness Remove"))

        # Remove "The Black Silence's Page" from the pool if randomize_black_silence_page is false
        if not self.options.randomize_black_silence_page:
            items_by_name["The Black Silence's Page"].copies = 0

    def create_regions(self) -> None:
        # 1. Create Menu region (techinal 0th sphere w/o items)
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # 2. Create a region for each reception
        for node in self.reception_tree.reception_nodes:
            node_region = Region(node.name, self.player, self.multiworld)
            
            # Create a location for each check
            for i in range(node.checks):
                location_name = f"{node.name} ({i+1})"

                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], node_region)
                node_region.locations.append(location)

            self.multiworld.regions.append(node_region)

        # 2.1 Pre-place Black Silence Page at Oliver Reception if needed
        if self.options.randomize_black_silence_page.value:
            self.multiworld.get_location("Oliver (1)", self.player).place_locked_item(self.create_item("The Black Silence's Page"))

        # 3. Connect regions and add access rules
        # We have to connect Menu region to the first reception
        menu.connect(self.multiworld.get_region(self.reception_tree.get_node(self.reception_tree.first_reception).name, self.player))

        # Now connect every other region
        for node in self.reception_tree.reception_nodes:
            this_region: Region = self.multiworld.get_region(node.name, self.player)

            # First we connect each region to the next
            if self.options.receptions_progression == 0 or self.options.receptions_progression == 2:
                # If it's those options, every reception is available from start and is also the last reception
                menu.connect(this_region)
            else:
                for nn in node.next:
                    this_region.connect(self.multiworld.get_region(self.reception_tree.get_node(nn).name, self.player))

            # Require Books
            for entrance in this_region.entrances:
                books = []
                for b in node.req_books:
                    books.append(books_dict[b].name)
                set_rule(entrance, lambda state, books=books: state.has_all(books, self.player) and logic.lor_enough_librarians(node.req_librarians, state, self.player))

        # 4. Create regions for abnos and connect them, also add rules
        max_depth = self.reception_tree.get_depth(self.reception_tree.last_reception)
        part = (max_depth - 2) / 5
        for i in range(10):
            floor = self.floors[i]
            j = 1
            for stage in [*floor.abno_stages, floor.realization_stage]:
                stage_region = Region(stage.name, self.player, self.multiworld)
                self.multiworld.regions.append(stage_region)

                # Create locations
                for k in range(stage.checks):
                    location_name = f"{stage.name} ({k+1})"

                    location = LORLocation(self.player, location_name, locations_name_to_id[location_name], stage_region)
                    stage_region.locations.append(location)
                    # TODO: Try to disable this rule and see if its good?
                    # add_item_rule(location, lambda item: item.player != self.player or (not item.name in list(books_by_name.keys()) or item.classification == ItemClassification.filler))

                # Select which region to connect to and connect
                y = part * j
                depth = round(y + box_muller_constraint(self.random, -part/2, part/2))

                depth_nodes = self.reception_tree.get_nodes_of_depth(depth)
                node = depth_nodes[self.random.randint(0, len(depth_nodes)-1) if len(depth_nodes) > 0 else 0]
                node_region: Region = self.multiworld.get_region(node.name, self.player)

                node_region.connect(stage_region)
                
                # Set rule
                books = []
                for b in node.req_books:
                    books.append(books_dict[b].name)
                    
                set_rule(stage_region.entrances[0], lambda state, books=books: 
                         state.has_all(books, self.player) 
                         and logic.lor_has_floor(i, state, self.player) 
                         and logic.lor_enough_librarians_on_floor(i, stage.req_librarians, state, self.player))

                j += 1

        # 5. Create endgame region, connect it to the last reception
        endgame = Region("Endgame", self.player, self.multiworld)

        # Add the endgoal locations
        for node in endgoal_receptions:
            # Create a location for each check
            for i in range(node.checks):
                location_name = f"{node.name} ({i+1})"

                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], endgame)
                location.progress_type = LocationProgressType.EXCLUDED
                endgame.locations.append(location)

        # Create endgoal location with finish event
        victory_event = LORLocation(self.player, "Game Completed", None, endgame)
        victory_event.place_locked_item(self.create_event("One Perfect Book Achieved"))
        endgame.locations.append(victory_event)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("One Perfect Book Achieved", self.player)

        # Connect endgame region to mid
        if self.options.receptions_progression == 0 or self.options.receptions_progression == 2:
            for node in self.reception_tree.reception_nodes:
                this_region: Region = self.multiworld.get_region(node.name, self.player)

                this_region.connect(endgame)
        else:
            last_node = self.multiworld.get_region(self.reception_tree.get_node(self.reception_tree.last_reception).name, self.player)
            last_node.connect(endgame)

        self.multiworld.regions.append(endgame)

    def create_item(self, item: str) -> LORItem:
        data: LORItemData = items_by_name[item]
        return LORItem(item, data.type, data.id, self.player)
    
    def create_event(self, event: str) -> LORItem:
        return LORItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        # Test item pool
        itempool: list[str] = [] 
    
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Create item pool variable
        itempool: list[str] = []

        # Fill item pool with items with fixed amount of copies (Books, Upgrades, Binah, Black Silence's Page)
        for i in items_by_name.values():
            if i.copies > 0:
                itempool += [i.name]*i.copies

        # Fill all unused space with the filler items
        fillers = ["Book of Everything", "Booster Pack"]
        itempool += [fillers[self.options.filler_items]]*(total_locations-len(itempool))
        
        # Set the item pool
        self.multiworld.itempool += map(self.create_item, itempool)

    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        # input()
        visualize_regions(self.multiworld.get_region("Menu", self.player), "lorap.puml")

        slot_data = self.options.as_dict(
            "random_seed",
            "endgoals",
            "ensemble_battles",
            "abno_page_shuffle",
            "abno_page_randomization",
            "exodia_guaratnee",
            "ego_page_shuffle",
            "randomize_reception_tree",
            "receptions_progression",
            "enemies_turn_into_checks",
            "abno_randomization",
            "shuffle_realizations",
            "floors_require_books",
            "randomize_black_silence_page",
            "balance_book_contents",
            "filler_items",
            )

        for l in self.multiworld.get_locations(self.player):
            print(l)

        reception_book_requirements = {node.id: node.req_books for node in self.reception_tree.reception_nodes}
        slot_data["reception_book_requirements"] = reception_book_requirements

        abno_book_requirements: list[list[list[int]]] = []
        abno_fight_order: list[list[int]] = []
        for floor in self.floors:
            abno_book_requirements.append([stage.req_books for stage in [*floor.abno_stages, floor.realization_stage]])
            abno_fight_order.append([stage.id for stage in [*floor.abno_stages, floor.realization_stage]])
        slot_data["abno_book_requirements"] = abno_book_requirements
        slot_data["abno_fight_order"] = abno_fight_order


        slot_data["first_reception"] = self.reception_tree.first_reception
        slot_data["last_reception"] = self.reception_tree.last_reception

        reception_tree: dict[int, dict] = {}
        for node in self.reception_tree.reception_nodes:
            reception_tree[node.id] = {
                "next": node.next,
                "y": node.y,
            }
        slot_data["reception_tree"] = reception_tree

        return slot_data
    