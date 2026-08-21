import typing
import logging
import hashlib
import math
import random

from . import logic
from . import options as lor_options
from .options import LOROptions
from .items import LORItem, LORItemData, items_by_name, items_by_category, items_name_to_id
from .locations import LORLocation, LORSetupResult, ProgressionNode, setup_locations, locations_name_to_id
from .gamedata.floors import Floor
from .gamedata.books import books_dict, books
from Options import OptionGroup
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule
from BaseClasses import ItemClassification, Region, LocationProgressType


BOE_BUNDLES_PER_SPHERE = (6, 6, 10, 11, 10, 20, 7)
BOE_POOL_MULTIPLIER = 2
VANILLA_BOOK_LOGIC_MULTIPLIER = 2
SLOT_DATA_VERSION = 3


def _stable_seed_int(*parts: object) -> int:
    text = "|".join(str(part) for part in parts)
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


class LORWebWorld(WebWorld):
    option_groups = [
        OptionGroup("Start and Goals", [
            lor_options.Endgoals,
            lor_options.PersistentGoals,
            lor_options.EnsembleBattles,
            lor_options.EndgoalsAlwaysUnlocked,
            lor_options.LockFloors,
            lor_options.StartingFloor,
        ]),
        OptionGroup("Battle Graph and Progression", [
            lor_options.ProgressionMode,
            lor_options.ChapterClearPercentage,
            lor_options.ReceptionsRequireBooks,
            lor_options.FloorsRequireBooks,
            lor_options.BookRequirementDensity,
            lor_options.BalanceBookRequirements,
            lor_options.EnemiesTurnIntoChecks,
            lor_options.ShortcutConnections,
            lor_options.RandomizeBlackSilencePage,
        ]),
        OptionGroup("Page and Floor Randomization", [
            lor_options.CustomLORAPSeed,
            lor_options.ShuffleAbnos,
            lor_options.ShuffleRealizations,
            lor_options.ShuffleReverbEnsembleFloors,
            lor_options.AbnoPageShuffle,
            lor_options.AbnoPageRandomization,
            lor_options.ExodiaGuarantee,
            lor_options.EGOPageShuffle,
            lor_options.PageRandomization,
        ]),
        OptionGroup("Book Contents and Filler", [
            lor_options.BookContentsRandomization,
            #lor_options.FillerItems,
            lor_options.FillerPages,
            lor_options.ExclusivenessRemove,
        ]),
        OptionGroup("Library Power Items", [
            lor_options.PassivePointsItems,
            lor_options.StartingPassivePointsItems,
            lor_options.PassiveLimitsItems,
            lor_options.StartingPassiveLimitsItems,
            lor_options.EmotionLimitsItems,
            lor_options.StartingEmotionLimitsItems,
        ]),
        OptionGroup("Traps", [
            lor_options.Traps,
            lor_options.TrapsSevereness,
        ]),
        OptionGroup("Death Link", [
            lor_options.Deathlink,
            lor_options.OutgoingDeathlink,
            lor_options.IncomingDeathlink,
        ]),
    ]


