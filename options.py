from dataclasses import dataclass

from Options import OptionSet, Range, Choice, PerGameCommonOptions, Toggle

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


### PROGRESSION ###
class RandomizeReceptionTree(Toggle):
    """
    If 'true', reception tree is randomized, with receptions being shuffled and placed randomly, creating a reception tree
    unique for each Seed. 
    
    First reception is ALWAYS Rats. Last reception is ALWAYS Oliver.
    """

    display_name = "Randomize Reception Tree"
    default = True

#class ReceptionsRequirePrevious(Toggle): # NOTE: Honestly idk, makes my life easier without it.
#    """
#    If 'true', to access a reception you have to complete atleast one of it's previous receptions.
#    """
#
#    display_name = "Receptions Require Previous"
#    default = True

class ReceptionsRequireBooks(Toggle):
    """
    If 'true', every reception will require books to send invitation.
    
    Turning this off majorly distorts (heh, get it?) intended progression and has high chance to BK you and/or others.
    """

    display_name = "Receptions Require Books"
    default = True

#class ReceptionsProgression(Choice):
#    """
#    Select the way receptions progress in the game.
#
#    Unlocked - Every reception is unlocked from the start. Endgoals are also unlocked.
#    Progressive - Every reception is locked except one at the start. To unlock next receptions you have to complete one of the previous ones. Completing last
#                  reception in the reception tree unlocks access to the endgoals.
#    Books - Every reception requires books to send invitation. Endgoals are unlocked. !!!BE AWARE that this setting follows NO logical progression, and you might as well just get Xiao after Rats!!!
#    ProgressiveBooks - Every reception is locked except one at the start. To unlock a reception you have to complete one of the previous ones and send required books in the invitation.
#                       Required books are randomized. Endgoal access is same as 'Paths' option.
#
#    Receptions in Unlocked & Books are represented not in a tree form in-game.
#    """
#
#    display_name = "Receptions Progression"
#    option_unlocked = 0
#    option_progressive = 1
#    option_books = 2
#    option_progressivebooks = 3
#    default = 3

class ShuffleAbnos(Toggle):
    """
    If 'true', Abnormalities will be shuffled between the floors
    """

    display_name = "Shuffle Abnormalities"
    default = True

class ShuffleRealizations(Toggle):
    """
    If 'true', Realizations will be shuffled between the Floors.
    """

    display_name = "Shuffle Realizations"
    default = True

class FloorsRequireBooks(Toggle):
    """
    If 'true', Abnormality Suppressions and Realizations will require books.

    Turning this off majorly distorts (heh, get it?) intended progression and has high chance to BK you and/or others.
    """
    
    display_name = "Floors Require Books"
    default = True

class RandomizeBlackSilencePage(Toggle):
    """
    If 'true', Black Silence Page item's location will be random.
    If 'false', Black Silence Page will be unlocked after completing Reception of Oliver
    """

    display_name = "Randomize Black Silence Page Location"
    default = True

class BalanceBookContents(Toggle):
    """
    If 'true', Every vanilla book's Combat and Key Pages will be balanced around the chapter of the stage they're required in
    or chapter of the highest chapter stage available.
    
    This setting will default drops to chapter of the book in vanilla game if it's not required in floor/reception.
    """
    display_name = "Balance Book Contents"
    default = True

class EnemiesTurnIntoChecks(Toggle):
    """
    If 'true', instead of receiving Checks after completing the Reception, You get one check for each defeated enemy.
    (There CAN be more checks than there is enemies!)

    If you really hate yourself and want to complete some receptions more than once.
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

class ExclusivenessRemove(Choice):
    """
    Select if "Combat Page Exclusiveness Removal" item should be added to the pool.

    I think option names are self explainatory?
    """
    display_name = "Combat Page Exclusiveness Remova"
    option_dontadd = 0
    option_item = 1
    option_remove = 2
    default = 1

class FillerItems(Choice):
    """
    Select which filler items are going to be in the pool.

    Book of Everything - It's drops adapt to your current progress, giving you pages around your current level.
                         Page rarity has small impact on item weights (Every rarity can drop almost with the same chance).
                         Allows for a more balanced playthrough. Amount of each page dropped is random.
    Booster Packs - Can give you any page in the game no matter when you burn them, but every page is dropped as a single copy,
                    and page weight decreases with rarity drastically (Higher rarity will drop a lot less).
                    Makes playthouugh a less balanced, and maybe more fun. If you win in the gacha.
    """
    display_name = "Filler Items"
    option_bookofeverything = 0
    option_boosterpacks = 1
    default = 0

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

@dataclass
class LOROptions(PerGameCommonOptions):
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
    # receptions_require_previous: ReceptionsRequirePrevious
    receptions_require_books: ReceptionsRequireBooks
    shuffle_abnos: ShuffleAbnos
    shuffle_realizations: ShuffleRealizations
    floors_require_books: FloorsRequireBooks
    randomize_black_silence_page: RandomizeBlackSilencePage
    balance_book_contents: BalanceBookContents
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