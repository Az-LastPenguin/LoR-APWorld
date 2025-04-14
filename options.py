from dataclasses import dataclass

from Options import OptionSet, Range, Choice, PerGameCommonOptions, Toggle

class Fillers(Range):
    """
    !!!NOT IMPLEMENTED!!!TODO

    Amount of pages from books that get replaced with filler items.
    """

    display_name = "Filler Item%"
    range_start = 0
    range_end = 20
    default = 10

class Traps(Range):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Amount of filler items that get replaced by a trap.
    """

    display_name = "Trap Item%"
    range_start = 0
    range_end = 20
    default = 10

class TrapsDifficulty(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO
    
    How miserable will traps make your life feel.

    Easy - Effects activate as soon as possible (first available Scene), one time only. Mostly minor inconveniences;
    Medium - Effects can activate at the beginning of any Scene from the moment you get them, one time only. Some effects are annoying;
    Hard - Effects can activate at any time from the moment you get them (In Reception). They also get tied to the exact Scene and Reception they activated at,
           making it so they're repeated if you restart the reception (by losing or restarting), until you beat that reception.
           (They also don't happen on already beaten Receptions.)
           (Oh and the effects... Let's say, most inconvenient stuff might just happen.)
    """

    display_name = "Traps Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    default = 2

class LockedFloors(Toggle):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Whether or not every floor except one (Random by default) is locked at the start of the run.
    """
    display_name = "Locked Floors"
    default = False

class FirstFloor(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO

    If Locked Floors is On, which floor will be the first one unlocked.
    """
    display_name = "First Unlocked Floor"
    option_malkuth = 0
    option_yesod = 1
    option_hod = 2
    option_netzach = 3
    option_tiphereth = 4
    option_gebura = 5
    option_chesed = 6
    option_binah = 7
    option_hokma = 8
    option_keter = 9
    option_random = 10
    default = 10

class EndGoals(OptionSet):
    """
    End Goals of a Run.
    You should achieve all of the selected goals, in order to complete the Run.
    Every goal also contains some checks. (Each ensemble battle, Black silence battle, etc.)
    Every goal not selected will STILL be in the game and WILL yield checks, though those checks will not contain
    any item significant to progression (such as a Librarian, Abno Pages, EGO Pages and others). TODO
    
    'Reverberation Ensemble' - Defeat X of 10 Ensemble battles. X can be set in the 'Reverberation Ensemble Goal Battles' setting.
    'Black Silence' - Complete Reception of The Black Silence.
    'Keter Realization' - Realize the Floor of General Works.
    'Distorted Ensemble' - Complete Reception of The Reverberation Ensemble Distorted.
    """

    display_name = "End Goals"
    default = {"Reverberation Ensemble"}
    valid_keys = {"Reverberation Ensemble", "Black Silence", "Keter Realization", "Distorted Ensemble"}

class EnsembleBattles(Range):
    """Amount of Reverberation Ensemble battles you need to defeat, in order to consider 'Reverberation Ensemble' goal completed."""
    display_name = "Reverberation Ensemble Goal Battles"
    range_start = 1
    range_end = 10
    default = 10

class AbnoPageRandomization(Choice):
    """
    The way Abnormality pages are randomized. 

    None - Pages are not randomized. TODO
    InFloorShuffle - Pages order of acquirement is shuffled in their floors. TODO
                     (Example shuffled Malkuth's floor Abno Pages order: Queen Bee, Fairy Festival, Snow White's Apple, Scorched Girl, Happy Teddy Bear)
    Shuffle - Pages are shuffled between the floors, retaining their Emotion State (Positive/Negative), Rate and Emotion Levels. TODO
    VanillaLike - Pages are shuffled between the floors, their Emotion State and Rate are random,
                  Emotion Levels are randomized and distributed like in vanilla. (6 of I, 6 of II, 3 of III per floor)
    GuaranteedRandom - Pages are shuffled between the floors, their Emotion State, Rate and Emotion levels are randomized. It is guaranteed that there will be at least:
                       4 Positive Pages, 4 Negative Pages, 3 Pages of each Emotion Level per floor.
    Random - Pure random. Pages are shuffled, Emotion State, Rate and Emotion Level are randomized.
    """

    display_name = "Abnormality Page Randomization"
    option_none = 0
    option_infloorshuffle = 1
    option_shuffle = 2
    option_vanillalike = 3
    option_guaranteed = 4
    option_random = 5
    default = 4

