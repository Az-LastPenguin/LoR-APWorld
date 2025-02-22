from typing import Dict, NamedTuple
from BaseClasses import Location, Region

class LORLocation(Location):
    game: str = "Library of Ruina"

class LORLocationData(NamedTuple):
    name: str = ''
    address: int | None = None
    parent: Region | None = None

#end_cond_location_offset: int = 144000
#base_offset: int = 143000
#abno_offset: int = 143300
#clear_offset: int = 143600

#canard: Dict[str, int] = {
#    "Rats": 2,
#    "Yun's Office" : 2,
#    "Brotherhood of Iron": 2,
#    "Hook Office": 2,
#    
#    "Pierre's Bistro": 2,
#    "Streetlight Office": 2,
#}
#
#urban_legend: Dict[str, int] = {
#    "Stray Dogs": 2,
#    "Zwei Office": 3,
#    "Molar Office": 2,
#}
#
#storylineA: Dict[str, int] = {
#    "The Carnival": 2,
#    "Kurokumo Clan": 2,
#    "Sweepers": 3,
#    "Index Proselytes": 3,
#    "The Thumb": 3,
#    "Index Proxies": 3,
#    "얀샋ㄷ요무": 4,
#}
#
#storylineB: Dict[str, int] = {
#    "Full-Stop Office": 2,
#    "Musicians of Bremen": 2,
#    "Shi Association": 3,
#    "Smiling Faces": 3,
#    "The Blue Reverberation": 3,
#    "The Red Mist": 4,
#    "The Purple Tear": 4,
#}
#
#storylineC: Dict[str, int] = {
#    "Dawn Office": 2,
#    "Wedge Office": 3,
#    "The 8 o’Clock Circus": 3,
#    "The Crying Children": 4,
#    "Liu Association Section 2": 3,
#    "Liu Association Section 1": 3,
#    "Xiao": 4,
#}
#
#storylineD: Dict[str, int] = {
#    "Gaze Office": 2,
#    "Tomerry": 3,
#    "Puppets": 3,
#    "WARP Cleanup Crew": 3,
#    "Cane Office": 3,
#    "R Corp.": 3,
#    "R Corp. II": 3,
#}
#
#impurity: Dict[str, int] = {
#    "Hana Association": 4,
#}



#canard_general: Dict[str, int] = {
#    "Urban Myth-class Syndicate": 2,
#    "Hook Office Remnants" : 2,
#    "Backstreets Butchers": 2,
#}
#
#urban_legend_general: Dict[str, int] = {
#    "Grade 8 Fixers": 2,
#    "Grade 7 Fixers": 2,
#    "Urban Legend-class Office": 2,
#    "Urban Legend-class Syndicate": 2,
#    "Axe Gang": 2,
#}
#
#urban_plague_general: Dict[str, int] = {
#    "Rusted Chains": 2,
#    "Grade 7 Fixers": 2,
#    "Urban Legend-class Office": 2,
#}
#
#urban_nightmare_general: Dict[str, int] = {
#    "Seven Association": 2,
#    "Blade Lineage": 2,
#}
#
#sotc_general: Dict[str, int] = {
#    "Dong-hwan the Grade 1 Fixer": 2,
#    "Night Awls": 2,
#    "The Udjat": 2,
#    "Mirae Life Insurance": 2,
#    "Leaflet Workshop": 2,
#    "Bayard": 2,
#}



malkuth: Dict[str, int] = {
    "Scorched Girl": 3,
    "Happy Teddy Bear": 3,
    "Fairy Festival": 3,
    "Queen Bee": 3,
    
    "Floor of History Realization": 8,
}

yesod: Dict[str, int] = {
    "Forsaken Murderer": 3,
    "All-Around Helper": 3,
    "Singing Machine": 3,
    "The Funeral of the Dead Butterflies": 3,
    
    "Floor of Technological Sciences Realization": 8,
}

hod: Dict[str, int] = {
    "Today’s Shy Look": 3,
    "The Red Shoes": 3,
    "Spider Bud": 3,
    "Laetitia": 3,
    
    "Floor of Literature Realization": 8,
}

netzach: Dict[str, int] = {
    "Fragment of the Universe": 3,
    "Child of the Galaxy": 3,
    "Porccubus": 3,
    "Alriune": 3,
    
    "Floor of Art Realization": 8,
}

