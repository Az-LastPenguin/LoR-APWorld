from typing import NamedTuple
from BaseClasses import Location, Region

class LORLocation(Location):
    game: str = "Library of Ruina"

class LORLocationData(NamedTuple):
    name: str = ''
    address: int | None = None
    parent: Region | None = None

end_cond_location_offset: int = 144000
base_offset: int = 143000
abno_offset: int = 143300
clear_offset: int = 143600

books: list[str] = [
    "Book of Rats",
    "Book of a Grade 9 Fixer",
    "Book of Finn",
    "Book of Yun’s Office",
    "Book of Eri",
    "Book of Yun",
    "Book of the Brotherhood of Iron",
    "Book of Mo",
    "Book of Consta",
    "Book of Arnold",
    "Hook Office, Vol. I",
    "Book of Taein",
    "Book of Naoki",
    "Book of McCullin",
    "Hook Office, Vol. II",

    "Book of Pierre",
    "Book of Jack",
    "Book of Mars",
    "Book of Lulu",
    "A Guide to District 23",
    "Dark Alleys of the Backstreets, Vol. I",
    "A Backstreets Fixer, Vol. I",
    "Streetlight Office",

    "Book of Zwei South Section 6",
    "Book of San",
    "Book of Julia",
    "Book of Isadora",
    "Book of Walter",
    "Book of the Stray Dogs",
    "Book of Gyeong-mi",
    "Book of Dino",
    "Book of Zulu",
    "Book of Molar Office",
    "Book of Olga",
    "Book of Rain",
    "Book of Mika",
    "Dark Alleys of the Backstreets, Vol. II",
    "A Backstreets fixer, vol, II",
    "A Backstreets Fixer, Vol. III",
    "A Backstreets Fixer, Vol. IV",
    "Book of a Grade 8 Fixer",
    "Book of a Grade 7 Fixer",
    "Book of Axe Gang",

    "Book of The Carnival",
    "Book of Full-Stop Office",
    "Book of Liwei",
    "Book of Stephan",
    "Book of Tamaki",
    "Book of Salvador",
    "Book of Yuna",
    "Book of Gaze Office",
    "Book of Alloc",
    "Book of Dalloc",
    "Book of Bono",
    "Book of Kurokumo Clan",
    "Book of Sayo",
    "Book of Yang",
    "Book of Gin",
    "Book of The Musicians of Bremen",
    "Book of Meow",
    "Book of MuMu",
    "Book of Oink",
    "Book of Wedge Office",
    "Book of Oscar",
    "Book of Pameli",
    "Book of Pamela",
    "Book of Tomerry",
    "Book of Jikan",
    "Book of a Rusted Chainlink",
    "Book of a Workshop-affiliated Fixer",
    "Book of a Jeong's Office Fixer",
    "Book of Hanafuda",

    "Book of a Sweeper",
    "Book of Anton",
    "Book of Lyla",
    "Book of Valerie",
    "Book of Shi Association",
    "Book of Yujin",
    "Book of Valentin",
    "Book of Tenma",
    "Book of Emma",
    "Book of Noah",
    "Book of a Puppet",
    "Book of a Weighty Puppet",
    "Book of an Index Proselyte",
    "Book of the Smiling Faces",
    "Book of Wang",
    "Book of Jin",
    "Book of Mi",
    "Unstable Book of the Crying Children",
    "Book of WARP Cleanup Crew",
    "Book of Rose",
    "Book of Sen",
    "Book of Lesti",
    "Book of a Seven Association Fixer",
    "Book of Dante",
    "Book of a Blade Lineage Cutthroat",
    "Book of Bamboo-hatted Kim",

    "Book of the Thumb",
    "Book of Boris",
    "Book of Denis",
    "Book of Katriel",
    "Book of Kalo",
    "Book of a Church of Gears Worshipper",
    "Liu Association Section 2, Vol I",
    "Liu Association Section 2, Vol II",
    "Book of Lowell",
    "Book of Cecil",
    "Book of Mei",
    "Book of Cane Office",
    "Book of Bada",
    "Book of Martina",
    "Book of Nemo",
    "Book of the Index",
    "Book of Esther",
    "Book of Gloria",
    "Book of Hubert",
    "Book of Liu Association Section 1",
    "Book of Chun",
    "Book of the Red Mist",
    "Book of the Reindeer Team",
    "Book of the Rhino Team",
    "Book of the Rabbit Team",
    "Book of Rudolph",
    "Book of Maxim",
    "Book of Myo",
    "Book of Nikolai",
    "Book of 얀샋ㄷ요무",
    "Book of Miris",
    "Book of Xiao",
    "Book of the Purple Tear",
    "Complete Book of Rudolph",
    "Complete Book of Maxim",
    "Complete Book of Myo",
    "Complete Book of Nikolai",
    "Book of Dong-hwan the Grade 1 Fixer",
    "Book of a Night Awl",
    "Book of Allen",
    "Book of an Udjat",
    "Book of a Irina",
    "Book of a Mirae Life Insurer",
    "Book of a Leaflet Workshop Fixer",
    "Book of Yae",
    "Book of a Bayard's Office Fixer",
    "Book of Bayard",

    "Book of Hana Association",
    "Book of Harold",
    "Book of Mirinae",
    "Book of Olivier",
]

