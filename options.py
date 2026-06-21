from dataclasses import dataclass

from Options import OptionSet, Range, Choice, PerGameCommonOptions, Toggle, FreeText

# TODO: Add difficulty presets that will automatically configure the YAML to the difficulty the player wants.
# For example: Easy difficulty would set Traps Impact Level to Weak, set Guarantee Exodia Abnormality Sets to True and increase total of Passive and Emotion related items.
# Of course settings can be modified regardless of the preset, those are simply for faster configuration.


### FLOOR-RELATED ###
class LockFloors(Toggle):
    """
    If 'true', every floor except one (Random or preset) is locked at the start of the run and must be unlocked via respective items.
    """

    display_name = "Lock Floors"
    default = True

class StartingFloor(Choice):
    """
    If "Lock Floors" is 'true', select which floor will be unlocked at the start of the run.
    """

    display_name = "Starting Floor"
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
    option_randomized = 10
    default = 10


### ENDGOAL-RELATED
class Endgoals(OptionSet):
    """
    Select Endgoals of a Run.
    You must achieve all of the selected goals, in order for the Run to be completed.
    Goals contain checks which WONT yield any items progression relies on (Mostly only Passive/Emotion upgrades and Book of Everything)
    Goals that are not selected will STILL be accessed in the game and WILL yield checks.
    
    'Reverberation Ensemble' - Defeat X out of 10 Ensemble battles. X can be set in the 'Reverberation Ensemble Goal Receptions' setting.
    'Black Silence' - Complete Reception of The Black Silence.
    'Keter Realization' - Realize the Floor of General Works.
    'Distorted Ensemble' - Complete Reception of The Reverberation Ensemble Distorted.
    """

    display_name = "End Goals"
    default = {"Reverberation Ensemble"}
    valid_keys = {"Reverberation Ensemble", "Black Silence", "Keter Realization", "Distorted Ensemble"}

class EnsembleBattles(Range):
    """
    Select amount of Reverberation Ensemble Receptions you have to complete in order for 'Reverberation Ensemble' goal to be considered completed.
    """
    display_name = "Reverberation Ensemble Goal Receptions"
    range_start = 1
    range_end = 10
    default = 10


### RANDOMIZATION ###
class AbnoPageShuffle(Choice):
    """
    Select the way Abnormality Pages are shuffled.

    None - Abno Pages are not shuffled and are placed exactly like in the vanilla game.
    InFloor - Pages are shuffled in their floors individually.
    Sets - Pages are shuffled between floors in abnormality sets
           (For example 3 of Scorched Girl's pages are gonna end up in the same page group after randomization).
    Pages - Pages are shuffled between floors idividually.
    """

    display_name = "Abnormality Page Shuffle"
    option_none = 0
    option_infloor = 1
    option_sets = 2
    option_pages = 3
    default = 3

class AbnoPageRandomization(Choice):
    """
    Select the way Abnormality Pages are randomized.

    None - Abno Pages retain their vanilla Emotion State, Level and Rate.
    Guarantee - Every stat is randomized, but it is guaranteed that there will be at least: 4 Positive Pages, 4 Negative Pages, 3 Pages of each Emotion Level per floor.
    Unbound - Every stat is randomized, without restrictions.
    """

    display_name = "Abnormality Page Randomization"
    option_none = 0
    option_guarantee = 1
    option_unbound = 2
    default = 2

class ExodiaGuarantee(Toggle):
    """
    If 'Abnormality Page Shuffle' option is set to 'Sets' or 'Pages', forces certain Abno Pages to be on the same floor after randomization:
    'Hate', 'Desair', 'Greed', 'Wrath', 'Nix';
    'Big Eyes', 'Small Beak', 'Long Arms', 'The Beast';
    'Baptism', 'Apostles', 'Advent'.
    
    !!! IMPORTANT: If 'Abnormality Page Shuffle' is set to 'Sets', one of the floors will be forced to have exact same pool of Abno Pages as vanilla Tiphereth floor.
    """
    display_name = "Guarantee Exodia Abnormality Sets"
    default = False

