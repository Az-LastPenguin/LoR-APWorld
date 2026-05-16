from BaseClasses import CollectionState
from .items import items_by_category


def lor_enough_librarians(need: int, state: CollectionState, player: int) -> bool:
    librarian_items = [f.name for f in items_by_category["Librarian"]]
    floor_items = [f.name for f in items_by_category["FloorUnlock"]]

    for i in range(10):
        if not state.has(floor_items[i], player):
            continue

        required_librarian_items = need - 1 - (1 if i == 7 and state.has("Binah", player) else 0)
        if state.has(librarian_items[i], player, max(0, required_librarian_items)):
            return True
        #if lor_enough_librarians_on_floor(i, need - 1 + (1 if i == 7 and state.has("Binah", player) else 0), state, player):
        #    return True

    return False

#def lor_enough_librarians_on_floor(id: int, need: int, state: CollectionState, player: int) -> bool:
#    librarian_items = [f.name for f in items_by_category["Librarian"]]
#
#    return state.has(librarian_items[id], player, need-1)