class LORWorld(World):
    game = "Library of Ruina"
    web = LORWebWorld()
    options_dataclass = LOROptions
    options: LOROptions
    topology_present = True
    explicit_indirect_conditions = False

    item_name_to_id = items_name_to_id
    location_name_to_id = locations_name_to_id
    item_name_groups = {
        "Vanilla Books": {book.name for book in books},
    }

    setup_result: LORSetupResult = None
    floors: list[Floor] = []
    client_seed: int = 0
    effective_lorap_seed: str = ""
    lorap_random: random.Random = None

    logger = logging.getLogger()


    def _custom_lorap_seed_value(self) -> str:
        option = getattr(self.options, "custom_lorap_seed", "")
        value = getattr(option, "value", option)
        if value is None:
            return ""
        return str(value).strip()

    def _create_lorap_random(self) -> random.Random:
        custom_seed = self._custom_lorap_seed_value()
        if custom_seed:
            self.effective_lorap_seed = custom_seed
        else:
            self.effective_lorap_seed = str(self.random.getrandbits(64))
        return random.Random(_stable_seed_int("LORAP", self.effective_lorap_seed))

    def _option_enabled(self, option_name: str) -> bool:
        option = getattr(self.options, option_name)
        return bool(getattr(option, "value", option))

    def _option_value(self, option_name: str, default: int) -> int:
        option = getattr(self.options, option_name, default)
        return int(getattr(option, "value", option))

    def _boe_layers_enabled(self) -> bool:
        return self._option_value("progression_mode", 0) == 1

    def _boe_bundles_per_sphere(self) -> list[int]:
        return list(BOE_BUNDLES_PER_SPHERE)

    def _boe_bundles_required_through_sphere(self, sphere: int) -> int:
        bundles = self._boe_bundles_per_sphere()
        return sum(bundles[:max(0, min(sphere, len(bundles)))])

    def _actual_vanilla_books_required(self) -> int:
        return max(0, self.setup_result.layer_count - 1)

    def _actual_books_required_for_node(self, node: ProgressionNode) -> int:
        return max(0, node.global_layer)

    def _logic_books_required_for_node(self, node: ProgressionNode) -> int:
        return self._actual_books_required_for_node(node) * VANILLA_BOOK_LOGIC_MULTIPLIER

    @property
    def reception_tree(self):
        return self.setup_result.tree

    @property
    def progression_nodes(self) -> list[ProgressionNode]:
        return self.setup_result.progression_nodes

    @property
    def progression_edges(self) -> list[tuple[str, str]]:
        return self.setup_result.progression_edges

    def _selected_goal_nodes(self) -> list[ProgressionNode]:
        return self.setup_result.selected_goal_nodes

    def _initialize_item_state(self) -> None:
        self.item_copies: dict[str, int] = {name: data.copies for name, data in items_by_name.items()}
        self.item_classifications: dict[str, ItemClassification] = {name: data.type for name, data in items_by_name.items()}

        for book in books:
            self.item_copies[book.name] = 0
            self.item_classifications[book.name] = ItemClassification.filler

        self.item_copies["Book of Everything"] = 0
        self.item_classifications["Book of Everything"] = ItemClassification.filler
        self.item_copies["Booster Pack"] = 0
        self.item_classifications["Booster Pack"] = ItemClassification.filler

        if self._boe_layers_enabled():
            required_boe = self._boe_bundles_required_through_sphere(7)
            self.item_copies["Book of Everything"] = required_boe * BOE_POOL_MULTIPLIER
            self.item_classifications["Book of Everything"] = ItemClassification.progression_skip_balancing

            vanilla_book_pool = self._actual_vanilla_books_required() * VANILLA_BOOK_LOGIC_MULTIPLIER
            book_order = list(books)
            (self.lorap_random or self.random).shuffle(book_order)
            for index in range(vanilla_book_pool):
                book_name = book_order[index % len(book_order)].name
                self.item_copies[book_name] += 1
                self.item_classifications[book_name] = ItemClassification.progression_skip_balancing
        else:
            for book_id in self.setup_result.used_book_requirements:
                book_name = books_dict[book_id].name
                self.item_copies[book_name] = 1
                self.item_classifications[book_name] = ItemClassification.progression

        self.item_copies["Passive Attribution Points"] = int(self.options.passive_points_items.value)
        self.item_copies["Passive Limits Break"] = int(self.options.passive_limits_items.value)
        self.item_copies["Emotion Limits Break"] = int(self.options.emotion_limits_items.value)

        if self.options.randomize_black_silence_page.value:
            self.item_copies["The Black Silence's Page"] = 1
            self.item_classifications["The Black Silence's Page"] = ItemClassification.progression
        else:
            self.item_copies["The Black Silence's Page"] = 0

        if self.options.remove_exclusive.value == 1:
            self.item_copies["Combat Page Exclusiveness Removal"] = 1
        else:
            self.item_copies["Combat Page Exclusiveness Removal"] = 0

    def _precollect_starting_items(self) -> None:
        if self.options.lock_floors.value:
            rng = self.lorap_random or self.random
            floor_index = rng.randint(0, 9) if self.options.starting_floor.value >= 10 else self.options.starting_floor.value
            floor_name = items_by_category["FloorUnlock"][floor_index].name
            self.multiworld.push_precollected(self.create_item(floor_name))
            self.item_copies[floor_name] = 0
            self.logger.info(floor_name)
        else:
            for floor in items_by_category["FloorUnlock"]:
                self.multiworld.push_precollected(self.create_item(floor.name))
                self.item_copies[floor.name] = 0

        for _ in range(self.options.starting_passive_points_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Attribution Points"))

        for _ in range(self.options.starting_passive_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Passive Limits Break"))

        for _ in range(self.options.starting_emotion_limits_items.value):
            self.multiworld.push_precollected(self.create_item("Emotion Limits Break"))

        if self.options.remove_exclusive.value != 1:
            self.multiworld.push_precollected(self.create_item("Combat Page Exclusiveness Removal"))

    def generate_early(self) -> None:
        self.lorap_random = self._create_lorap_random()
        self.client_seed = self.lorap_random.randrange(1, 2 ** 31)
        self.setup_result = setup_locations(self.lorap_random, self.options)
        self.floors = self.setup_result.floors
        self._initialize_item_state()
        self._precollect_starting_items()

    def create_regions(self) -> None:
        self.node_regions: dict[str, Region] = {}
        self.node_entrances: dict[str, list[object]] = {}
        self.edge_entrances: list[tuple[str, str, object]] = []
        self.node_clear_events: dict[str, str] = {}
        self.sphere_clearability_events: dict[int, str] = {}
        self.goal_event_items: list[str] = []
        self.location_nodes: dict[str, ProgressionNode] = {}

        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        nodes_by_key = {node.key: node for node in self.progression_nodes}

        for node in self.progression_nodes:
            region = Region(node.name, self.player, self.multiworld)
            self.node_regions[node.key] = region

            for index in range(node.source.checks):
                location_name = f"{node.name} ({index + 1})"
                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], region)
                if node.id == self.reception_tree.first_reception and node.kind == "reception":
                    location.progress_type = LocationProgressType.PRIORITY
                region.locations.append(location)
                self.location_nodes[location_name] = node

            clear_event = f"{node.name} Cleared"
            clear_location = LORLocation(self.player, clear_event, None, region)
            clear_location.place_locked_item(self.create_event(clear_event))
            region.locations.append(clear_location)
            self.node_clear_events[node.key] = clear_event

            self.multiworld.regions.append(region)

        if self._boe_layers_enabled():
            for sphere in range(1, 7):
                event_name = f"Sphere {sphere} Fully Clearable"
                event_location = LORLocation(self.player, event_name, None, menu)
                event_location.place_locked_item(self.create_event(event_name))
                menu.locations.append(event_location)
                self.sphere_clearability_events[sphere] = event_name

        first_node = nodes_by_key[f"reception:{self.reception_tree.first_reception}"]
        first_entrance = menu.connect(self.node_regions[first_node.key])
        self.node_entrances.setdefault(first_node.key, []).append(first_entrance)

        for source_key, target_key in self.progression_edges:
            source_region = self.node_regions[source_key]
            target_region = self.node_regions[target_key]
            entrance = source_region.connect(target_region)
            self.node_entrances.setdefault(target_key, []).append(entrance)
            self.edge_entrances.append((source_key, target_key, entrance))

        if not self.options.randomize_black_silence_page.value:
            self.multiworld.get_location("Oliver (1)", self.player).place_locked_item(
                self.create_item("The Black Silence's Page")
            )

        last_node = nodes_by_key[f"reception:{self.reception_tree.last_reception}"]
        goal_hub = Region("Goal Hub", self.player, self.multiworld)
        self.multiworld.regions.append(goal_hub)
        self.node_regions["goal_hub"] = goal_hub
        goal_hub_entrance = menu.connect(goal_hub)
        self.node_entrances.setdefault("goal_hub", []).append(goal_hub_entrance)
        self.edge_entrances.append((last_node.key, "goal_hub", goal_hub_entrance))

        selected_goals = self._selected_goal_nodes()
        for goal_node in selected_goals:
            key = goal_node.key
            region = Region(goal_node.name, self.player, self.multiworld)
            self.node_regions[key] = region

            for index in range(goal_node.source.checks):
                location_name = f"{goal_node.name} ({index + 1})"
                location = LORLocation(self.player, location_name, locations_name_to_id[location_name], region)
                location.progress_type = LocationProgressType.EXCLUDED
                region.locations.append(location)

            event_name = f"{goal_node.name} Goal Completed"
            event_location = LORLocation(self.player, event_name, None, region)
            event_location.place_locked_item(self.create_event(event_name))
            region.locations.append(event_location)
            self.goal_event_items.append(event_name)

            self.multiworld.regions.append(region)
            goal_entrance = goal_hub.connect(region)
            self.node_entrances.setdefault(key, []).append(goal_entrance)
            self.edge_entrances.append(("goal_hub", key, goal_entrance))

        victory_region = Region("Victory", self.player, self.multiworld)
        victory_event = LORLocation(self.player, "Game Completed", None, victory_region)
        victory_event.place_locked_item(self.create_event("One Perfect Book Achieved"))
        victory_region.locations.append(victory_event)
        self.multiworld.regions.append(victory_region)
        victory_entrance = goal_hub.connect(victory_region)
        self.node_entrances.setdefault("victory", []).append(victory_entrance)
        self.edge_entrances.append(("goal_hub", "victory", victory_entrance))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("One Perfect Book Achieved", self.player)

    def _node_requirements_met(self, state, node: ProgressionNode) -> bool:
        if not self._node_book_requirements_met(state, node):
            return False

        if node.kind == "stage":
            floor_name = f"{node.floor.seph} Floor"
            librarian_name = f"{node.floor.seph} Librarian"
            binah_bonus = 1 if node.floor.seph == "Binah" and state.has("Binah", self.player) else 0
            return (
                state.has(floor_name, self.player)
                and state.has(librarian_name, self.player, max(0, node.req_librarians - 1 - binah_bonus))
            )

        return logic.lor_enough_librarians(node.req_librarians, state, self.player)

    def _node_book_requirements_met(self, state, node: ProgressionNode) -> bool:
        if self._boe_layers_enabled():
            return True
        if node.req_books:
            book_names = [books_dict[book_id].name for book_id in node.req_books]
            if not state.has_all(book_names, self.player):
                return False
        return True

    def _layer_access_balancing_enabled(self, node: ProgressionNode) -> bool:
        return node.sphere_layer >= 2

    def _lower_layers_clearable(self, state, node: ProgressionNode) -> bool:
        if not self._layer_access_balancing_enabled(node):
            return True

        for other_node in self.progression_nodes:
            if other_node.sphere == node.sphere and other_node.sphere_layer < node.sphere_layer:
                if not state.can_reach(self.node_clear_events[other_node.key], "Location", self.player):
                    return False
        return True

    def _previous_spheres_clearable(self, state, sphere: int) -> bool:
        for other_node in self.progression_nodes:
            if other_node.sphere < sphere:
                if not state.can_reach(self.node_clear_events[other_node.key], "Location", self.player):
                    return False
        return True

    def _sphere_clear_requirement_met(self, state, sphere: int) -> bool:
        sphere_nodes = [node for node in self.progression_nodes if node.sphere == sphere]
        if not sphere_nodes:
            return True

        clear_percentage = max(0, min(100, self._option_value("sphere_clear_percentage", 50)))
        required = math.ceil(len(sphere_nodes) * clear_percentage / 100)
        if required <= 0:
            return True

        cleared = sum(
            1 for node in sphere_nodes
            if state.has(self.node_clear_events[node.key], self.player)
        )
        return cleared >= required

    def _make_node_access_rule(self, node: ProgressionNode):
        def access_rule(state, node=node):
            return self._node_requirements_met(state, node)
        return access_rule

    def _make_edge_access_rule(self, source_key: str, target_key: str):
        nodes_by_key = {node.key: node for node in self.progression_nodes}
        target_node = nodes_by_key.get(target_key)
        source_event = self.node_clear_events.get(source_key)

        def access_rule(state, target_node=target_node, source_event=source_event):
            if self._boe_layers_enabled():
                if target_node is not None:
                    if not self._node_requirements_met(state, target_node):
                        return False
                    required_books = self._actual_books_required_for_node(target_node)
                    if not state.has_group("Vanilla Books", self.player, required_books):
                        return False
                if (source_key, target_key) in self.setup_result.transition_edges:
                    source_node = nodes_by_key.get(source_key)
                    if source_node is not None and not self._sphere_clear_requirement_met(state, source_node.sphere):
                        return False
                    required_boe = self._boe_bundles_required_through_sphere(source_node.sphere)
                    if not state.has("Book of Everything", self.player, required_boe):
                        return False
                return True

            if source_event is not None and not state.has(source_event, self.player):
                return False
            if target_node is not None and not self._node_requirements_met(state, target_node):
                return False
            if (
                target_node is not None
                and (source_key, target_key) in self.setup_result.transition_edges
                and not self._previous_spheres_clearable(state, target_node.sphere)
            ):
                return False
            return True

        return access_rule

    def _make_layer_location_rule(self, node: ProgressionNode, previous_rule):
        def access_rule(state, node=node, previous_rule=previous_rule):
            return previous_rule(state) and self._lower_layers_clearable(state, node)

        return access_rule

    def _make_goal_hub_rule(self):
        oliver_key = f"reception:{self.reception_tree.last_reception}"
        oliver_event = self.node_clear_events.get(oliver_key)
        always_unlocked = self._option_enabled("endgoals_always_unlocked")

        def access_rule(state, oliver_event=oliver_event, always_unlocked=always_unlocked):
            if always_unlocked:
                return True
            if oliver_event is not None and not state.has(oliver_event, self.player):
                return False
            return True

        return access_rule

    def _make_endgoal_access_rule(self, node: ProgressionNode):
        def access_rule(state, node=node):
            return self._node_requirements_met(state, node)

        return access_rule

    def _make_boe_sphere_location_rule(self, node: ProgressionNode, previous_rule):
        required_boe = self._boe_bundles_required_through_sphere(node.sphere - 1)
        previous_sphere_event = self.sphere_clearability_events.get(node.sphere - 1)

        def access_rule(
            state,
            required_boe=required_boe,
            previous_rule=previous_rule,
            previous_sphere_event=previous_sphere_event,
        ):
            if not previous_rule(state):
                return False
            if not state.has("Book of Everything", self.player, required_boe):
                return False
            return previous_sphere_event is None or state.has(previous_sphere_event, self.player)

        return access_rule

    def _make_sphere_clearability_event_rule(self, sphere: int):
        sphere_locations = tuple(
            location_name for location_name, node in self.location_nodes.items()
            if node.sphere == sphere
        )

        def access_rule(state, sphere_locations=sphere_locations):
            return all(
                state.can_reach(location_name, "Location", self.player)
                for location_name in sphere_locations
            )

        return access_rule

    def _make_layer_item_location_rule(self, node: ProgressionNode, previous_rule):
        required_books = self._logic_books_required_for_node(node)

        def access_rule(state, required_books=required_books, previous_rule=previous_rule):
            return previous_rule(state) and state.has_group("Vanilla Books", self.player, required_books)

        return access_rule

    def _make_goal_progression_rule(self, previous_rule):
        required_books = self._actual_vanilla_books_required()
        required_boe = self._boe_bundles_required_through_sphere(7)

        def access_rule(state, previous_rule=previous_rule):
            return (
                previous_rule(state)
                and state.has_group("Vanilla Books", self.player, required_books)
                and state.has("Book of Everything", self.player, required_boe)
            )

        return access_rule

    def _make_victory_rule(self):
        def victory_rule(state):
            return state.has_all(self.goal_event_items, self.player)
        return victory_rule

    def create_item(self, item: str) -> LORItem:
        data: LORItemData = items_by_name[item]
        classification = getattr(self, "item_classifications", {}).get(item, data.type)
        return LORItem(item, classification, data.id, self.player)

    def create_event(self, event: str) -> LORItem:
        return LORItem(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        itempool: list[str] = []
        for item_name, copies in self.item_copies.items():
            if copies > 0:
                itempool.extend([item_name] * copies)

        filler_name = "Booster Pack" # if self._boe_layers_enabled() else ["Book of Everything", "Booster Pack"][self.options.filler_items.value]
        itempool.extend([filler_name] * max(0, total_locations - len(itempool)))

        if len(itempool) > total_locations:
            raise Exception(f"LORAP item pool has {len(itempool)} items for only {total_locations} locations")

        self.multiworld.itempool += [self.create_item(item_name) for item_name in itempool]

    def _book_requirement_chapters(self) -> dict[str, int]:
        requirement_chapters: dict[str, int] = {}

        for node in self.progression_nodes:
            for book_id in node.req_books:
                book_name = books_dict[book_id].name
                if book_name not in requirement_chapters:
                    requirement_chapters[book_name] = node.chapter
                else:
                    requirement_chapters[book_name] = min(requirement_chapters[book_name], node.chapter)

        return requirement_chapters

    def _is_book_location_allowed(self, item, node: ProgressionNode, requirement_chapters: dict[str, int]) -> bool:
        if item.player != self.player:
            return True

        required_chapter = requirement_chapters.get(item.name)
        if required_chapter is None:
            return True

        maximum_chapter = min(7, required_chapter + (1 if required_chapter <= 2 else 2))
        return node.chapter <= maximum_chapter

    def _make_book_item_rule(self, node: ProgressionNode, previous_item_rule, requirement_chapters: dict[str, int]):
        def item_rule(item):
            return previous_item_rule(item) and self._is_book_location_allowed(item, node, requirement_chapters)

        return item_rule

    def _set_book_placement_rules(self) -> None:
        if self._boe_layers_enabled():
            return
        if not self._option_enabled("balance_book_requirements"):
            return

        requirement_chapters = self._book_requirement_chapters()
        if not requirement_chapters:
            return

        for location_name, node in self.location_nodes.items():
            location = self.multiworld.get_location(location_name, self.player)
            location.item_rule = self._make_book_item_rule(node, location.item_rule, requirement_chapters)

    def _set_boe_sphere_location_rules(self) -> None:
        if not self._boe_layers_enabled():
            return

        for location_name, node in self.location_nodes.items():
            if node.sphere <= 1:
                continue

            location = self.multiworld.get_location(location_name, self.player)
            set_rule(location, self._make_boe_sphere_location_rule(node, location.access_rule))

    def _set_boe_sphere_clearability_event_rules(self) -> None:
        if not self._boe_layers_enabled():
            return

        for sphere, event_name in self.sphere_clearability_events.items():
            event_location = self.multiworld.get_location(event_name, self.player)
            set_rule(event_location, self._make_sphere_clearability_event_rule(sphere))

    def _set_layer_location_rules(self) -> None:
        if self._boe_layers_enabled():
            for location_name, node in self.location_nodes.items():
                location = self.multiworld.get_location(location_name, self.player)
                set_rule(location, self._make_layer_item_location_rule(node, location.access_rule))
            return

        for location_name, node in self.location_nodes.items():
            if not self._layer_access_balancing_enabled(node):
                continue

            location = self.multiworld.get_location(location_name, self.player)
            set_rule(location, self._make_layer_location_rule(node, location.access_rule))

        for node in self.progression_nodes:
            if not self._layer_access_balancing_enabled(node):
                continue

            clear_location = self.multiworld.get_location(self.node_clear_events[node.key], self.player)
            set_rule(clear_location, self._make_layer_location_rule(node, clear_location.access_rule))

    def _set_boe_goal_location_rules(self) -> None:
        if not self._boe_layers_enabled():
            return

        for key, region in self.node_regions.items():
            if key.startswith("endgoal:") or key == "victory":
                for location in region.locations:
                    set_rule(location, self._make_goal_progression_rule(location.access_rule))

        for location_name in self.goal_event_items:
            location = self.multiworld.get_location(location_name, self.player)
            set_rule(location, self._make_goal_progression_rule(location.access_rule))

    def set_rules(self) -> None:
        first_key = f"reception:{self.reception_tree.first_reception}"

        for source_key, target_key, entrance in self.edge_entrances:
            if target_key == "goal_hub":
                set_rule(entrance, self._make_goal_hub_rule())
            elif target_key == "victory":
                set_rule(entrance, self._make_victory_rule())
            elif target_key.startswith("endgoal:"):
                goal_node = next(node for node in self._selected_goal_nodes() if node.key == target_key)
                set_rule(entrance, self._make_endgoal_access_rule(goal_node))
            elif target_key != first_key:
                set_rule(entrance, self._make_edge_access_rule(source_key, target_key))

        self._set_book_placement_rules()
        self._set_layer_location_rules()
        self._set_boe_sphere_location_rules()
        self._set_boe_sphere_clearability_event_rules()
        self._set_boe_goal_location_rules()

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        slot_data = self.options.as_dict(
            "endgoals",
            "persistent_goals",
            "ensemble_battles",
            "abno_page_shuffle",
            "abno_page_randomization",
            "exodia_guarantee",
            "ego_page_shuffle",
            #"receptions_require_books",
            #"shuffle_abnos",
            #"shuffle_realizations",
            #"floors_require_books",
            # "randomize_black_silence_page",
            "book_contents_randomization",
            "shuffle_ensemble_floor",
            "enemies_turn_into_checks",
            "endgoals_always_unlocked",
            "balance_book_requirements",
            "book_requirement_density",
            #"shortcut_connections",
            "progression_mode",
            "chapter_clear_percentage",
            "deathlink",
            "outgoing_deathlink",
            "incoming_deathlink",
        )
        # slot_data["randomize_reception_tree"] = 1
        slot_data["lorap_client_seed"] = self.client_seed
        slot_data["slot_data_version"] = SLOT_DATA_VERSION
        # slot_data["effective_lorap_seed"] = self.effective_lorap_seed

        slot_data["reception_book_requirements"] = {
            node.id: node.req_books for node in self.reception_tree.reception_nodes
        }

        abno_book_requirements: list[list[list[int]]] = []
        abno_fight_order: list[list[int]] = []
        included_stage_ids = {
            node.id for node in [*self.progression_nodes, *self._selected_goal_nodes()]
            if node.kind == "stage"
        }
        for floor in self.floors:
            stages = [
                stage for stage in [*floor.abno_stages, floor.realization_stage]
                if stage.id in included_stage_ids
            ]
            abno_book_requirements.append([stage.req_books for stage in stages])
            abno_fight_order.append([stage.id for stage in stages])
        slot_data["abno_book_requirements"] = abno_book_requirements
        slot_data["abno_fight_order"] = abno_fight_order

        slot_data["first_reception"] = self.reception_tree.first_reception
        slot_data["last_reception"] = self.reception_tree.last_reception
        slot_data["abno_stage_chapters"] = self.setup_result.abno_stage_chapters
        slot_data["boe_bundles_per_sphere"] = self._boe_bundles_per_sphere() if self._boe_layers_enabled() else [0] * 7
        slot_data["boe_bundles_cumulative"] = [
            self._boe_bundles_required_through_sphere(sphere)
            for sphere in range(1, 8)
        ] if self._boe_layers_enabled() else [0] * 7
        slot_data["boe_required_total"] = self._boe_bundles_required_through_sphere(7) if self._boe_layers_enabled() else 0
        slot_data["boe_pool_total"] = self.item_copies["Book of Everything"]
        slot_data["layer_count"] = self.setup_result.layer_count
        slot_data["vanilla_books_required_total"] = self._actual_vanilla_books_required() if self._boe_layers_enabled() else 0
        slot_data["vanilla_books_pool_total"] = (
            self._actual_vanilla_books_required() * VANILLA_BOOK_LOGIC_MULTIPLIER
            if self._boe_layers_enabled() else 0
        )
        slot_data["vanilla_books_required_per_layer"] = (
            list(range(self.setup_result.layer_count)) if self._boe_layers_enabled() else []
        )
        slot_data["vanilla_books_logic_per_layer"] = (
            [layer * VANILLA_BOOK_LOGIC_MULTIPLIER for layer in range(self.setup_result.layer_count)]
            if self._boe_layers_enabled() else []
        )

        battle_nodes: dict[str, dict] = {}
        for node in self.progression_nodes:
            node_data = {
                "id": node.id,
                "name": node.name,
                "kind": node.kind,
                "chapter": node.chapter,
                "sphere": node.sphere,
                "sphere_layer": node.sphere_layer,
                "global_layer": node.global_layer,
                "req_librarians": node.req_librarians,
                #"visual_x": node.visual_x,
                #"visual_y": node.visual_y,
            }
            if node.kind == "stage" and node.floor is not None:
                node_data["assigned_floor"] = node.floor.id
            battle_nodes[node.key] = node_data

        battle_edges = [
            {
                "source": source,
                "target": target,
                "transition": (source, target) in self.setup_result.transition_edges,
            }
            for source, target in self.progression_edges
        ]

        last_reception_key = f"reception:{self.reception_tree.last_reception}"
        #last_node = next(node for node in self.progression_nodes if node.key == last_reception_key)
        selected_goals = self._selected_goal_nodes()
        if selected_goals:
            #goal_spacing = 250.0
            center = (len(selected_goals) - 1) / 2.0
            for index, goal_node in enumerate(selected_goals):
                offset = index - center
                key = goal_node.key
                node_data = {
                    "id": goal_node.id,
                    "name": goal_node.name,
                    "kind": goal_node.kind,
                    "chapter": goal_node.chapter,
                    "sphere": 8,
                    "sphere_layer": 0,
                    "global_layer": self.setup_result.layer_count - 1,
                    "req_librarians": goal_node.req_librarians,
                    #"visual_x": round(last_node.visual_x + offset * goal_spacing, 2),
                    #"visual_y": round(last_node.visual_y + 360.0 + abs(offset) * 25.0, 2),
                }
                if goal_node.kind == "stage" and goal_node.floor is not None:
                    node_data["assigned_floor"] = goal_node.floor.id
                battle_nodes[key] = node_data
                battle_edges.append({"source": last_reception_key, "target": key})

        slot_data["battle_nodes"] = battle_nodes
        slot_data["battle_edges"] = battle_edges
        return slot_data
