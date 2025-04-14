import typing
from .options import LOROptions
from .items import LORItem, LORItemData, item_list, item_dict
from .locations import LORLocation, MapNode, FloorInfo, generate_reception_tree, randomize_suppresions, location_list, endgoals
from worlds.AutoWorld import World
from worlds.generic.Rules import add_item_rule, set_rule
from BaseClasses import Entrance, ItemClassification, Region, LocationProgressType
from Utils import visualize_regions

class LORWorld(World):
    game = "Library of Ruina" 
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True  # show path to required location checks in spoiler

    #item_name_groups = { 
    #    "Floor": {name for name, data in item_table.items() if data.category == "Floor"},
    #    "AbnoPages": {name for name, data in item_table.items() if data.category == "AbnoPages"},
    #    "Librarians": {name for name, data in item_table.items() if data.category == "Librarian"},
    #    "EGOPage": {name for name, data in item_table.items() if data.category == "EGOPage"},
    #    "Receptions": {name for name, data in item_table.items() if data.category == "Reception"},
    #    "Progression": {name for name, data in item_table.items() if data.category == "Progression"},
    #}
    item_name_to_id = {item.name: item.id for item in item_list}
    location_name_to_id = location_list

    reception_tree: list[MapNode]
    floors: list[FloorInfo]
    first_floor: int

    def generate_early(self) -> None:
        # Randomize Suppressions & Receptions
        self.random.seed()

        # If Locked Floors option is On, select the first floor
        if self.options.locked_floors.value:
            if self.options.first_floor.value == 10:
                self.first_floor = self.random.randint(0, 9)
            else:
                self.first_floor = self.options.first_floor.value
            
            # Add Every other floor's unlock item to the list
            for i in [i for i in item_list if "Floor of " in i.name]:
                if i.id != self.first_floor:
                    i.amount = 1

        # Randomize Suppressions' / Realizaztions' order and floor if needed
        self.floors = randomize_suppresions(self.options.abno_prog.value, self.random)

        # Randomize Receptions order if needed
        self.reception_tree = generate_reception_tree(self.options.reception_prog.value, self.random)

        # If reception prog random is 1 or 3, we have to generate items which will be unlocking the receptions
        if self.options.reception_prog.value != 1 and self.options.reception_prog.value != 3:
            return
        
        for n in [n for n in self.reception_tree if n.receptions[0].chapter >= 2]:
            for r in n.receptions:
                item = LORItemData("Reception of "+r.name, id=(15 << 28 | r.id))
                item_list.append(item)
                item_dict[item.name] = item

    def create_regions(self) -> None:
        # Generate Spheres
        # 1. Generate Menu sphere (techinal 0th sphere w/o items)
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # 2. Generate floor spheres
        names = ["Malkuth", "Yesod", "Hod", "Netzach", "Tiphereth", "Gebura", "Chesed", "Binah", "Hokma", "Keter"]
        for i in range(10):
            floor = self.floors[i]
            name = names[i]
            stages = [*floor.abnos, floor.realization]

            floor_region = Region(name, self.player, self.multiworld)

            for s in stages:
                for k in s.locations.keys():
                    floor_region.locations.append(LORLocation(self.player, k, s.locations[k], floor_region))

            self.multiworld.regions.append(floor_region)

            menu.connect(floor_region)
            
        # 3. Generate reception spheres
        prev_region = menu

        for i in range(1, 8):
            nodes = [n for n in self.reception_tree if n.receptions[0].chapter == i]
            chapter_region = Region("Chapter "+str(i), self.player, self.multiworld)

            for n in nodes:
                for r in n.receptions:
                    for k in r.locations.keys():
                        loc = LORLocation(self.player, k, r.locations[k], chapter_region)
                        if self.options.reception_prog == 1 or self.options.reception_prog == 3:
                            loc.access_rule = lambda state: [a for a, b in state.prog_items[self.player].items() if (a in ["Reception of "+node.receptions[-1].name for node in n.prev] and b >= 1)]
                        else:
                            loc.access_rule = lambda state: True in [state.can_reach_location(l) for l in [node.receptions[-1].name + " (1)" for node in n.prev]]
                        
                        chapter_region.locations.append(loc)
            
            self.multiworld.regions.append(chapter_region)

            prev_region.connect(chapter_region)

            prev_region = chapter_region

        # 4. Generate Endgame sphere with every selected endgoal (except Keter realization)
        endgame_region = Region("Endgame", self.player, self.multiworld)

        for s in endgoals:
            for k in s.locations.keys():
                loc = LORLocation(self.player, k, s.locations[k], endgame_region)
                loc.progress_type = LocationProgressType.EXCLUDED
                endgame_region.locations.append(loc)
        
        self.multiworld.regions.append(endgame_region)

        prev_region.connect(endgame_region)

    def create_item(self, item: str) -> LORItem:
        data: LORItemData = list(filter(lambda x: x.name == item, item_list))[0]
        return LORItem(item, data.type, data.id, self.player)
    
    def create_items(self) -> None:
        itempool: list[str] = []

        # Fill item pool with items with already determined amount of copies
        for i in item_list:
            if i.amount > 0:
                itempool += [i.name]*i.amount

        # Add certain amount of passive attribution point items
        itempool += ["Passive Attribution Point"]*self.options.passive_points.value

        # Fill free space in the item pool
        itempool += ["Book of Everything"]*(len(self.multiworld.get_locations(self.player))-len(itempool))

        self.multiworld.itempool += map(self.create_item, itempool)

    def set_rules(self) -> None:
        
        pass

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        input()
        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
        pass
        #total = 0
        #for i in self.multiworld.itempool:
        #    if i.name == "Book of Everything":
        #        total += 1

        #return {
        #    # Seed
        #    "seed": str(self.random.randint(0, 2147483647)),
        #
        #    # Settings
        #    "fillers": self.options.fillers.value,
        #    "traps": self.options.traps.value,
        #    "traps_difficulty": self.options.traps_difficulty.value,
        #    "locked_floors": self.options.locked_floors.value,
        #    "random_first_floor": self.options.random_first_floor.value,
        #    "end_goals": ",".join(self.options.end_goals.value),
        #    "ensemble_battles": self.options.ensemble_battles.value,
        #    "abno_page_balance": self.options.abno_page_balance.value,
        #    "drop_system": self.options.drop_system.value,
        #    "randomize_pages": self.options.randomize_pages.value,
        #    
        #    # Data
        #    "books_of_everything": total,
        #}
    