abnormalities: list[str] = [
    # Malkuth Checks
    "Scorched Girl suppression(1)",
    "Scorched Girl suppression(2)",
    "Scorched Girl suppression(3)",

    "Happy Teddy Bear suppression(1)",
    "Happy Teddy Bear suppression(2)",
    "Happy Teddy Bear suppression(3)",

    "Fairy Festival suppression(1)",
    "Fairy Festival suppression(2)",
    "Fairy Festival suppression(3)",

    "Queen Bee suppression(1)",
    "Queen Bee suppression(2)",
    "Queen Bee suppression(3)",

    "Floor of History Realization(1)",
    "Floor of History Realization(2)",
    "Floor of History Realization(3)",

    "Floor of History Realization(4)",
    "Floor of History Realization(5)",
    "Floor of History Realization(6)",
    "Floor of History Realization(7)",
    "Floor of History Realization(8)",

    # Yesod Checks
    "Forsaken Murderer suppression(1)",
    "Forsaken Murderer suppression(2)",
    "Forsaken Murderer suppression(3)",

    "All-Around Helper suppression(1)",
    "All-Around Helper suppression(2)",
    "All-Around Helper suppression(3)",

    "Singing Machine suppression(1)",
    "Singing Machine suppression(2)",
    "Singing Machine suppression(3)",

    "The Funeral of the Dead Butterflies suppression(1)",
    "The Funeral of the Dead Butterflies suppression(2)",
    "The Funeral of the Dead Butterflies suppression(3)",

    "Floor of Technological Sciences Realization(1)",
    "Floor of Technological Sciences Realization(2)",
    "Floor of Technological Sciences Realization(3)",

    "Floor of Technological Sciences Realization(4)",
    "Floor of Technological Sciences Realization(5)",
    "Floor of Technological Sciences Realization(6)",
    "Floor of Technological Sciences Realization(7)",
    "Floor of Technological Sciences Realization(8)",

    # Hod Checks
    "Today’s Shy Look suppression(1)",
    "Today’s Shy Look suppression(2)",
    "Today’s Shy Look suppression(3)",

    "The Red Shoes suppression(1)",
    "The Red Shoes suppression(2)",
    "The Red Shoes suppression(3)",

    "Spider Bud suppression(1)",
    "Spider Bud suppression(2)",
    "Spider Bud suppression(3)",

    "Laetitia suppression(1)",
    "Laetitia suppression(2)",
    "Laetitia suppression(3)",

    "Floor of Literature Realization(1)",
    "Floor of Literature Realization(2)",
    "Floor of Literature Realization(3)",

    "Floor of Literature Realization(4)",
    "Floor of Literature Realization(5)",
    "Floor of Literature Realization(6)",
    "Floor of Literature Realization(7)",
    "Floor of Literature Realization(8)",

    # Netzach Checks
    "Fragment of the Universe suppression(1)",
    "Fragment of the Universe suppression(2)",
    "Fragment of the Universe suppression(3)",

    "Child of the Galaxy suppression(1)",
    "Child of the Galaxy suppression(2)",
    "Child of the Galaxy suppression(3)",

    "Porccubus suppression(1)",
    "Porccubus suppression(2)",
    "Porccubus suppression(3)",

    "Alriune suppression(1)",
    "Alriune suppression(2)",
    "Alriune suppression(3)",

    "Floor of Art Realization(1)",
    "Floor of Art Realization(2)",
    "Floor of Art Realization(3)",

    "Floor of Art Realization(4)",
    "Floor of Art Realization(5)",
    "Floor of Art Realization(6)",
    "Floor of Art Realization(7)",
    "Floor of Art Realization(8)",

    # Tiphereth Checks
    "The Queen of Hatred suppression(1)",
    "The Queen of Hatred suppression(2)",
    "The Queen of Hatred suppression(3)",

    "The Knight of Despair suppression(1)",
    "The Knight of Despair suppression(2)",
    "The Knight of Despair suppression(3)",

    "The King of Greed suppression(1)",
    "The King of Greed suppression(2)",
    "The King of Greed suppression(3)",

    "The Servant of Wrath suppression(1)",
    "The Servant of Wrath suppression(2)",
    "The Servant of Wrath suppression(3)",

    "Floor of Natural Sciences Realization(1)",
    "Floor of Natural Sciences Realization(2)",
    "Floor of Natural Sciences Realization(3)",

    "Floor of Natural Sciences Realization(4)",
    "Floor of Natural Sciences Realization(5)",
    "Floor of Natural Sciences Realization(6)",
    "Floor of Natural Sciences Realization(7)",
    "Floor of Natural Sciences Realization(8)",

    # Gebura Checks
    "Little Red Riding Hooded Mercenary suppression(1)",
    "Little Red Riding Hooded Mercenary suppression(2)",
    "Little Red Riding Hooded Mercenary suppression(3)",

    "Big and Will be Bad Wolf suppression(1)",
    "Big and Will be Bad Wolf suppression(2)",
    "Big and Will be Bad Wolf suppression(3)",

    "Mountain of Smiling Bodies suppression(1)",
    "Mountain of Smiling Bodies suppression(2)",
    "Mountain of Smiling Bodies suppression(3)",

    "Nosferatu suppression(1)",
    "Nosferatu suppression(2)",
    "Nosferatu suppression(3)",

    "Floor of Language Realization(1)",
    "Floor of Language Realization(2)",
    "Floor of Language Realization(3)",

    "Floor of Language Realization(4)",
    "Floor of Language Realization(5)",
    "Floor of Language Realization(6)",
    "Floor of Language Realization(7)",
    "Floor of Language Realization(8)",

    # Chesed Checks
    "Scarecrow Searching for Wisdom suppression(1)",
    "Scarecrow Searching for Wisdom suppression(2)",
    "Scarecrow Searching for Wisdom suppression(3)",

    "Warm-hearted Woodsman suppression(1)",
    "Warm-hearted Woodsman suppression(2)",
    "Warm-hearted Woodsman suppression(3)",

    "The Road Home & Scaredy Cat suppression(1)",
    "The Road Home & Scaredy Cat suppression(2)",
    "The Road Home & Scaredy Cat suppression(3)",

    "Ozma suppression(1)",
    "Ozma suppression(2)",
    "Ozma suppression(3)",

    "Floor of Social Sciences Realization(1)",
    "Floor of Social Sciences Realization(2)",
    "Floor of Social Sciences Realization(3)",

    "Floor of Social Sciences Realization(4)",
    "Floor of Social Sciences Realization(5)",
    "Floor of Social Sciences Realization(6)",
    "Floor of Social Sciences Realization(7)",
    "Floor of Social Sciences Realization(8)",

    # Binah Checks
    "Big Bird suppression(1)",
    "Big Bird suppression(2)",
    "Big Bird suppression(3)",

    "Punishing Bird suppression(1)",
    "Punishing Bird suppression(2)",
    "Punishing Bird suppression(3)",

    "Judgement Bird suppression(1)",
    "Judgement Bird suppression(2)",
    "Judgement Bird suppression(3)",

    "Floor of Philosophy Realization(1)",
    "Floor of Philosophy Realization(2)",
    "Floor of Philosophy Realization(3)",

    "Floor of Philosophy Realization(4)",
    "Floor of Philosophy Realization(5)",
    "Floor of Philosophy Realization(6)",

    "Floor of Philosophy Realization(7)",
    "Floor of Philosophy Realization(8)",
    "Floor of Philosophy Realization(9)",
    "Floor of Philosophy Realization(10)",
    "Floor of Philosophy Realization(11)",

    # Hokma Checks
    "The Burrowing Heaven suppression(1)",
    "The Burrowing Heaven suppression(2)",
    "The Burrowing Heaven suppression(3)",

    "The Price of Silence suppression(1)",
    "The Price of Silence suppression(2)",
    "The Price of Silence suppression(3)",

    "Blue Star suppression(1)",
    "Blue Star suppression(2)",
    "Blue Star suppression(3)",

    "Floor of Religion Realization(1)",
    "Floor of Religion Realization(2)",
    "Floor of Religion Realization(3)",

    "Floor of Religion Realization(4)",
    "Floor of Religion Realization(5)",
    "Floor of Religion Realization(6)",

    "Floor of Religion Realization(7)",
    "Floor of Religion Realization(8)",
    "Floor of Religion Realization(9)",
    "Floor of Religion Realization(10)",
    "Floor of Religion Realization(11)",

    # Keter Checks
    "Bloodbath suppression(1)",
    "Bloodbath suppression(2)",
    "Bloodbath suppression(3)",

    "Heart of Aspiration suppression(1)",
    "Heart of Aspiration suppression(2)",
    "Heart of Aspiration suppression(3)",

    "Pinocchio suppression(1)",
    "Pinocchio suppression(2)",
    "Pinocchio suppression(3)",

    "The Snow Queen suppression(1)",
    "The Snow Queen suppression(2)",
    "The Snow Queen suppression(3)",
]

