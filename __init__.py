import typing
import time
from .options import LOROptions
from .items import LORItem, LORItemData, items_by_name, items_by_category, items_name_to_id
from .locations import LORLocation, setup_locations, locations_name_to_id
from .gamedata.receptions import ReceptionGroupInfo, receptions_dict, receptions_by_name
from .gamedata.abnormalities import Floor
from .gamedata.books import books_dict
from worlds.AutoWorld import World
from worlds.generic.Rules import add_item_rule, set_rule
from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Region, LocationProgressType
from Utils import visualize_regions

## TODO Webworld here

class LORWorld(World):
    game = "Library of Ruina" 
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True  # show path to required location checks in spoiler

    item_name_to_id = items_name_to_id
    location_name_to_id = locations_name_to_id

    reception_groups: list[ReceptionGroupInfo] = []
    reception_tree = None
    floors: list[Floor] = []

    def generate_early(self) -> None:
        # Set Randomization Seed
        if self.options.random_seed.value < 0:
            self.options.random_seed.value = int(time.time())

        self.random.seed(self.options.random_seed.value)

        # Setup Locations overall
        self.reception_groups, self.reception_tree, self.floors = setup_locations(self.random, self.options.randomize_reception_tree.value, self.options.abno_randomization.value, self.options.shuffle_realizations.value)

        # Precollect unlocked floors
        if self.options.lock_floors.value: # I am very fond of very long one-liners
            self.multiworld.push_precollected(self.create_item(items_by_category["FloorUnlock"][self.options.starting_floor.value == 10 and self.random.randint(0,9) or self.options.starting_floor.value].name))
        else:
            for fi in items_by_category["FloorUnlock"]:
                self.multiworld.push_precollected(self.create_item(fi.name))
        
        # Precollect "Passive Attribution Points"
        for i in range(self.options.starting_passive_points_items):
            self.multiworld.push_precollected(self.create_item("Passive Attribution Points"))

        # Precollect "Passive Limits Break"
        for i in range(self.options.starting_passive_limits_items):
            self.multiworld.push_precollected(self.create_item("Passive Limits Break"))

        # Precollect "Emotion Limits Break"
        for i in range(self.options.starting_emotion_limits_items):
            self.multiworld.push_precollected(self.create_item("Emotion Limits Break"))

    def create_regions(self) -> None:
        # Generate Spheres
        # 1. Generate Menu sphere (techinal 0th sphere w/o items)
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        # 2.1. Generate Chapter Spheres with receptions
        prev_region = menu
        for i in range(1,8): # Chapters 1-7
            chapter_region = Region(f"Chapter {i}", self.player, self.multiworld)
            groups = [group for group in self.reception_groups if group.chapter == i]

            # 2.2. Go through receptions in every group to create locations associated with them
            for group in groups:
                for rid in group.receptions:
                    index = group.receptions.index(rid)
                    reception = receptions_dict[rid]

                    # Create event location for this reception
                    reception_event = LORLocation(self.player, reception.name, None, chapter_region)
                    reception_event.place_locked_item(self.create_event(f"Completed Reception of {reception.name}"))

                    # Rule: Can only access (complete) this reception depending on settings either if one of previous receptions was completed or this plus all required book items received
                    need_receptions = []
                    need_books = []
                    # Add prev reception clears as a requirement
                    if self.options.receptions_progression.value != 0:
                        if index > 0: # If this reception is not the first in the group
                            prev_reception = group.receptions[index-1]
                            need_receptions.append(f"Completed Reception of {receptions_dict[prev_reception].name}")
                        else: # If it is, check last receptions of previous groups
                            for pg in group.prev_groups:
                                prev_group = next((g for g in self.reception_groups if g.id == pg))
                                last_reception = prev_group.receptions[-1]
                                need_receptions.append(f"Completed Reception of {receptions_dict[last_reception].name}")
                    
                    # Add book requirement
                    if self.options.receptions_progression.value == 2:
                        for b in reception.req_books:
                            need_books.append(books_dict[b].name) 
   
                    if reception.id != 2:
                        set_rule(reception_event, lambda state, receptions=need_receptions, books=need_books: state.has_any(receptions, self.player) and state.has_all(books, self.player))


                    print(f"Reception: {reception.name}")
                    print(f"Previous:")
                    for i in need_receptions:
                        print(i)
                    print(f"Books:")
                    for i in need_books:
                        print(i)
                    #print(reception_event.can_reach(self.multiworld.state))
                    print("-----------------")


                    chapter_region.locations.append(reception_event)

                    # Create locations for this reception
                    for j in range(reception.checks):
                        location_name = f"{reception.name} ({j+1})"

                        location = LORLocation(self.player, location_name, locations_name_to_id[location_name], chapter_region)
                        set_rule(location, lambda state: state.has(f"Completed Reception of {reception.name}", self.player))
                        chapter_region.locations.append(location)
            
            # 2.3. Connect previous region with this one and add it to the list of regions
            prev_region.connect(chapter_region)
            self.multiworld.regions.append(chapter_region)

            prev_region = chapter_region






        # 3.1. Generate "Engame" Sphere with "Ensemble", "Black Silence" and "Distorted Ensemble" goals
        endgame_region = Region("Endgame", self.player, self.multiworld)

        #for group in [group for group in self.used_reception_groups if group.chapter == 8]:
        #    reception = receptions_dict[group.receptions[0]]
        #    
        #    # Create event location for this endgoal
        #    endgoal_event = LORLocation(self.player, reception.name, None, endgame_region)
        #    endgoal_event.place_locked_item(self.create_event(f"Completed Reception of {reception.name}"))
        #    endgame_region.locations.append(endgoal_event)
        #
        #    # Create locations for this endgoal TODO

        # 3.2. Add Rules for accessing Endgame with certain settings


        # 3.3. Add Rules for game completion
        #temp_event = LORLocation(self.player, "TEST EVENT", None, endgame_region)
        #temp_event.place_locked_item(self.create_event("Endgoal Completed"))
        #endgame_region.locations.append(temp_event)

        victory_event = LORLocation(self.player, "Game Completed", None, endgame_region)
        victory_event.place_locked_item(self.create_event("One Perfect Book Achieved"))

        # Find last reception in the tree
        last_group = [g for g in self.reception_groups if 999 in g.next_groups][0]
        last_reception = receptions_dict[last_group.receptions[-1]]
        set_rule(victory_event, lambda state: state.has(f"Completed Reception of {last_reception.name}", self.player))

        endgame_region.locations.append(victory_event)

        # 3.4. Connect Endgame Region with either Menu Region or Chapter 7
        prev_region.connect(endgame_region)
        self.multiworld.regions.append(endgame_region)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("One Perfect Book Achieved", self.player)

        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

        return

        # 2.1. Generate Chapter Spheres with receptions
        prev_region = menu
        for i in range(1,8): # Chapters 1-7
            chapter_region = Region(f"Chapter {i}", self.player, self.multiworld)
            groups = [group for group in self.used_reception_groups if group.chapter == i]

            # 2.2. Go through receptions in every group to create locations associated with them
            for group in groups:
                for rid in group.receptions:
                    index = group.receptions.index(rid)
                    reception = receptions_dict[rid]

                    # Create event location for this reception
                    reception_event = LORLocation(self.player, reception.name, None, chapter_region)
                    reception_event.place_locked_item(self.create_event(f"Completed Reception of {reception.name}"))

                    # Rule: Can only access (complete) this reception depending on settings either if one of previous receptions was completed or this plus available Archipelago Book
                    prev_locations = []
                    if index > 0:
                        # Check if this reception has previous receptions in same group
                        prev_locations = [f"Completed Reception of {receptions_dict[group.receptions[index-1]].name}"]
                    else:
                        # If it's the first (or the only) reception of the group, we check last receptions of previous groups
                        prev_locations = [f"Completed Reception of {receptions_dict[[x for x in self.used_reception_groups if x.id == g][0].receptions[-1]].name}" for g in group.prev_groups]

                    if self.options.receptions_progression.value == 1:
                        # To Access this reception you have to be able to beat (access) one of previous receptions
                        set_rule(reception_event, lambda state: state.has_any(prev_locations, self.player) if len(prev_locations) > 0 else True)
                    elif self.options.receptions_progression.value == 2:
                        for o in prev_locations:
                            print(o)
                        # If configured, you also have to have atleast one Archipelago Book
                        set_rule(reception_event, lambda state: 
                                 (state.has_any(prev_locations, self.player) if len(prev_locations) > 0 else state.can_reach_region("Menu"))
                                 )#and logic.can_send_invitation(state, self.player))
                    
                    chapter_region.locations.append(reception_event)

                    # Create locations for this reception
                    for j in range(reception.checks):
                        location_name = f"{reception.name} ({j+1})"

                        location = LORLocation(self.player, location_name, locations_name_to_id[location_name], chapter_region)
                        set_rule(location, lambda state: state.has(f"Completed Reception of {reception.name}", self.player))
                        chapter_region.locations.append(location)
            
            # 2.3. Connect previous region with this one and add it to the list of regions
            prev_region.connect(chapter_region)
            self.multiworld.regions.append(chapter_region)

            prev_region = chapter_region


        # 3.1. Generate "Engame" Sphere with "Ensemble", "Black Silence" and "Distorted Ensemble" goals
        endgame_region = Region("Endgame", self.player, self.multiworld)

        for group in [group for group in self.used_reception_groups if group.chapter == 8]:
            reception = receptions_dict[group.receptions[0]]
            
            # Create event location for this endgoal
            endgoal_event = LORLocation(self.player, reception.name, None, endgame_region)
            endgoal_event.place_locked_item(self.create_event(f"Completed Reception of {reception.name}"))
            endgame_region.locations.append(endgoal_event)

            # Create locations for this endgoal TODO

        # 3.2. Add Rules for accessing Endgame with certain settings


        # 3.3. Add Rules for game completion
        temp_event = LORLocation(self.player, "TEST EVENT", None, endgame_region)
        temp_event.place_locked_item(self.create_event("Endgoal Completed"))
        endgame_region.locations.append(temp_event)

        victory_event = LORLocation(self.player, "Light Recollected", None, endgame_region)
        victory_event.place_locked_item(self.create_event("Light Recollected"))

        endgame_region.locations.append(victory_event)

        # 3.4. Connect Endgame Region with either Menu Region or Chapter 7
        menu.connect(endgame_region)
        self.multiworld.regions.append(endgame_region)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Light Recollected", self.player)

        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

        return



        # 2. Generate Chapter Spheres with receptions
        prev_region = menu
        for i in range (1,8):
            chapter_region = Region(f"Chapter {i}", self.player, self.multiworld)

            groups = [group for group in self.used_reception_groups if group.chapter == i]

            for group in groups:
                for r in group.receptions:
                    reception = receptions_dict[r]
                
                    # Create event for completing this reception (being able to access it)
                    #loc_event = LORLocation(self.player, reception.name, None, chapter_region)
                    #loc_event.place_locked_item(self.create_event(f"Completed Reception of {reception.name}"))

                    #prev_locations = []
                    #if group.receptions.index(r) > 0:
                    #    # Check if this reception has previous receptions in same group
                    #    prev_locations = [f"Completed Reception of {receptions_dict[group.receptions[group.receptions.index(r)-1]].name}"]
                    #else:
                    #    # If it's the first (or the only) reception of the group, we check last receptions of previous groups
                    #    prev_locations = [f"Completed Reception of {receptions_dict[[x for x in self.used_reception_groups if x.id == g][0].receptions[-1]].name}" for g in group.prev_groups]

                    #if self.options.receptions_progression.value == 1:
                    #    # To Access this reception you have to be able to beat (access) one of previous receptions
                    #    set_rule(loc_event, lambda state: state.has_any(prev_locations, self.player))
                    #elif self.options.receptions_progression.value == 2:
                    #    # If configured, you also have to have atleast one unused Archipelago Book
                    #    pass
                    #    #set_rule(loc_event, lambda state: state.has_any(prev_locations, self.player)) # and logic.can_send_invitation(state, self.player))
                    #
                    #chapter_region.locations.append(loc_event)


                    # Create locations for checks
                    for k in range(reception.checks):
                        loc_name = f"{reception.name} ({k+1})"
                        location = LORLocation(self.player, loc_name, locations_name_to_id[loc_name], chapter_region)

                        # Reception items can only be accessed if reception is completed (can be accessed/completed)
                        set_rule(location, lambda state: True ) #state.has(f"Completed Reception of {reception.name}", self.player))

                        chapter_region.locations.append(location)
                        
            print(self.multiworld.state.can_reach_location("Rats (1)", self.player))
            
            prev_region.connect(chapter_region)
            prev_region = chapter_region

            self.multiworld.regions.append(chapter_region)

        # 3. Generate Endgame sphere with every selected endgoal (except Keter realization)
        endgame_region = Region("Endgame", self.player, self.multiworld)

        # Create locations with events and items for every endgoal reception
        for group in [group for group in self.used_reception_groups if group.chapter == 8]:
            reception = receptions_dict[group.receptions[0]]
            
            # Create an event of completing this reception
            #event_loc = LORLocation(self.player, reception.name, None)
            #event_loc.place_locked_item(self.create_event(reception.name))
            #set_rule(event_loc, lambda state: state.has(reception.name+" (1)", self.player))

            # Create locations for checks
            for k in range (reception.checks):
                name = reception.name+" ("+str(k + 1)+")"
                location = LORLocation(self.player, name, locations_name_to_id[name], endgame_region)
                #location.progress_type = LocationProgressType.EXCLUDED

                endgame_region.locations.append(location)
        
        # Endgoal Region Access Logic
        #endgame_entrance = Entrance(self.player, "Endgoal Access", self.options.endgoal_progression.value == 0 and menu or prev_region)
        #if self.options.endgoal_progression.value == 0:
        #    menu.exits.append(endgame_entrance)
        #else:
        #    prev_region.exits.append(endgame_entrance)
        #    set_rule(endgame_entrance, lambda state: state.has(receptions_dict[[group for group in self.used_reception_groups if 999 in group.next_groups][0].receptions[-1]].name, self.player))

        #endgame_entrance.connect(endgame_region)

        menu.connect(endgame_region)

        self.multiworld.regions.append(endgame_region)

        ev = LORLocation(self.player, "Test", None, endgame_region)
        ev.place_locked_item(self.create_event("Endgoal Completion"))
        endgame_region.locations.append(ev)

        # Create logic checks for each Endgoal
        #for g in self.options.end_goals.value:
        #    match g:
        #        case 'Reverberation Ensemble':
        #            receptions = [70001, 70002, 70003, 70004, 70005, 70006, 70007, 70008, 70009, 70010]
        #            for r in receptions:
        #                ensemble_event = LORLocation(self.player, receptions_dict[r].name+" Completion", None)
        #                ensemble_event.place_locked_item(self.create_event("Ensemble Endgoal Progress"))
        #                set_rule(ensemble_event, lambda state: state.has(receptions_dict[r].name, self.player))
        #            event = LORLocation(self.player, "Ensemble Engoal", None)
        #            event.place_locked_item(self.create_event("Endgoal Completion"))
        #            set_rule(event, lambda state: state.has("Ensemble Endgoal Progress", self.player, self.options.ensemble_battles.value))
        #        case 'Black Silence':
        #            event = LORLocation(self.player, "Black Silence Engoal", None)
        #            event.place_locked_item(self.create_event("Endgoal Completion"))
        #            set_rule(event, lambda state: state.has("The Black Silence", self.player))
        #        case 'Distorted Ensemble':
        #            event = LORLocation(self.player, "Distorted Ensemble Engoal", None)
        #            event.place_locked_item(self.create_event("Endgoal Completion"))
        #            set_rule(event, lambda state: state.has("The Reverberation Ensemble Distorted", self.player))
        #        case _:
        #            pass

        # Create main victory event
        victory_event = LORLocation(self.player, "Light Recollected", None, endgame_region)
        victory_event.place_locked_item(self.create_event("Light Recollected"))
        endgame_region.locations.append(victory_event)

        set_rule(victory_event, lambda state: state.has("Endgoal Completion", self.player, len(self.options.end_goals.value)))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Light Recollected", self.player)

    def create_item(self, item: str) -> LORItem:
        data: LORItemData = items_by_name[item]
        return LORItem(item, data.type, data.id, self.player)
    
    def create_event(self, event: str) -> LORItem:
        return LORItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        # Generate the Item Pool
        itempool: list[str] = []

        # Fill item pool with items with already determined amount of copies
        for i in items_by_name.values():
            if i.copies > 0 and i.type_id == "Book":
                itempool += [i.name]*i.copies

        #itempool += ["Book of Everything"]*(total_locations-len(itempool))

        self.multiworld.itempool += map(self.create_item, itempool)

        # Fill item pool with items with already determined amount of copies
        #for i in item_list:
        #    if i.amount > 0:
        #        itempool += [i.name]*i.amount

        # Add certain amount of passive attribution point items
        #itempool += ["Passive Attribution Point"]*self.options.passive_points.value

        # Fill free space in the item pool
        #itempool += ["Book of Everything"]*(len(self.multiworld.get_locations(self.player))-len(itempool))

        #self.multiworld.itempool += map(self.create_item, itempool)

    #def collect(self, state: CollectionState, item: Item) -> bool:
    #    change = super().collect(state, item)
    #    if change:
    #        if "Completed Reception of " in item.name:
    #            state.prog_items[self.player]["Completed Receptions"] += 1
    #        if item.name == "Archipelago Book":
    #            state.prog_items[self.player]["AP Books"] += 1
    #    return change

    #def remove(self, state: CollectionState, item: Item) -> bool:
    #    change = super().remove(state, item)
    #    if change:
    #        if "Completed Reception of " in item.name:
    #            state.prog_items[self.player]["Completed Receptions"] -= 1
    #        if item.name == "Archipelago Book":
    #            state.prog_items[self.player]["AP Books"] -= 1
    #    return change

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
    