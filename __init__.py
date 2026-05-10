import typing
import time
import logging

from . import logic
from .options import LOROptions
from .items import LORItem, LORItemData, items_by_id, items_by_name, items_by_category, items_name_to_id
from .locations import LORLocation, LORSetupResult, ProgressionNode, setup_locations, locations_name_to_id
from .gamedata.receptions import endgoal_receptions
from .gamedata.floors import Floor
from .gamedata.books import books_dict, books_by_name
from worlds.AutoWorld import World
from worlds.generic.Rules import set_rule
from BaseClasses import Item, ItemClassification, Region, LocationProgressType


class LORWorld(World):
    game = "Library of Ruina"
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True
    explicit_indirect_conditions = False

    item_name_to_id = items_name_to_id
    location_name_to_id = locations_name_to_id

    setup_result: LORSetupResult = None
    floors: list[Floor] = []

    logger = logging.getLogger()

    def _option_enabled(self, option_name: str) -> bool:
        option = getattr(self.options, option_name)
        return bool(getattr(option, "value", option))


    @property
    def reception_tree(self):
        return self.setup_result.tree

    @property
    def progression_nodes(self) -> list[ProgressionNode]:
        return self.setup_result.progression_nodes

    @property
    def progression_edges(self) -> list[tuple[str, str]]:
        return self.setup_result.progression_edges

    def _selected_endgoal_receptions(self):
        selected_goals = set(self.options.endgoals.value)
        selected_nodes = []

        for node in endgoal_receptions:
            if node.id >= 70001 and node.id <= 70010:
                if "Reverberation Ensemble" in selected_goals:
                    ensemble_limit = int(self.options.ensemble_battles.value)
                    if len([n for n in selected_nodes if n.id >= 70001 and n.id <= 70010]) < ensemble_limit:
                        selected_nodes.append(node)
                continue

            if node.id == 60003 and "Black Silence" in selected_goals:
                selected_nodes.append(node)
                continue

            if node.id == 60004 and "Distorted Ensemble" in selected_goals:
                selected_nodes.append(node)

        return selected_nodes

    def generate_early(self) -> None:
        # Set Randomization Seed
        if self.options.random_seed.value < 0:
            self.options.random_seed.value = int(time.time())

        self.random.seed(self.options.random_seed.value)

        self.setup_result = setup_locations(self.random, self.options)
        self.floors = self.setup_result.floors

        # Precollect unlocked floors
        if self.options.lock_floors.value:
            floor = items_by_category["FloorUnlock"][
                self.random.randint(0, 9) if self.options.starting_floor.value >= 10 else self.options.starting_floor.value
            ].name
            self.multiworld.push_precollected(self.create_item(floor))
            items_by_name[floor].copies = 0
            self.logger.info(floor)
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
        for _ in range(self.options.starting_passive_points_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Attribution Points"))

        # Precollect "Passive Limits Break" items
        for _ in range(self.options.starting_passive_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Limits Break"))

        # Precollect "Emotion Limits Break" items
        for _ in range(self.options.starting_emotion_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Emotion Limits Break"))

        # Precollect or add to the pool the "Combat Page Exclusiveness Remove" item
        if self.options.remove_exclusive.value == 1:
            items_by_name["Combat Page Exclusiveness Removal"].copies = 1
        else:
            self.multiworld.push_precollected(self.create_item("Combat Page Exclusiveness Removal"))
            items_by_name["Combat Page Exclusiveness Removal"].copies = 0

        if self.options.randomize_black_silence_page.value:
            items_by_name["The Black Silence's Page"].copies = 1
            items_by_name["The Black Silence's Page"].type = ItemClassification.progression
        else:
            items_by_name["The Black Silence's Page"].copies = 0

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        nodes_by_key = {node.key: node for node in self.progression_nodes}

        for pnode in self.progression_nodes:
            region = Region(pnode.name, self.player, self.multiworld)

            for i in range(pnode.source.checks):
                location_name = f"{pnode.name} ({i + 1})"
                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], region)
                set_rule(location, self._make_location_access_rule(pnode))
                region.locations.append(location)

                if pnode.id == self.reception_tree.first_reception and pnode.kind == "reception":
                    location.progress_type = LocationProgressType.PRIORITY
                    if self.options.balance_book_requirements.value:
                        location.item_rule = lambda item: not item.name in books_by_name or books_by_name[item.name].chapter < 6

            self.multiworld.regions.append(region)


        if not self.options.randomize_black_silence_page.value:
            self.multiworld.get_location("Oliver (1)", self.player).place_locked_item(
                self.create_item("The Black Silence's Page")
            )

        first_node = nodes_by_key[f"reception:{self.reception_tree.first_reception}"]
        menu.connect(self.multiworld.get_region(first_node.name, self.player))

        for source_key, target_key in self.progression_edges:
            source_node = nodes_by_key[source_key]
            target_node = nodes_by_key[target_key]
            source_region = self.multiworld.get_region(source_node.name, self.player)
            target_region = self.multiworld.get_region(target_node.name, self.player)

            entrance = source_region.connect(target_region)
            set_rule(entrance, self._make_access_rule(target_node))

        endgame = Region("Endgame", self.player, self.multiworld)

        for node in endgoal_receptions:
            for i in range(node.checks):
                location_name = f"{node.name} ({i + 1})"
                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], endgame)
                location.progress_type = LocationProgressType.EXCLUDED
                endgame.locations.append(location)

        victory_event = LORLocation(self.player, "Game Completed", None, endgame)
        victory_event.place_locked_item(self.create_event("One Perfect Book Achieved"))
        endgame.locations.append(victory_event)

        self.multiworld.completion_condition[self.player] = lambda state: state.has("One Perfect Book Achieved", self.player)

        last_node = nodes_by_key[f"reception:{self.reception_tree.last_reception}"]
        last_region = self.multiworld.get_region(last_node.name, self.player)
        last_region.connect(endgame)

        self.multiworld.regions.append(endgame)

    def _node_requirements_met(self, state, pnode: ProgressionNode) -> bool:
        book_names = [books_dict[b].name for b in pnode.req_books]

        if not state.has_all(book_names, self.player):
            return False

        if pnode.kind == "stage":
            floor_name = f"{pnode.floor.seph} Floor"
            librarian_name = f"{pnode.floor.seph} Librarian"
            binah_bonus = 1 if pnode.floor.seph == "Binah" and state.has("Binah", self.player) else 0
            return (
                state.has(floor_name, self.player)
                and state.has(librarian_name, self.player, pnode.req_librarians - 1 - binah_bonus)
            )

        return logic.lor_enough_librarians(pnode.req_librarians, state, self.player)

    def _lower_chapter_nodes_clearable(self, state, pnode: ProgressionNode) -> bool:
        for previous_node in self.progression_nodes:
            if previous_node.key == pnode.key or previous_node.chapter >= pnode.chapter:
                continue
            if not state.can_reach(previous_node.name, "Region", self.player):
                return False
            if not self._node_requirements_met(state, previous_node):
                return False
        return True

    def _make_location_access_rule(self, pnode: ProgressionNode):
        def _location_access_rule(state, pnode=pnode):
            return self._lower_chapter_nodes_clearable(state, pnode)

        return _location_access_rule

    def _make_access_rule(self, pnode: ProgressionNode):
        def _access_rule(state, pnode=pnode):
            return self._node_requirements_met(state, pnode)

        return _access_rule

    def create_item(self, item: str) -> LORItem:
        data: LORItemData = items_by_name[item]
        return LORItem(item, data.type, data.id, self.player)

    def create_event(self, event: str) -> LORItem:
        return LORItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        itempool: list[str] = []
        for i in items_by_name.values():
            if i.copies > 0:
                itempool += [i.name] * i.copies

        fillers = ["Book of Everything", "Booster Pack"]
        filler_name = fillers[self.options.filler_items.value]
        itempool += [filler_name] * max(0, total_locations - len(itempool))

        if len(itempool) > total_locations:
            raise Exception(f"LORAP item pool has {len(itempool)} items for only {total_locations} locations")

        self.multiworld.itempool += map(self.create_item, itempool)


    def set_rules(self) -> None:
        pass

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:

        slot_data = self.options.as_dict(
            "random_seed",
            "endgoals",
            "ensemble_battles",
            "abno_page_shuffle",
            "abno_page_randomization",
            "exodia_guaratnee",
            "ego_page_shuffle",
            "receptions_require_books",
            "shuffle_abnos",
            "shuffle_realizations",
            "floors_require_books",
            "randomize_black_silence_page",
            "book_contents_randomization",
            "enemies_turn_into_checks",
            "balance_book_requirements",
        )
        slot_data["randomize_reception_tree"] = 1

        reception_book_requirements = {
            node.id: node.req_books for node in self.reception_tree.reception_nodes
        }
        slot_data["reception_book_requirements"] = reception_book_requirements

        abno_book_requirements: list[list[list[int]]] = []
        abno_fight_order: list[list[int]] = []
        for floor in self.floors:
            stages = [*floor.abno_stages, floor.realization_stage]
            abno_book_requirements.append([stage.req_books for stage in stages])
            abno_fight_order.append([stage.id for stage in stages])
        slot_data["abno_book_requirements"] = abno_book_requirements
        slot_data["abno_fight_order"] = abno_fight_order

        slot_data["first_reception"] = self.reception_tree.first_reception
        slot_data["last_reception"] = self.reception_tree.last_reception

        slot_data["abno_stage_chapters"] = self.setup_result.abno_stage_chapters


        battle_nodes: dict[str, dict] = {}
        for pnode in self.progression_nodes:
            node_data = {
                "id": pnode.id,
                "name": pnode.name,
                "kind": pnode.kind,
                "chapter": pnode.chapter,
                "req_librarians": pnode.req_librarians,
                "visual_x": pnode.visual_x,
                "visual_y": pnode.visual_y,
            }
            if pnode.kind == "stage" and pnode.floor is not None:
                node_data["assigned_floor"] = pnode.floor.id
            battle_nodes[pnode.key] = node_data

        battle_edges = [
            {"source": src, "target": dst} for src, dst in self.progression_edges
        ]

        last_reception_key = f"reception:{self.reception_tree.last_reception}"
        last_node = next(node for node in self.progression_nodes if node.key == last_reception_key)
        selected_goals = self._selected_endgoal_receptions()
        if selected_goals:
            goal_spacing = 250.0
            center = (len(selected_goals) - 1) / 2.0
            for index, goal_node in enumerate(selected_goals):
                offset = index - center
                key = f"endgoal:{goal_node.id}"
                battle_nodes[key] = {
                    "id": goal_node.id,
                    "name": goal_node.name,
                    "kind": "reception",
                    "chapter": goal_node.chapter,
                    "req_librarians": goal_node.req_librarians,
                    "visual_x": round(last_node.visual_x + offset * goal_spacing, 2),
                    "visual_y": round(last_node.visual_y + 360.0 + abs(offset) * 25.0, 2),
                }
                battle_edges.append({"source": last_reception_key, "target": key})

        slot_data["battle_nodes"] = battle_nodes
        slot_data["battle_edges"] = battle_edges

        return slot_data