tiphereth: Dict[str, int] = {
    "The Queen of Hatred": 3,
    "The Knight of Despair": 3,
    "The King of Greed": 3,
    "The Servant of Wrath": 3,
    
    "Floor of Natural Sciences Realization": 8,
}

gebura: Dict[str, int] = {
    "Little Red Riding Hooded Mercenary": 3,
    "Big and Will be Bad Wolf": 3,
    "Mountain of Smiling Bodies": 3,
    "Nosferatu": 3,
    
    "Floor of Language Realization": 8,
}

chesed: Dict[str, int] = {
    "Scarecrow Searching for Wisdom": 3,
    "Warm-hearted Woodsman": 3,
    "The Road Home & Scaredy Cat": 3,
    "Ozma": 3,
    
    "Floor of Social Sciences Realization": 8,
}

binah: Dict[str, int] = {
    "Big Bird": 3,
    "Punishing Bird": 3,
    "Judgement Bird": 3,
    
    "Floor of Philosophy Realization": 11,
}

hokma: Dict[str, int] = {
    "The Burrowing Heaven": 3,
    "The Price of Silence": 3,
    "Blue Star": 3,
    
    "Floor of Religion Realization": 11,
}

keter: Dict[str, int] = {
    "Bloodbath": 3,
    "Heart of Aspiration": 3,
    "Pinocchio": 3,
    "The Snow Queen": 3,
    
    "Floor of General Works Realization": 8, # NO prrogression items
}



#endgoals: Dict[str, int] = { # NO progression items
#    # Reverb Ensemble (2 per Reception)
#    "[Ensemble] The Crying Children": 2,
#    "[Ensemble] The Church of Gears": 2,
#    "[Ensemble] The Eighth Chef": 2,
#    "[Ensemble] The Musicians of Bremen": 2,
#    "[Ensemble] The 8 o’Clock Circus": 2,
#    "[Ensemble] L’heure du Loup": 2,
#    "[Ensemble] The Puppeteer": 2,
#    "[Ensemble] The Blood-red Night": 2,
#    "[Ensemble] Yesterday’s Promise": 2,
#    "[Ensemble] The Blue Reverberation": 2,
#
#    "The Black Silence": 5,
#    "The Reverberation Ensemble Distorted": 5,
#}

location_table = {
#    "Canard": canard,
#    "Urban Legend": urban_legend,
#    "StoryA": storylineA,
#    "StoryB": storylineB,
#    "StoryC": storylineC,
#    "StoryD": storylineD,
#
#    "Canard General": canard_general,
#    "Urban Legend General": urban_legend_general,
#    "Urban Plague General": urban_plague_general,
#    "Urban Nightmare General": urban_nightmare_general,
#    "SotC General": sotc_general,

    "Malkuth": malkuth,
    "Yesod": yesod,
    "Hod": hod,
    "Netzach": netzach,
    "Tiphereth": tiphereth,
    "Gebura": gebura,
    "Chesed": chesed,
    "Binah": binah,
    "Hokma": hokma,
    "Keter": keter,

#    "EndGoals": endgoals,
}

#location_table = []
#
#i = 0
#for b in books:
#    location_table.append(LORLocationData(b, base_offset + i, None))
#    i += 1
#
#i = 0
#for a in abnormalities:
#    location_table.append(LORLocationData(a, abno_offset + i, None))
#    i += 1  

#i = 0
#for c in clear:
#    location_table.append(LORLocationData(c, clear_offset + i, None))
#    i += 1  