clear = [
    # Reverb Ensemble
    "[Ensemble] The Crying Children(1)",
    "[Ensemble] The Crying Children(2)",
    "[Ensemble] The Crying Children(3)",

    "[Ensemble] The Church of Gears(1)",
    "[Ensemble] The Church of Gears(2)",
    "[Ensemble] The Church of Gears(3)",
    
    "[Ensemble] The Musicians of Bremen(1)",
    "[Ensemble] The Musicians of Bremen(2)",
    "[Ensemble] The Musicians of Bremen(3)",

    "[Ensemble] The Eighth Chef(1)",
    "[Ensemble] The Eighth Chef(2)",
    "[Ensemble] The Eighth Chef(3)",

    "[Ensemble] The 8 o'Clock Circus(1)",
    "[Ensemble] The 8 o'Clock Circus(2)",
    "[Ensemble] The 8 o'Clock Circus(3)",

    "[Ensemble] L'heure du Loup(1)",
    "[Ensemble] L'heure du Loup(2)",
    "[Ensemble] L'heure du Loup(3)",

    "[Ensemble] The Puppeteer(1)",
    "[Ensemble] The Puppeteer(2)",
    "[Ensemble] The Puppeteer(3)",

    "[Ensemble] The Blood-red Night(1)",
    "[Ensemble] The Blood-red Night(2)",
    "[Ensemble] The Blood-red Night(3)",

    "[Ensemble] Yesterday's Promise(1)",
    "[Ensemble] Yesterday's Promise(2)",
    "[Ensemble] Yesterday's Promise(3)",

    "[Ensemble] The Blue Reverberation(1)",
    "[Ensemble] The Blue Reverberation(2)",
    "[Ensemble] The Blue Reverberation(3)",

    # Black Silence
    "Black Silence Reception(1)",
    "Black Silence Reception(2)",
    "Black Silence Reception(3)",
    "Black Silence Reception(4)",
    "Black Silence Reception(5)",
    "Black Silence Reception(6)",

    # Distorted Ensemble
    "Distorted Ensemble Reception(1)",
    "Distorted Ensemble Reception(2)",
    "Distorted Ensemble Reception(3)",
    "Distorted Ensemble Reception(4)",
    "Distorted Ensemble Reception(5)",
    "Distorted Ensemble Reception(6)",

    # Keter Realization
    "Floor of General Works Realization(1)",
    "Floor of General Works Realization(2)",
    "Floor of General Works Realization(3)",

    "Floor of General Works Realization(4)",
    "Floor of General Works Realization(5)",
    "Floor of General Works Realization(6)",
    "Floor of General Works Realization(7)",
    "Floor of General Works Realization(8)",
]

location_table = []

i = 0
for b in books:
    location_table.append(LORLocationData(b, base_offset + i, None))
    i += 1

i = 0
for a in abnormalities:
    location_table.append(LORLocationData(a, abno_offset + i, None))
    i += 1  

#i = 0
#for c in clear:
#    location_table.append(LORLocationData(c, clear_offset + i, None))
#    i += 1  