class EGOPageShuffle(Toggle):
    """
    Select if EGO Pages should be shuffled between floors.
    """
    
    display_name = "EGO Page Shuffle"
    default = True

class PageRandomization(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Select the way Key/Combat Pages are randomized.

    None - Key/Combat Pages are not randomized.
    Basic - Game Randomizes: Combat Pages' Dices and effects; Key Pages' HP, Break, Vulnerabilities.
    More - Above and: Combat Pages' Names and CG, Key Pages' Passives.
    Havoc - Above and: Combat Pages' VFX and SFX, Key Pages' visuals.
    """

    display_name = "Key/Combat Page Randomization"
    option_none = 0
    option_basic = 1
    option_more = 2
    option_havoc = 3
    default = 0 

class RandomizeBlackSilencePage(Toggle):
    """
    If 'true', Black Silence Page item's location will be random.
    If 'false', Black Silence Page will be unlocked after completing Reception of Oliver
    """

    display_name = "Randomize Black Silence Page Location"
    default = True

class BookContentsRandomization(Choice):
    """
    Select the way every vanilla book's contents will be randomized.

    BookChapter - Book contents will be balanced around the chapter of the book.
    StageChapter - Book contents will be balanced around the chapter of the reception/suppression/realization they're required in.
    Chaotic - Book contents are fully random.
    """
    display_name = "Book Contents Randomization"
    option_bookchapter = 0
    option_stagechapter = 1
    option_chaotic = 2
    default = 0

class BalanceBookRequirements(Toggle):
    """
    If true, receptions/suppressions/realizations will require books from around their chapters.
    Otherwise, random books will be selected.
    """
    display_name = "Balance Book Requirements"
    default = True

class BookRequirementDensity(Range):
    """
    Controls how many nodes in invitations menu will share same book requirment.

    At 100, every locked battle node receives its own book requirement.
    Lower values makes nearby nodes share the same requirements. At 1, nearly
    the entire graph may be unlocked by the one book.
    """

    display_name = "Book Requirement Density"
    range_start = 1
    range_end = 100
    default = 50

class ShuffleAbnos(Toggle):
    """
    If 'true', Abnormalities will be shuffled between the floors.
    """

    display_name = "Shuffle Abnormalities"
    default = True

class ShuffleRealizations(Toggle):
    """
    If 'true', Realizations will be shuffled between the Floors.
    """

    display_name = "Shuffle Realizations"
    default = True



class CustomLORAPSeed(FreeText):
    """
    Optional custom seed for LORAP-specific generation.

    Leave empty to use Archipelago's normal per-slot random seed.
    If set, the same value with the same options will reproduce the same LORAP battle tree, book requirements, floor shuffle and client-side RNG seed.
    """

    display_name = "Custom LORAP Seed"
    default = ""

class ReceptionsRequireBooks(Toggle):
    """
    If 'true', every reception will require books to send invitation.
    
    Turning this off majorly distorts (heh, get it?) intended progression and has high chance to BK you and/or others.
    """

    display_name = "Receptions Require Books"
    default = True

class FloorsRequireBooks(Toggle):
    """
    If 'true', Abnormality Suppressions and Realizations will require books.

    Turning this off majorly distorts (heh, get it?) intended progression and has high chance to BK you and/or others.
    """
    
    display_name = "Floors Require Books"
    default = True

class EnemiesTurnIntoChecks(Toggle):
    """
    If 'true', you send one item from the reception for each defeated enemy.
    (Completing the reception will still send remaining items)
    (This option simply allows for chipping at the enemies to send items without completing the reception to potentially escape BK)
    """

    display_name = "Enemies Turn Into Checks"
    default = True

### ITEMS###
class PassivePointsItems(Range):
    """
    Select the amount of "Passive Attribution Points" Items you'll be able to acquire in total.
    You always start with 2 Items (Unless configured otherwise) and get 2 Passive Attribution Points for each Item.
    Base amount is 15 Items, meaning up to 34 Passive Attribution Points in-game.

    Do note that adding more of those Items leads to having less free space in the Item Pool,
    potentially lowering the amount of other filler items you'll be able to get.
    """
    display_name = "Passive Attribution Point Items"
    range_start = 0
    range_end = 100
    default = 15

class StartingPassivePointsItems(Range):
    """
    Select the amount of "Passive Attribution Points" Items you are starting with.
    """
    display_name = "Starting Passive Attribution Point Items"
    range_start = 0
    range_end = 100
    default = 2

class PassiveLimitsItems(Range):
    """
    Select the amount of "Passive Limits Break" Items you'll be able to acquire in total.
    You always start with 2 Items (Unless configured otherwise) and get 1 Passive slot for each Item.
    These Items determine how much Passives you'll be able to put on a single Key Page (Not including passives tied to the page itself)
    Base amount is 10 Items, meaning up to 12 Passives attributed in-game.

    Do note that adding more of those Items leads to having less free space in the Item Pool,
    potentially lowering the amount of other filler items you'll be able to get.
    """
    display_name = "Passive Limits Break Items"
    range_start = 0
    range_end = 25
    default = 10

class StartingPassiveLimitsItems(Range):
    """
    Select the amount of "Passive Limits Break" Items you are starting with.
    """
    display_name = "Starting Passive Limits Break Items"
    range_start = 0
    range_end = 25
    default = 2

class EmotionLimitsItems(Range):
    """
    Select the amount of "Emotion Limits Break" Items you'll be able to acquire in total.
    You always start with 0 Items (Unless configured otherwise) and your max Emotion Level increases by 1 for each Item.
    These Items determine the Maximum Emotion Level your librarians can get during receptions.
    Levels past 5 (Vanilla max) give additional small buffs like +1 Light, Page Draw & accasionally a Speed Die.
    That also means that you won't be getting Abno and EGO Pages even if you have them unless your Max Emotion Level is atleast 1 and 3 respectively.
    Base amount is 10 Items, meaning up to 10 Max Emotion Level in-game.

    Do Note that adding more of those Items leads to having less free space in the Item Pool,
    potentially lowering the amount of other filler items you'll be able to get.
    """
    display_name = "Passive Limits Break Items"
    range_start = 0
    range_end = 100
    default = 10

class StartingEmotionLimitsItems(Range):
    """
    Select the amount of "Emotion Limits Break" Items you are starting with.
    """
    display_name = "Starting Passive Limits Break Items"
    range_start = 0
    range_end = 100
    default = 0

class ExclusivenessRemove(Choice):
    """
    Select if "Combat Page Exclusiveness Removal" item should be added to the pool.

    I think option names are self explanatory?
    """
    display_name = "Combat Page Exclusiveness Remova"
    option_dontadd = 0
    option_item = 1
    option_remove = 2
    default = 1

class FillerItems(Choice):
    """
    Select which filler items are going to be in the pool.

    NOTE: Book of Everything doesn't work yet.

    Book of Everything - It's drops adapt to your current progress, giving you pages around your current level.
                         Page rarity has small impact on item weights (Every rarity can drop almost with the same chance).
                         Allows for a more balanced playthrough. Amount of each page dropped is random.
    Booster Packs - Can give you any page in the game no matter when you burn them, but every page is dropped as a single copy,
                    and page weight decreases with rarity drastically (Higher rarity will drop a lot less).
                    Makes playthough a less balanced, and maybe more fun. If you win in the gacha.
    """
    display_name = "Filler Items"
    option_bookofeverything = 0
    option_boosterpacks = 1
    default = 1

class FillerPages(Range):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Select the amount of pages (in %) from burning Filler Items that will turn into Filler Pages.
    Filler Pages are one-time instant use Pages that grant different buffs to your units or debuffs to enemy units
    (Example: Instant use +5 Strength). Filler Pages are only considered used if you win the reception.

    !!! Sum of this and "Traps%" must not exceed 100!
    """

    display_name = "Filler Page%"
    range_start = 0
    range_end = 100
    default = 10

class Traps(Range):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Select the amount of pages (in %) from burning Filler Items that will turn into Traps.
    Traps are different effects that put you in a disadvantage and their
    severeness depends on the "Traps Impact Level" option.

    !!! Sum of this and "Filler Page%" must not exceed 100!
    """

    display_name = "Traps%"
    range_start = 0
    range_end = 100
    default = 5

class TrapsSevereness(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO
    
    Select the severeness level of trap effects.

    Weak - Traps activate as soon as possible (first available Scene), once. Effects are mostly minor inconveniences.
    Mediocre - Traps can activate at the beginning of any Scene from the moment you get them, once. Effects can ruin your plans and be a nuisance for you;
    Dangerous - Traps can activate at any time from the moment you get them (at any point of any scene). They also get tied to the exact Scene and Reception they activated at,
            making it so they are repeated if you restart the reception (by losing or restarting), until you beat that reception.
            This level has the most impactful and invonvenient effects ready to mess up your run.
    """

    display_name = "Traps Severeness"
    option_weak = 0
    option_mediocre = 1
    option_dangerous = 2
    default = 1

### OTHER ###
class Deathlink(Toggle):
    """
    !!!NOT IMPLEMENTED!!! TODO

    If 'true', a deathlink is sent on a condition specified in "Outgoing Deathlink" Option.
    "Incoming Deathlink" option specifies what happens when you receive a deathlink.
    """
    
    display_name = "Deathlink"
    default = False

class OutgoingDeathlink(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO
    
    Select what must happen for a deathlink to be sent.

    UnitDeath - When in a battle and ANY librarian dies, deathlink is sent.
    TeamWipe - When in a battle and ALL librarians on the floor die, deathlink is sent.
    StageLoss - When a battle is lost, deathlink is sent. 
    """

    display_name = "Outgoing Deathlink"
    option_unitdeath = 0
    option_teamwipe = 1
    option_stageloss = 2
    default = 2

class IncomingDeathlink(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO
    
    Select what will happen after receiving a deathlink.

    UnitDeath - After receiving a deathlink while in battle, a random librarian dies.
    TeamWipe - After receiving a deathlink while in battle, all librarians on the floor die.
    StageLoss - After receiving a deathlink while in battle, lose the current battle.
    """

    display_name = "Incoming Deathlink"
    option_unitdeath = 0
    option_teamwipe = 1
    option_stageloss = 2
    default = 0

@dataclass
class LOROptions(PerGameCommonOptions):
    # Floor-Related
    lock_floors: LockFloors
    starting_floor: StartingFloor
    # Endgoal-related
    endgoals: Endgoals
    ensemble_battles: EnsembleBattles
    # Randomization
    abno_page_shuffle: AbnoPageShuffle
    abno_page_randomization: AbnoPageRandomization
    exodia_guaratnee: ExodiaGuarantee
    ego_page_shuffle: EGOPageShuffle
    page_randomization: PageRandomization
    randomize_black_silence_page: RandomizeBlackSilencePage
    book_contents_randomization: BookContentsRandomization
    balance_book_requirements: BalanceBookRequirements
    book_requirement_density: BookRequirementDensity
    custom_lorap_seed: CustomLORAPSeed
    # Progression
    receptions_require_books: ReceptionsRequireBooks
    shuffle_abnos: ShuffleAbnos
    shuffle_realizations: ShuffleRealizations
    floors_require_books: FloorsRequireBooks
    enemies_turn_into_checks: EnemiesTurnIntoChecks
    # Items
    passive_points_items: PassivePointsItems
    starting_passive_points_items: StartingPassivePointsItems
    passive_limits_items: PassiveLimitsItems
    starting_passive_limits_items: StartingPassiveLimitsItems
    emotion_limits_items: EmotionLimitsItems
    starting_emotion_limits_items: StartingEmotionLimitsItems
    remove_exclusive: ExclusivenessRemove
    filler_items: FillerItems
    filler_pages: FillerPages
    traps: Traps
    traps_severeness: TrapsSevereness
    # Other
    deathlink: Deathlink
    outgoing_deathlink: OutgoingDeathlink
    incoming_deathlink: IncomingDeathlink