#books: list[str] = [
#    "Book of Rats",
#    "Book of a Grade 9 Fixer",
#    "Book of Finn",
#    "Book of Yun’s Office",
#    "Book of Eri",
#    "Book of Yun",
#    "Book of the Brotherhood of Iron",
#    "Book of Mo",
#    "Book of Consta",
#    "Book of Arnold",
#    "Hook Office, Vol. I",
#    "Book of Taein",
#    "Book of Naoki",
#    "Book of McCullin",
#    "Hook Office, Vol. II",
#
#    "Book of Pierre",
#    "Book of Jack",
#    "Book of Mars",
#    "Book of Lulu",
#    "A Guide to District 23",
#    "Dark Alleys of the Backstreets, Vol. I",
#    "A Backstreets Fixer, Vol. I",
#    "Streetlight Office",
#
#    "Book of Zwei South Section 6",
#    "Book of San",
#    "Book of Julia",
#    "Book of Isadora",
#    "Book of Walter",
#    "Book of the Stray Dogs",
#    "Book of Gyeong-mi",
#    "Book of Dino",
#    "Book of Zulu",
#    "Book of Molar Office",
#    "Book of Olga",
#    "Book of Rain",
#    "Book of Mika",
#    "Dark Alleys of the Backstreets, Vol. II",
#    "A Backstreets fixer, vol, II",
#    "A Backstreets Fixer, Vol. III",
#    "A Backstreets Fixer, Vol. IV",
#    "Book of a Grade 8 Fixer",
#    "Book of a Grade 7 Fixer",
#    "Book of Axe Gang",
#
#    "Book of The Carnival",
#    "Book of Full-Stop Office",
#    "Book of Liwei",
#    "Book of Stephan",
#    "Book of Tamaki",
#    "Book of Salvador",
#    "Book of Yuna",
#    "Book of Gaze Office",
#    "Book of Alloc",
#    "Book of Dalloc",
#    "Book of Bono",
#    "Book of Kurokumo Clan",
#    "Book of Sayo",
#    "Book of Yang",
#    "Book of Gin",
#    "Book of The Musicians of Bremen",
#    "Book of Meow",
#    "Book of MuMu",
#    "Book of Oink",
#    "Book of Wedge Office",
#    "Book of Oscar",
#    "Book of Pameli",
#    "Book of Pamela",
#    "Book of Tomerry",
#    "Book of Jikan",
#    "Book of a Rusted Chainlink",
#    "Book of a Workshop-affiliated Fixer",
#    "Book of a Jeong's Office Fixer",
#    "Book of Hanafuda",
#
#    "Book of a Sweeper",
#    "Book of Anton",
#    "Book of Lyla",
#    "Book of Valerie",
#    "Book of Shi Association",
#    "Book of Yujin",
#    "Book of Valentin",
#    "Book of Tenma",
#    "Book of Emma",
#    "Book of Noah",
#    "Book of a Puppet",
#    "Book of a Weighty Puppet",
#    "Book of an Index Proselyte",
#    "Book of the Smiling Faces",
#    "Book of Wang",
#    "Book of Jin",
#    "Book of Mi",
#    "Unstable Book of the Crying Children",
#    "Book of WARP Cleanup Crew",
#    "Book of Rose",
#    "Book of Sen",
#    "Book of Lesti",
#    "Book of a Seven Association Fixer",
#    "Book of Dante",
#    "Book of a Blade Lineage Cutthroat",
#    "Book of Bamboo-hatted Kim",
#
#    "Book of the Thumb",
#    "Book of Boris",
#    "Book of Denis",
#    "Book of Katriel",
#    "Book of Kalo",
#    "Book of a Church of Gears Worshipper",
#    "Liu Association Section 2, Vol I",
#    "Liu Association Section 2, Vol II",
#    "Book of Lowell",
#    "Book of Cecil",
#    "Book of Mei",
#    "Book of Cane Office",
#    "Book of Bada",
#    "Book of Martina",
#    "Book of Nemo",
#    "Book of the Index",
#    "Book of Esther",
#    "Book of Gloria",
#    "Book of Hubert",
#    "Book of Liu Association Section 1",
#    "Book of Chun",
#    "Book of the Red Mist",
#    "Book of the Reindeer Team",
#    "Book of the Rhino Team",
#    "Book of the Rabbit Team",
#    "Book of Rudolph",
#    "Book of Maxim",
#    "Book of Myo",
#    "Book of Nikolai",
#    "Book of 얀샋ㄷ요무",
#    "Book of Miris",
#    "Book of Xiao",
#    "Book of the Purple Tear",
#    "Complete Book of Rudolph",
#    "Complete Book of Maxim",
#    "Complete Book of Myo",
#    "Complete Book of Nikolai",
#    "Book of Dong-hwan the Grade 1 Fixer",
#    "Book of a Night Awl",
#    "Book of Allen",
#    "Book of an Udjat",
#    "Book of a Irina",
#    "Book of a Mirae Life Insurer",
#    "Book of a Leaflet Workshop Fixer",
#    "Book of Yae",
#    "Book of a Bayard's Office Fixer",
#    "Book of Bayard",
#
#    "Book of Hana Association",
#    "Book of Harold",
#    "Book of Mirinae",
#    "Book of Olivier",
#]