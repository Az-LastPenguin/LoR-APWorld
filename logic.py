from BaseClasses import CollectionState
from .items import items_by_category

def lor_enough_librarians(need: int, state: CollectionState, player: int) -> bool:
    librarian_items = [f.name for f in items_by_category["Librarian"]]
    
    for i in range(10):
        if state.has(librarian_items[i], player, need - 1 - (1 if i == 7 and state.has("Binah", player) else 0)):
            return True
        #if lor_enough_librarians_on_floor(i, need - 1 + (1 if i == 7 and state.has("Binah", player) else 0), state, player):
        #    return True
            
    return False

#def lor_enough_librarians_on_floor(id: int, need: int, state: CollectionState, player: int) -> bool:
#    librarian_items = [f.name for f in items_by_category["Librarian"]]
#
#    return state.has(librarian_items[id], player, need-1)