class ExodiaGuarantee(Toggle):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Has no effect with the following 'Abnormality Page Randomization' settings: None, InFloorShuffle.
    
    If ON, certain sets of Abno Pages will be forced to appear on their vanilla floor with same Emotion State, Rate and Emotion Levels.
    """
    display_name = "Guarantee Exodia Abno Sets"
    default = False

class EGOPageRandomization(Toggle):
    """
    !!!NOT IMPLEMENTED!!! TODO

    If ON, EGO pages will be shuffled between the floors.
    """
    display_name = "Randomize EGO Pages"
    default = True

class DropSystem(Choice):
    """
    They way you get Combat Pages and Key Pages in the game.

    BookOfEverything - Every possible drop from every book from every enemy from every reception seen on the map, all in one book.
                       Chances for everything of same type are the same (Key Page chance = 20%);
    BookOfEverythingBalanced - Same as above, except drops are balanced in a way. The more books you burn, the better will be the drops,
                               meaning in the beginning you're most likely to get first chapters' drops, and dropped pages get progressively better.
    """

    display_name = "Randomizer Drop System"
    option_bookofeverything = 0
    option_bookofeverythingbalanced = 1
    default = 1

class ReceptionsProgression(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO

    The way receptions progress in the game.

    Unlocked - Every Reception is unlocked from the start and receptions are placed just like in the vanilla game.
    Items - Every Reception in chapters 2-7 is locked, and they are unlocked with respective "Reception of X" item. (Kinda Pre 0.4 way)
    Randomized - Receptions are shuffled and randomly placed while having vanilla-like progression (you won't get SotC receptions in the beginning).
                 Receptions are unlocked by completing previous reception. First Reception is ALWAYS Rats.
    RandomizedItems - 'Items' and 'Randomized' Options combined.
    """

    display_name = "Receptions Progression"
    option_unlocked = 0
    option_items = 1
    option_randomized = 2
    option_randomizeditems = 3
    default = 2

class AbnoProgression(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO

    The way Abnormality suppressions/Floor realizations progress in the game

    Vanilla - Abnormality order is exact same as in vanilla.
    Shuffle - Suppressions' order is shuffled in the floor.
    FloorShuffle - Suppressions' order AND floor is shuffled. (Example: The Knight of Despair(Tiphereth II) instead of Singing Machine(Yesod III))
    Random - Same as above, but all Floors' Realizations are also shuffled.
    """

    display_name = "Abnormality Progression"
    option_vanilla = 0
    option_shuffle = 1
    option_floorshuffle = 2
    option_random = 3
    default = 3

class PassivePoints(Range):
    """Amount of Passive Attribution Point items there will be. In-game starting amount is always 8, point items will add +1 to the in-game amount.
    Default amount of those items is 8 due to vanilla max points being 16."""
    display_name = "Passive Attribution Point Items"
    range_start = 0
    range_end = 99
    default = 8

class RandomizePages(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO

    To what degree can pages be randomized.

    None - No page is randomized;
    Basic - Combat Pages' Dices and effects, Key Pages' HP, Break, Vulnerabilities;
    More - Above and: Combat Pages' Names and CG, Key Pages' Passives;
    Havoc - Above and: Combat Pages' VFX and SFX, Key Pages' visuals;
    """

    display_name = "Pages Randomization"
    option_none = 0
    option_basic = 1
    option_more = 2
    option_havoc = 3
    default = 0 


@dataclass
class LOROptions(PerGameCommonOptions):
    fillers: Fillers
    traps: Traps
    traps_difficulty: TrapsDifficulty
    locked_floors: LockedFloors
    first_floor: FirstFloor
    end_goals: EndGoals
    ensemble_battles: EnsembleBattles
    abno_page_randomization: AbnoPageRandomization
    exodia_guaratnee: ExodiaGuarantee
    ego_page_randomization: EGOPageRandomization
    drop_system: DropSystem
    reception_prog: ReceptionsProgression
    abno_prog: AbnoProgression
    passive_points: PassivePoints
    randomize_pages: RandomizePages