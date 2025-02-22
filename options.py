from dataclasses import dataclass

from Options import OptionSet, Range, Choice, PerGameCommonOptions, Toggle

class Fillers(Range):
    """
    !!!NOT IMPLEMENTED!!!

    Amount of pages from books that get replaced with filler items
    """

    display_name = "Filler Item%"
    range_start = 0
    range_end = 20
    default = 10

class Traps(Range):
    """
    !!!NOT IMPLEMENTED!!!

    Amount of filler items that get replaced by a trap
    """

    display_name = "Trap Item%"
    range_start = 0
    range_end = 20
    default = 10

class TrapsDifficulty(Choice):
    """
    !!!NOT IMPLEMENTED!!!
    
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
    !!!NOT IMPLEMENTED!!!

    Whether or not every floor except one (Keter by default) is locked at the start of the run.
    """
    display_name = "Locked Floors"

class RandomFirstFloor(Toggle):
    """
    !!!NOT IMPLEMENTED!!!

    If Locked Floors is On, whether or not to randomize which floor is the only one unlocked.
    """
    display_name = "Random First Floor"

class EndGoals(OptionSet):
    """
    End Goals of a Run.
    You should achieve all of the selected goals, in order to complete the Run.
    Every goal also contains some checks. (Each ensemble battle, Black silence battle, etc.)
    Every goal not selected will STILL be in the game, but will not yield checks. (This isn't implemented yet.)
    
    'Reverberation Ensemble' - Defeat X of 10 Ensemble battles. X can be set in the 'Reverberation Ensemble Goal Battles' setting;
    'Black Silence' - Complete Reception of The Black Silence;
    'Keter Realization' - Realize the Floor of General Works
    'Distorted Ensemble' - Complete Reception of The Reverberation Ensemble Distorted
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

class AbnoPagesBalance(Choice):
    """
    How balanced randomization of Abnormality pages is. 

    Unbalanced - Fully random;
    Balanced - Each floor is guaranteed to have atleast 3 cards of each emotion level;
    Vanilla - Pages are distributed like in vanilla (6 of I, 6 of II, 3 of III).
    """

    display_name = "Abnormality Page Randomization"
    option_unbalanced = 0
    option_balanced = 1
    option_vanilla = 2
    default = 1

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

class RandomizePages(Choice):
    """
    !!!NOT IMPLEMENTED!!!

    To what degree can pages be randomized.

    None - No page is randomized;
    Basic - Combat Pages' Dices and effects, Key Pages' HP, Break, Vulnerabilities;
    More - Above and: Combat Pages' Names and CG, Key Pages' Passives;
    Havoc - Above and: Combat Pages' VFX and SFX, Key Pages' visuals;
    """

    display_name = "Randomize Pages"
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
    random_first_floor: RandomFirstFloor
    end_goals: EndGoals
    ensemble_battles: EnsembleBattles
    abno_page_balance: AbnoPagesBalance
    drop_system: DropSystem
    randomize_pages: RandomizePages