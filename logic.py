from BaseClasses import CollectionState
from .items import items_by_category

def lor_enough_librarians(need: int, state: CollectionState, player: int) -> bool:
    for i in range(10):
        if lor_enough_librarians_on_floor(i, need - 1 + (1 if i == 7 and state.has("Binah", player) else 0), state, player):
            return True

    return False

def lor_enough_librarians_on_floor(id: int, need: int, state: CollectionState, player: int) -> bool:
    librarian_items = [f.name for f in items_by_category["Librarian"]]

    return state.has(librarian_items[id-1], player, need-1)

def lor_has_floor(id: int, state: CollectionState, player: int) -> bool:
    floor_names = [f.name for f in items_by_category["FloorUnlock"]]

    return state.has(floor_names[id-1], player)