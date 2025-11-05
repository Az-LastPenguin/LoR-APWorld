from dataclasses import dataclass

from Options import OptionSet, Range, Choice, PerGameCommonOptions, Toggle

# TODO: Add difficulty presets that will automatically configure the YAML to the difficulty the player wants.
# For example: Easy difficulty would set Traps Impact Level to Weak, set Guarantee Exodia Abnormality Sets to True and increase total of Passive and Emotion related items.
# Of course settings can be modified regardless of the preset, those are simply for faster configuration.


### FILLERS ###
class Fillers(Range):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Select the amount of pages (in %) from burning books that will be replaced with filler items.
    """

    display_name = "Filler Item%"
    range_start = 0
    range_end = 20
    default = 10


### TRAPS ###
class Traps(Range):
    """
    !!!NOT IMPLEMENTED!!! TODO

    Select the amount of filler items (in %) that will be replaced by traps.
    """

    display_name = "Traps Item%"
    range_start = 0
    range_end = 20
    default = 10

class TrapsImpact(Choice):
    """
    !!!NOT IMPLEMENTED!!! TODO
    
    Select the impact level of trap effects.

    Weak - Traps activate as soon as possible (first available Scene), once. Almost not impactful at all.
    Mediocre - Traps can activate at the beginning of any Scene from the moment you get them, once. Can ruin your plans and be a nuisance for you;
    Dangerous - Traps can activate at any time from the moment you get them (at any point of any scene). They also get tied to the exact Scene and Reception they activated at,
            making it so they are repeated if you restart the reception (by losing or restarting), until you beat that reception.
            This level has the most impactful and invonvenient stuff ready to mess up your run.
    """

    display_name = "Traps Impact Level"
    option_weak = 0
    option_mediocre = 1
    option_dangerous = 2
    default = 1


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
    option_random = 10
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
class RandomizationSeed(Range):
    """
    Select Randomization Seed which will be used for randomizing different aspects of the Run.
    Keep it at -1 if you want the Seed to be random.
    """
    display_name = "Randomization Seed"
    range_start = -1
    range_end = 2147483647
    default = -1

class AbnoPageShuffle(Choice):
    """
    Select the way Abnormality Pages are shuffled.

    None - Abno Pages are not shuffled and are placed exactly like in the vanilla game.
    InFloorShuffle - Pages are shuffled in their floors.
    Shuffle - Pages are shuffled between the floors.
    """

    display_name = "Abnormality Page Shuffle"
    option_none = 0
    option_infloorshuffle = 1
    option_shuffle = 2
    default = 2

class AbnoPageRandomization(Choice):
    """
    Select the way Abnormality Pages are randomized.

    None - Abno Pages retain their vanilla Emotion State, Level and Rate.
    VanillaLike - Emotion State and Rate are randomized, Emotion Levels are randomized and distributed like in vanilla game. (6 of I, 6 of II, 3 of III per floor)
    Guarantee - Every stat is randomized, but it is guaranteed that there will be at least: 4 Positive Pages, 4 Negative Pages, 3 Pages of each Emotion Level per floor.
    Random - Every stat is randomized, without restrictions.
    """

    display_name = "Abnormality Page Randomization"
    option_none = 0
    option_vanillalike = 1
    option_guarantee = 2
    option_random = 3
    default = 2

class ExodiaGuarantee(Toggle):
    """
    If "Abnormality Page Shuffle" is set to "Shuffle", and this setting is 'true', certain sets of Abno Pages will be forced 
    to appear on the same floor with vanilla Emotion State, Rate and Emotion Levels (albeit not always in same group of pages).
    """
    display_name = "Guarantee Exodia Abnormality Sets"
    default = False

class EGOPageShuffle(Choice):
    """
    Select the way EGO Pages are shuffled.

    None - EGO Pages are not shuffled and are placed exactly like in the vanilla game.
    InFloorShuffle - EGO Pages' order of acquirement is shuffled in their floors.
    Shuffle - EGO Pages are shuffled between floors.
    """
    
    display_name = "EGO Page Shuffle"
    option_none = 0
    option_infloorshuffle = 1
    option_shuffle = 2
    default = 2

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


### PROGRESSION ###
class RandomizeReceptionTree(Toggle):
    """
    If 'true', reception tree is randomized, with receptions being shuffled and placed randomly, creating a reception tree
    unique for each Seed. First reception is ALWAYS Rats. Last reception is ALWAYS Oliver.
    """

    display_name = "Randomize Reception Tree"
    default = True

class ReceptionsProgression(Choice):
    """
    Select the way receptions progress in the game.

    Unlocked - Every reception is unlocked from the start. Endgoals are also unlocked.
    Progressive - Every reception is locked except one at the start. To unlock next receptions you have to complete one of the previous ones. Completing last
        reception in the reception tree unlocks access to the endgoals.
    ProgressiveBooks - Every reception is locked except one at the start. To unlock a reception you have to complete one of the previous ones and send required books in the invitation.
            Required books are randomized. Endgoal access is same as 'Paths' option.
    """

    display_name = "Receptions Progression"
    option_unlocked = 0
    option_progressive = 1
    option_progressivebooks = 2
    default = 2

class EnemiesTurnIntoChecks(Toggle):
    """
    If 'true', instead of receiving Checks after completing the Reception, You get one check for each defeated enemy.

    If you really hate yourself and want to complete some receptions more than once.
    """

    display_name = "Enemies Turn Into Checks"
    default = True

class AbnoRandomization(Choice):
    """
    Select the way Abnormality suppressions order is randomized in the game.

    None - Abnormality order is exact same as in vanilla.
    InFloorShuffle - Suppressions' order is shuffled in their floors.
    Shuffle - Suppressions' are shuffled between the floors. (Example: The Knight of Despair(Tiphereth II) instead of Singing Machine(Yesod III))
    """

    display_name = "Abnormality Randomization"
    option_none = 0
    option_infloorshuffle = 1
    option_shuffle = 2
    default = 2

class ShuffleRealizations(Toggle):
    """
    If 'true', Realizations are shuffled between the Floors. (Example: Keter Realization in Binah's Floor)
    """

    display_name = "Realization Randomization"
    default = True

class FloorProgression(Choice):
    """
    Select the way Abnormality Suppressions and Realizations progress.

    AlwaysOpen - Suppressions and Realizations don't have any requirements, you can attempt next stage whenever you want.
    Books - Suppressions and Realizations require certain books.
    """
    
    display_name = "Floor Progression"
    option_alwaysopen = 0
    option_books = 1
    default = 1

class RandomizeBlackSilencePage(Toggle):
    """
    If 'true', Black Silence Page item's location will be random.
    If 'false', Black Silence Page will be unlocked after completing Reception of Oliver
    """

    display_name = "Randomize Black Silence Page Location"
    default = True

### OTHER ###
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
    range_end = 100
    default = 10

class StartingPassiveLimitsItems(Range):
    """
    Select the amount of "Passive Limits Break" Items you are starting with.
    """
    display_name = "Starting Passive Limits Break Items"
    range_start = 0
    range_end = 100
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


@dataclass
class LOROptions(PerGameCommonOptions):
    # Fillers & Traps
    fillers: Fillers
    traps: Traps
    traps_impact: TrapsImpact
    # Floor-Related
    lock_floors: LockFloors
    starting_floor: StartingFloor
    # Endgoal-related
    endgoals: Endgoals
    ensemble_battles: EnsembleBattles
    # Randomization
    random_seed: RandomizationSeed
    abno_page_shuffle: AbnoPageShuffle
    abno_page_randomization: AbnoPageRandomization
    exodia_guaratnee: ExodiaGuarantee
    ego_page_shuffle: EGOPageShuffle
    page_randomization: PageRandomization
    # Progression
    randomize_reception_tree: RandomizeReceptionTree
    receptions_progression: ReceptionsProgression
    enemies_turn_into_checks: EnemiesTurnIntoChecks
    abno_randomization: AbnoRandomization
    shuffle_realizations: ShuffleRealizations
    floor_progression: FloorProgression
    randomize_black_silence_page: RandomizeBlackSilencePage
    # Other
    passive_points_items: PassivePointsItems
    starting_passive_points_items: StartingPassivePointsItems
    passive_limits_items: PassiveLimitsItems
    starting_passive_limits_items: StartingPassiveLimitsItems
    emotion_limits_items: EmotionLimitsItems
    starting_emotion_limits_items: StartingEmotionLimitsItems