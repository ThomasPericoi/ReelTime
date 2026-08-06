#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT / "assets" / "medias" / "videos" / "movie-scenes"
DATA_DIR = ROOT / "assets" / "data"
OUT = DATA_DIR / "scenes.json"
JS_OUT = DATA_DIR / "scenes-data.js"
FLEXIBLE_SPAN_MINUTES = 7

MOVIE_META = {
    "12-angry-men": {"title": "12 Angry Men", "year": 1957, "director": "Sidney Lumet", "rightsHolder": "Orion-Nova Productions / MGM", "imdbRating": 9.0},
    "12-monkeys": {"title": "12 Monkeys", "year": 1995, "director": "Terry Gilliam", "rightsHolder": "Universal Pictures", "imdbRating": 8.0},
    "127-hours": {"title": "127 Hours", "year": 2010, "director": "Danny Boyle", "rightsHolder": "Searchlight Pictures / Pathé", "imdbRating": 7.5},
    "13-going-on-30": {"title": "13 Going on 30", "year": 2004, "director": "Gary Winick", "rightsHolder": "Columbia Pictures / Revolution Studios", "imdbRating": 6.3},
    "3-10-to-yuma": {"title": "3:10 to Yuma", "year": 1957, "director": "Delmer Daves", "rightsHolder": "Columbia Pictures", "imdbRating": 7.6},
    "8-bit-christmas": {"title": "8-Bit Christmas", "year": 2021, "director": "Michael Dowse", "rightsHolder": "Warner Bros. Pictures / New Line Cinema", "imdbRating": 6.7},
    "a-beautiful-mind": {"title": "A Beautiful Mind", "year": 2001, "director": "Ron Howard", "rightsHolder": "Universal Pictures / DreamWorks Pictures", "imdbRating": 8.2},
    "a-christmas-story": {"title": "A Christmas Story", "year": 1983, "director": "Bob Clark", "rightsHolder": "MGM / Warner Bros. Pictures", "imdbRating": 7.9},
    "a-clockwork-orange": {"title": "A Clockwork Orange", "year": 1971, "director": "Stanley Kubrick", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.2},
    "a-fish-called-wanda": {"title": "A Fish Called Wanda", "year": 1988, "director": "Charles Crichton", "rightsHolder": "MGM", "imdbRating": 7.5},
    "a-million-ways-to-die-in-the-west": {"title": "A Million Ways to Die in the West", "year": 2014, "director": "Seth MacFarlane", "rightsHolder": "Universal Pictures", "imdbRating": 6.1},
    "a-nightmare-on-elm-street": {"title": "A Nightmare on Elm Street", "year": 1984, "director": "Wes Craven", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 7.4},
    "a-serious-man": {"title": "A Serious Man", "year": 2009, "director": "Joel Coen and Ethan Coen", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.0},
    "a-star-is-born": {"title": "A Star Is Born", "year": 2018, "director": "Bradley Cooper", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.6},
    "ace-ventura-when-nature-calls": {"title": "Ace Ventura: When Nature Calls", "year": 1995, "director": "Steve Oedekerk", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.4},
    "all-the-president-s-men": {"title": "All the President's Men", "year": 1976, "director": "Alan J. Pakula", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.9},
    "american-gangster": {"title": "American Gangster", "year": 2007, "director": "Ridley Scott", "rightsHolder": "Universal Pictures", "imdbRating": 7.8},
    "american-hustle": {"title": "American Hustle", "year": 2013, "director": "David O. Russell", "rightsHolder": "Sony Pictures", "imdbRating": 7.2},
    "american-made": {"title": "American Made", "year": 2017, "director": "Doug Liman", "rightsHolder": "Universal Pictures", "imdbRating": 7.2},
    "american-psycho": {"title": "American Psycho", "year": 2000, "director": "Mary Harron", "rightsHolder": "Lionsgate", "imdbRating": 7.6},
    "and-justice-for-all": {"title": "...And Justice for All", "year": 1979, "director": "Norman Jewison", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.4},
    "angels-and-demons": {"title": "Angels & Demons", "year": 2009, "director": "Ron Howard", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 6.7},
    "annie": {"title": "Annie", "year": 1982, "director": "John Huston", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 6.6},
    "anomalisa": {"title": "Anomalisa", "year": 2015, "director": "Charlie Kaufman and Duke Johnson", "rightsHolder": "Paramount Pictures", "imdbRating": 7.2},
    "anora": {"title": "Anora", "year": 2024, "director": "Sean Baker", "rightsHolder": "Neon", "imdbRating": 7.4},
    "ant-man-and-the-wasp-quantumania": {"title": "Ant-Man and the Wasp: Quantumania", "year": 2023, "director": "Peyton Reed", "rightsHolder": "Marvel Studios / Walt Disney Pictures", "imdbRating": 6.0},
    "antichrist": {"title": "Antichrist", "year": 2009, "director": "Lars von Trier", "rightsHolder": "IFC Films / Zentropa", "imdbRating": 6.5},
    "apocalypse-now": {"title": "Apocalypse Now", "year": 1979, "director": "Francis Ford Coppola", "rightsHolder": "United Artists / Lionsgate", "imdbRating": 8.4},
    "asteroid-city": {"title": "Asteroid City", "year": 2023, "director": "Wes Anderson", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 6.4},
    "babe": {"title": "Babe", "year": 1995, "director": "Chris Noonan", "rightsHolder": "Universal Pictures", "imdbRating": 6.9},
    "back-to-the-future": {"title": "Back to the Future", "year": 1985, "director": "Robert Zemeckis", "rightsHolder": "Universal Pictures", "imdbRating": 8.5},
    "back-to-the-future-part-3": {"title": "Back to the Future Part III", "year": 1990, "director": "Robert Zemeckis", "rightsHolder": "Universal Pictures", "imdbRating": 7.5},
    "basic-instinct": {"title": "Basic Instinct", "year": 1992, "director": "Paul Verhoeven", "rightsHolder": "StudioCanal / Lionsgate", "imdbRating": 7.1},
    "batman-returns": {"title": "Batman Returns", "year": 1992, "director": "Tim Burton", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.1},
    "beau-is-afraid": {"title": "Beau Is Afraid", "year": 2023, "director": "Ari Aster", "rightsHolder": "A24", "imdbRating": 6.6},
    "beetlejuice": {"title": "Beetlejuice", "year": 1988, "director": "Tim Burton", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.4},
    "before-sunrise": {"title": "Before Sunrise", "year": 1995, "director": "Richard Linklater", "rightsHolder": "Columbia Pictures", "imdbRating": 8.1},
    "being-john-malkovich": {"title": "Being John Malkovich", "year": 1999, "director": "Spike Jonze", "rightsHolder": "USA Films / Universal Pictures", "imdbRating": 7.7},
    "being-the-ricardos": {"title": "Being the Ricardos", "year": 2021, "director": "Aaron Sorkin", "rightsHolder": "Amazon Studios", "imdbRating": 6.5},
    "being-there": {"title": "Being There", "year": 1979, "director": "Hal Ashby", "rightsHolder": "United Artists / Warner Bros. Discovery", "imdbRating": 7.9},
    "belfast": {"title": "Belfast", "year": 2021, "director": "Kenneth Branagh", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.2},
    "big": {"title": "Big", "year": 1988, "director": "Penny Marshall", "rightsHolder": "20th Century Studios", "imdbRating": 7.3},
    "big-fish": {"title": "Big Fish", "year": 2003, "director": "Tim Burton", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.9},
    "black-hawk-down": {"title": "Black Hawk Down", "year": 2001, "director": "Ridley Scott", "rightsHolder": "Sony Pictures", "imdbRating": 7.7},
    "blue-velvet": {"title": "Blue Velvet", "year": 1986, "director": "David Lynch", "rightsHolder": "MGM / De Laurentiis Entertainment Group", "imdbRating": 7.7},
    "bone-tomahawk": {"title": "Bone Tomahawk", "year": 2015, "director": "S. Craig Zahler", "rightsHolder": "RLJ Entertainment", "imdbRating": 7.1},
    "brewster-s-millions": {"title": "Brewster's Millions", "year": 1985, "director": "Walter Hill", "rightsHolder": "Universal Pictures", "imdbRating": 6.5},
    "bugonia": {"title": "Bugonia", "year": 2025, "director": "Yorgos Lanthimos", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.4},
    "bullet-train": {"title": "Bullet Train", "year": 2022, "director": "David Leitch", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.3},
    "burn-after-reading": {"title": "Burn After Reading", "year": 2008, "director": "Joel Coen and Ethan Coen", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.0},
    "captain-fantastic": {"title": "Captain Fantastic", "year": 2016, "director": "Matt Ross", "rightsHolder": "Bleecker Street", "imdbRating": 7.8},
    "carrie": {"title": "Carrie", "year": 1976, "director": "Brian De Palma", "rightsHolder": "United Artists / MGM", "imdbRating": 7.4},
    "casablanca": {"title": "Casablanca", "year": 1942, "director": "Michael Curtiz", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.5},
    "cast-away": {"title": "Cast Away", "year": 2000, "director": "Robert Zemeckis", "rightsHolder": "20th Century Studios / DreamWorks Pictures", "imdbRating": 7.8},
    "charlie-s-angels": {"title": "Charlie's Angels", "year": 2000, "director": "McG", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 5.7},
    "chef": {"title": "Chef", "year": 2014, "director": "Jon Favreau", "rightsHolder": "Open Road Films", "imdbRating": 7.3},
    "chickenhare-and-the-hamster-of-darkness": {"title": "Chickenhare and the Hamster of Darkness", "year": 2022, "director": "Ben Stassen and Benjamin Mousquet", "rightsHolder": "nWave Pictures / Sony Pictures", "imdbRating": 6.3},
    "child-s-play": {"title": "Child's Play", "year": 1988, "director": "Tom Holland", "rightsHolder": "MGM / United Artists", "imdbRating": 6.7},
    "citizen-kane": {"title": "Citizen Kane", "year": 1941, "director": "Orson Welles", "rightsHolder": "Warner Bros. Discovery", "imdbRating": 8.2},
    "civil-war": {"title": "Civil War", "year": 2024, "director": "Alex Garland", "rightsHolder": "A24", "imdbRating": 7.0},
    "clueless": {"title": "Clueless", "year": 1995, "director": "Amy Heckerling", "rightsHolder": "Paramount Pictures", "imdbRating": 6.9},
    "crazy-stupid-love": {"title": "Crazy, Stupid, Love.", "year": 2011, "director": "Glenn Ficarra and John Requa", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.4},
    "darkest-hour": {"title": "Darkest Hour", "year": 2017, "director": "Joe Wright", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.4},
    "dave": {"title": "Dave", "year": 1993, "director": "Ivan Reitman", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.9},
    "dawn-of-the-dead": {"title": "Dawn of the Dead", "year": 1978, "director": "George A. Romero", "rightsHolder": "United Film Distribution Company / Anchor Bay Entertainment", "imdbRating": 7.8},
    "dead-man": {"title": "Dead Man", "year": 1995, "director": "Jim Jarmusch", "rightsHolder": "Miramax", "imdbRating": 7.5},
    "demolition": {"title": "Demolition", "year": 2015, "director": "Jean-Marc Vallée", "rightsHolder": "Fox Searchlight Pictures", "imdbRating": 7.0},
    "den-of-thieves": {"title": "Den of Thieves", "year": 2018, "director": "Christian Gudegast", "rightsHolder": "STX Entertainment", "imdbRating": 7.0},
    "die-hard-2": {"title": "Die Hard 2", "year": 1990, "director": "Renny Harlin", "rightsHolder": "20th Century Studios", "imdbRating": 7.2},
    "donnie-darko": {"title": "Donnie Darko", "year": 2001, "director": "Richard Kelly", "rightsHolder": "Arrow Films / Newmarket Films", "imdbRating": 8.0},
    "dr-strangelove": {"title": "Dr. Strangelove", "year": 1964, "director": "Stanley Kubrick", "rightsHolder": "Sony Pictures / Columbia Pictures", "imdbRating": 8.3},
    "dracula-dead-and-loving-it": {"title": "Dracula: Dead and Loving It", "year": 1995, "director": "Mel Brooks", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 5.9},
    "dragnet": {"title": "Dragnet", "year": 1987, "director": "Tom Mankiewicz", "rightsHolder": "Universal Pictures", "imdbRating": 6.0},
    "dumb-and-dumber": {"title": "Dumb and Dumber", "year": 1994, "director": "Peter Farrelly", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 7.3},
    "ed-wood": {"title": "Ed Wood", "year": 1994, "director": "Tim Burton", "rightsHolder": "Touchstone Pictures / Disney", "imdbRating": 7.8},
    "election": {"title": "Election", "year": 1999, "director": "Alexander Payne", "rightsHolder": "Paramount Pictures", "imdbRating": 7.2},
    "elysium": {"title": "Elysium", "year": 2013, "director": "Neill Blomkamp", "rightsHolder": "TriStar Pictures / Sony Pictures", "imdbRating": 6.6},
    "escape-from-new-york": {"title": "Escape From New York", "year": 1981, "director": "John Carpenter", "rightsHolder": "StudioCanal / AVCO Embassy", "imdbRating": 7.1},
    "eternal-sunshine-of-the-spotless-mind": {"title": "Eternal Sunshine of the Spotless Mind", "year": 2004, "director": "Michel Gondry", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 8.3},
    "every-which-way-but-loose": {"title": "Every Which Way but Loose", "year": 1978, "director": "James Fargo", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.3},
    "evil-dead-2": {"title": "Evil Dead II", "year": 1987, "director": "Sam Raimi", "rightsHolder": "StudioCanal / Rosebud Releasing", "imdbRating": 7.6},
    "ex-machina": {"title": "Ex Machina", "year": 2014, "director": "Alex Garland", "rightsHolder": "A24 / Universal Pictures", "imdbRating": 7.7},
    "explorers": {"title": "Explorers", "year": 1985, "director": "Joe Dante", "rightsHolder": "Paramount Pictures", "imdbRating": 6.4},
    "eyes-wide-shut": {"title": "Eyes Wide Shut", "year": 1999, "director": "Stanley Kubrick", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.5},
    "fantastic-mister-fox": {"title": "Fantastic Mr. Fox", "year": 2009, "director": "Wes Anderson", "rightsHolder": "20th Century Studios", "imdbRating": 7.9},
    "far-and-away": {"title": "Far and Away", "year": 1992, "director": "Ron Howard", "rightsHolder": "Universal Pictures", "imdbRating": 6.6},
    "fargo": {"title": "Fargo", "year": 1996, "director": "Joel Coen", "rightsHolder": "Gramercy Pictures / MGM", "imdbRating": 8.1},
    "father-of-the-bride": {"title": "Father of the Bride", "year": 1991, "director": "Charles Shyer", "rightsHolder": "Touchstone Pictures / Disney", "imdbRating": 6.6},
    "fifth-element": {"title": "The Fifth Element", "year": 1997, "director": "Luc Besson", "rightsHolder": "Gaumont / Sony Pictures", "imdbRating": 7.6},
    "finding-forrester": {"title": "Finding Forrester", "year": 2000, "director": "Gus Van Sant", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.3},
    "firestarter": {"title": "Firestarter", "year": 1984, "director": "Mark L. Lester", "rightsHolder": "Universal Pictures", "imdbRating": 6.1},
    "flubber": {"title": "Flubber", "year": 1997, "director": "Les Mayfield", "rightsHolder": "Walt Disney Pictures", "imdbRating": 5.3},
    "ford-v-ferrari": {"title": "Ford v Ferrari", "year": 2019, "director": "James Mangold", "rightsHolder": "20th Century Studios", "imdbRating": 8.1},
    "foul-play": {"title": "Foul Play", "year": 1978, "director": "Colin Higgins", "rightsHolder": "Paramount Pictures", "imdbRating": 6.8},
    "four-lions": {"title": "Four Lions", "year": 2010, "director": "Chris Morris", "rightsHolder": "Film4 / StudioCanal", "imdbRating": 7.3},
    "foxcatcher": {"title": "Foxcatcher", "year": 2014, "director": "Bennett Miller", "rightsHolder": "Sony Pictures Classics", "imdbRating": 7.0},
    "from-dusk-till-dawn": {"title": "From Dusk Till Dawn", "year": 1996, "director": "Robert Rodriguez", "rightsHolder": "Miramax / Dimension Films", "imdbRating": 7.2},
    "from-russia-with-love": {"title": "From Russia with Love", "year": 1963, "director": "Terence Young", "rightsHolder": "Eon Productions / MGM", "imdbRating": 7.3},
    "fury": {"title": "Fury", "year": 2014, "director": "David Ayer", "rightsHolder": "Sony Pictures", "imdbRating": 7.6},
    "ghost": {"title": "Ghost", "year": 1990, "director": "Jerry Zucker", "rightsHolder": "Paramount Pictures", "imdbRating": 7.1},
    "ghostbusters": {"title": "Ghostbusters", "year": 1984, "director": "Ivan Reitman", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.8},
    "glengarry-glen-ross": {"title": "Glengarry Glen Ross", "year": 1992, "director": "James Foley", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 7.6},
    "good-morning-vietnam": {"title": "Good Morning Vietnam", "year": 1987, "director": "Barry Levinson", "rightsHolder": "Touchstone Pictures / Disney", "imdbRating": 7.3},
    "good-time": {"title": "Good Time", "year": 2017, "director": "Josh Safdie and Benny Safdie", "rightsHolder": "A24", "imdbRating": 7.3},
    "good-will-hunting": {"title": "Good Will Hunting", "year": 1997, "director": "Gus Van Sant", "rightsHolder": "Miramax", "imdbRating": 8.4},
    "goodfellas": {"title": "Goodfellas", "year": 1990, "director": "Martin Scorsese", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.7},
    "gran-torino": {"title": "Gran Torino", "year": 2008, "director": "Clint Eastwood", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.1},
    "green-book": {"title": "Green Book", "year": 2018, "director": "Peter Farrelly", "rightsHolder": "Universal Pictures / Participant", "imdbRating": 8.2},
    "gremlins": {"title": "Gremlins", "year": 1984, "director": "Joe Dante", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.3},
    "gremlins-2": {"title": "Gremlins 2: The New Batch", "year": 1990, "director": "Joe Dante", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.5},
    "halloween-3": {"title": "Halloween III: Season of the Witch", "year": 1982, "director": "Tommy Lee Wallace", "rightsHolder": "Universal Pictures", "imdbRating": 5.2},
    "halloweentown-2": {"title": "Halloweentown II: Kalabar's Revenge", "year": 2001, "director": "Mary Lambert", "rightsHolder": "Disney Channel / Walt Disney Television", "imdbRating": 6.3},
    "hostel-2": {"title": "Hostel: Part II", "year": 2007, "director": "Eli Roth", "rightsHolder": "Lionsgate", "imdbRating": 5.5},
    "house-of-gucci": {"title": "House of Gucci", "year": 2021, "director": "Ridley Scott", "rightsHolder": "MGM / Universal Pictures", "imdbRating": 6.6},
    "i-saw-the-tv-glow": {"title": "I Saw the TV Glow", "year": 2024, "director": "Jane Schoenbrun", "rightsHolder": "A24", "imdbRating": 5.8},
    "in-the-loop": {"title": "In the Loop", "year": 2009, "director": "Armando Iannucci", "rightsHolder": "IFC Films / BBC Films", "imdbRating": 7.4},
    "in-the-name-of-the-father": {"title": "In the Name of the Father", "year": 1993, "director": "Jim Sheridan", "rightsHolder": "Universal Pictures", "imdbRating": 8.1},
    "incredibles-2": {"title": "Incredibles 2", "year": 2018, "director": "Brad Bird", "rightsHolder": "Pixar / Walt Disney Pictures", "imdbRating": 7.5},
    "indiana-jones-3": {"title": "Indiana Jones and the Last Crusade", "year": 1989, "director": "Steven Spielberg", "rightsHolder": "Lucasfilm / Paramount Pictures", "imdbRating": 8.2},
    "insidious": {"title": "Insidious", "year": 2010, "director": "James Wan", "rightsHolder": "FilmDistrict / Sony Pictures", "imdbRating": 6.8},
    "insomnia": {"title": "Insomnia", "year": 2002, "director": "Christopher Nolan", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.2},
    "inspector-gadget-2": {"title": "Inspector Gadget 2", "year": 2003, "director": "Alex Zamm", "rightsHolder": "Walt Disney Pictures", "imdbRating": 3.5},
    "into-the-wild": {"title": "Into the Wild", "year": 2007, "director": "Sean Penn", "rightsHolder": "Paramount Vantage", "imdbRating": 8.0},
    "jackie-brown": {"title": "Jackie Brown", "year": 1997, "director": "Quentin Tarantino", "rightsHolder": "Miramax", "imdbRating": 7.5},
    "jacob-s-ladder": {"title": "Jacob's Ladder", "year": 1990, "director": "Adrian Lyne", "rightsHolder": "TriStar Pictures / StudioCanal", "imdbRating": 7.4},
    "jaws": {"title": "Jaws", "year": 1975, "director": "Steven Spielberg", "rightsHolder": "Universal Pictures", "imdbRating": 8.1},
    "julius-caesar": {"title": "Julius Caesar", "year": 1953, "director": "Joseph L. Mankiewicz", "rightsHolder": "MGM", "imdbRating": 7.2},
    "jumpin-jack-flash": {"title": "Jumpin' Jack Flash", "year": 1986, "director": "Penny Marshall", "rightsHolder": "20th Century Studios", "imdbRating": 6.0},
    "k-pax": {"title": "K-PAX", "year": 2001, "director": "Iain Softley", "rightsHolder": "Universal Pictures", "imdbRating": 7.4},
    "king-kong": {"title": "King Kong", "year": 1933, "director": "Merian C. Cooper and Ernest B. Schoedsack", "rightsHolder": "RKO Pictures / Warner Bros. Discovery", "imdbRating": 7.9},
    "labyrinth": {"title": "Labyrinth", "year": 1986, "director": "Jim Henson", "rightsHolder": "TriStar Pictures / The Jim Henson Company", "imdbRating": 7.3},
    "lady-and-the-tramp": {"title": "Lady and the Tramp", "year": 1955, "director": "Clyde Geronimi, Wilfred Jackson and Hamilton Luske", "rightsHolder": "Walt Disney Pictures", "imdbRating": 7.3},
    "late-night-with-the-devil": {"title": "Late Night with the Devil", "year": 2023, "director": "Cameron Cairnes and Colin Cairnes", "rightsHolder": "IFC Films / Shudder", "imdbRating": 7.0},
    "leon-the-professional": {"title": "Léon: The Professional", "year": 1994, "director": "Luc Besson", "rightsHolder": "Gaumont / Columbia Pictures", "imdbRating": 8.5},
    "lethal-weapon": {"title": "Lethal Weapon", "year": 1987, "director": "Richard Donner", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.6},
    "lethal-weapon-3": {"title": "Lethal Weapon 3", "year": 1992, "director": "Richard Donner", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.7},
    "lincoln": {"title": "Lincoln", "year": 2012, "director": "Steven Spielberg", "rightsHolder": "DreamWorks Pictures / 20th Century Studios", "imdbRating": 7.3},
    "little-miss-sunshine": {"title": "Little Miss Sunshine", "year": 2006, "director": "Jonathan Dayton and Valerie Faris", "rightsHolder": "Searchlight Pictures", "imdbRating": 7.8},
    "live-and-let-die": {"title": "Live and Let Die", "year": 1973, "director": "Guy Hamilton", "rightsHolder": "Eon Productions / MGM", "imdbRating": 6.7},
    "lolita": {"title": "Lolita", "year": 1962, "director": "Stanley Kubrick", "rightsHolder": "MGM / Warner Bros. Discovery", "imdbRating": 7.5},
    "lost-in-translation": {"title": "Lost In Translation", "year": 2003, "director": "Sofia Coppola", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.7},
    "lucky-number-slevin": {"title": "Lucky Number Slevin", "year": 2006, "director": "Paul McGuigan", "rightsHolder": "The Weinstein Company / MGM", "imdbRating": 7.7},
    "manchester-by-the-sea": {"title": "Manchester By the Sea", "year": 2016, "director": "Kenneth Lonergan", "rightsHolder": "Amazon Studios / Roadside Attractions", "imdbRating": 7.8},
    "marathon-man": {"title": "Marathon Man", "year": 1976, "director": "John Schlesinger", "rightsHolder": "Paramount Pictures", "imdbRating": 7.4},
    "marty-supreme": {"title": "Marty Supreme", "year": 2025, "director": "Josh Safdie", "rightsHolder": "A24", "imdbRating": 7.6},
    "master-and-commander": {"title": "Master and Commander", "year": 2003, "director": "Peter Weir", "rightsHolder": "20th Century Studios", "imdbRating": 7.5},
    "matilda": {"title": "Matilda", "year": 1996, "director": "Danny DeVito", "rightsHolder": "TriStar Pictures / Sony Pictures", "imdbRating": 7.0},
    "mean-girls": {"title": "Mean Girls", "year": 2004, "director": "Mark Waters", "rightsHolder": "Paramount Pictures", "imdbRating": 7.1},
    "memento": {"title": "Memento", "year": 2000, "director": "Christopher Nolan", "rightsHolder": "Summit Entertainment", "imdbRating": 8.4},
    "men-in-black-2": {"title": "Men in Black II", "year": 2002, "director": "Barry Sonnenfeld", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 6.2},
    "menace-2-society": {"title": "Menace II Society", "year": 1993, "director": "Albert Hughes and Allen Hughes", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 7.5},
    "metropolitan": {"title": "Metropolitan", "year": 1990, "director": "Whit Stillman", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 7.2},
    "mickey-17": {"title": "Mickey 17", "year": 2025, "director": "Bong Joon Ho", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.7},
    "mid90s": {"title": "Mid90s", "year": 2018, "director": "Jonah Hill", "rightsHolder": "A24", "imdbRating": 7.4},
    "midsommar": {"title": "Midsommar", "year": 2019, "director": "Ari Aster", "rightsHolder": "A24", "imdbRating": 7.1},
    "mission-impossible-3": {"title": "Mission: Impossible III", "year": 2006, "director": "J. J. Abrams", "rightsHolder": "Paramount Pictures", "imdbRating": 6.9},
    "molly-s-game": {"title": "Molly's Game", "year": 2017, "director": "Aaron Sorkin", "rightsHolder": "STX Entertainment", "imdbRating": 7.4},
    "mommie-dearest": {"title": "Mommie Dearest", "year": 1981, "director": "Frank Perry", "rightsHolder": "Paramount Pictures", "imdbRating": 6.7},
    "mona-lisa-smile": {"title": "Mona Lisa Smile", "year": 2003, "director": "Mike Newell", "rightsHolder": "Revolution Studios / Sony Pictures", "imdbRating": 6.6},
    "monster": {"title": "Monster", "year": 2003, "director": "Patty Jenkins", "rightsHolder": "Newmarket Films / Lionsgate", "imdbRating": 7.3},
    "moonrise-kingdom": {"title": "Moonrise Kingdom", "year": 2012, "director": "Wes Anderson", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.7},
    "morbius": {"title": "Morbius", "year": 2022, "director": "Daniel Espinosa", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 5.1},
    "mulholland-drive": {"title": "Mulholland Drive", "year": 2001, "director": "David Lynch", "rightsHolder": "Universal Pictures / StudioCanal", "imdbRating": 7.9},
    "munich": {"title": "Munich", "year": 2005, "director": "Steven Spielberg", "rightsHolder": "Universal Pictures / DreamWorks Pictures", "imdbRating": 7.5},
    "murder-at-1600": {"title": "Murder at 1600", "year": 1997, "director": "Dwight H. Little", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.1},
    "murder-on-the-orient-express": {"title": "Murder on the Orient Express", "year": 1974, "director": "Sidney Lumet", "rightsHolder": "EMI Films / Paramount Pictures", "imdbRating": 7.2},
    "national-treasure": {"title": "National Treasure", "year": 2004, "director": "Jon Turteltaub", "rightsHolder": "Walt Disney Pictures", "imdbRating": 6.9},
    "neon-demon": {"title": "The Neon Demon", "year": 2016, "director": "Nicolas Winding Refn", "rightsHolder": "Amazon Studios / Broad Green Pictures", "imdbRating": 6.1},
    "night-school": {"title": "Night School", "year": 2018, "director": "Malcolm D. Lee", "rightsHolder": "Universal Pictures", "imdbRating": 5.6},
    "nightcrawler": {"title": "Nightcrawler", "year": 2014, "director": "Dan Gilroy", "rightsHolder": "Open Road Films", "imdbRating": 7.8},
    "no-country-for-old-men": {"title": "No Country for Old Men", "year": 2007, "director": "Joel Coen and Ethan Coen", "rightsHolder": "Miramax / Paramount Vantage", "imdbRating": 8.2},
    "no-hard-feelings": {"title": "No Hard Feelings", "year": 2023, "director": "Gene Stupnitsky", "rightsHolder": "Sony Pictures", "imdbRating": 6.3},
    "no-strings-attached": {"title": "No Strings Attached", "year": 2011, "director": "Ivan Reitman", "rightsHolder": "Paramount Pictures", "imdbRating": 6.2},
    "nocturnal-animals": {"title": "Nocturnal Animals", "year": 2016, "director": "Tom Ford", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.4},
    "nosferatu": {"title": "Nosferatu", "year": 2024, "director": "Robert Eggers", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.1},
    "notorious": {"title": "Notorious", "year": 1946, "director": "Alfred Hitchcock", "rightsHolder": "RKO Radio Pictures / Disney", "imdbRating": 7.9},
    "novocaine": {"title": "Novocaine", "year": 2025, "director": "Dan Berk and Robert Olsen", "rightsHolder": "Paramount Pictures", "imdbRating": 6.5},
    "ocean-s-eleven": {"title": "Ocean's Eleven", "year": 2001, "director": "Steven Soderbergh", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.7},
    "ocean-s-twelve": {"title": "Ocean's Twelve", "year": 2004, "director": "Steven Soderbergh", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.5},
    "octopussy": {"title": "Octopussy", "year": 1983, "director": "John Glen", "rightsHolder": "Eon Productions / MGM", "imdbRating": 6.5},
    "once-upon-a-time-in-america": {"title": "Once Upon a Time in America", "year": 1984, "director": "Sergio Leone", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.3},
    "once-upon-a-time-in-hollywood": {"title": "Once Upon a Time in Hollywood", "year": 2019, "director": "Quentin Tarantino", "rightsHolder": "Sony Pictures", "imdbRating": 7.6},
    "paddington": {"title": "Paddington", "year": 2014, "director": "Paul King", "rightsHolder": "StudioCanal", "imdbRating": 7.3},
    "paris-texas": {"title": "Paris, Texas", "year": 1984, "director": "Wim Wenders", "rightsHolder": "20th Century Studios / Janus Films", "imdbRating": 8.1},
    "penguins-of-madagascar": {"title": "Penguins of Madagascar", "year": 2014, "director": "Eric Darnell and Simon J. Smith", "rightsHolder": "DreamWorks Animation / 20th Century Fox", "imdbRating": 6.7},
    "percy-jackson": {"title": "Percy Jackson & the Olympians: The Lightning Thief", "year": 2010, "director": "Chris Columbus", "rightsHolder": "20th Century Studios", "imdbRating": 5.9},
    "pig": {"title": "Pig", "year": 2021, "director": "Michael Sarnoski", "rightsHolder": "Neon", "imdbRating": 6.9},
    "pineapple-express": {"title": "Pineapple Express", "year": 2008, "director": "David Gordon Green", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 6.9},
    "pinocchio": {"title": "Pinocchio", "year": 2022, "director": "Robert Zemeckis", "rightsHolder": "Walt Disney Pictures", "imdbRating": 5.1},
    "point-break": {"title": "Point Break", "year": 1991, "director": "Kathryn Bigelow", "rightsHolder": "20th Century Studios", "imdbRating": 7.3},
    "poor-things": {"title": "Poor Things", "year": 2023, "director": "Yorgos Lanthimos", "rightsHolder": "Searchlight Pictures", "imdbRating": 7.7},
    "predator": {"title": "Predator", "year": 1987, "director": "John McTiernan", "rightsHolder": "20th Century Studios", "imdbRating": 7.8},
    "primal-fear": {"title": "Primal Fear", "year": 1996, "director": "Gregory Hoblit", "rightsHolder": "Paramount Pictures", "imdbRating": 7.7},
    "primer": {"title": "Primer", "year": 2004, "director": "Shane Carruth", "rightsHolder": "THINKFilm", "imdbRating": 6.7},
    "pulp-fiction": {"title": "Pulp Fiction", "year": 1994, "director": "Quentin Tarantino", "rightsHolder": "Miramax", "imdbRating": 8.8},
    "quick-change": {"title": "Quick Change", "year": 1990, "director": "Bill Murray and Howard Franklin", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.8},
    "rainman": {"title": "Rain Man", "year": 1988, "director": "Barry Levinson", "rightsHolder": "MGM / United Artists", "imdbRating": 8.0},
    "raising-cain": {"title": "Raising Cain", "year": 1992, "director": "Brian De Palma", "rightsHolder": "Universal Pictures", "imdbRating": 6.1},
    "rear-window": {"title": "Rear Window", "year": 1954, "director": "Alfred Hitchcock", "rightsHolder": "Universal Pictures", "imdbRating": 8.4},
    "requiem-for-a-dream": {"title": "Requiem for a Dream", "year": 2000, "director": "Darren Aronofsky", "rightsHolder": "Artisan Entertainment / Lionsgate", "imdbRating": 8.3},
    "road-house": {"title": "Road House", "year": 1989, "director": "Rowdy Herrington", "rightsHolder": "MGM / United Artists", "imdbRating": 6.7},
    "robin-hood": {"title": "Robin Hood", "year": 1973, "director": "Wolfgang Reitherman", "rightsHolder": "Walt Disney Pictures", "imdbRating": 7.5},
    "robocop-2": {"title": "RoboCop 2", "year": 1990, "director": "Irvin Kershner", "rightsHolder": "Orion Pictures / MGM", "imdbRating": 5.8},
    "rock-n-roll-high-school": {"title": "Rock 'n' Roll High School", "year": 1979, "director": "Allan Arkush", "rightsHolder": "New World Pictures", "imdbRating": 6.6},
    "rocky": {"title": "Rocky", "year": 1976, "director": "John G. Avildsen", "rightsHolder": "MGM / United Artists", "imdbRating": 8.1},
    "roman-holiday": {"title": "Roman Holiday", "year": 1953, "director": "William Wyler", "rightsHolder": "Paramount Pictures", "imdbRating": 8.0},
    "sabrina": {"title": "Sabrina", "year": 1954, "director": "Billy Wilder", "rightsHolder": "Paramount Pictures", "imdbRating": 7.6},
    "sandlot": {"title": "The Sandlot", "year": 1993, "director": "David Mickey Evans", "rightsHolder": "20th Century Studios", "imdbRating": 7.8},
    "say-anything": {"title": "Say Anything", "year": 1989, "director": "Cameron Crowe", "rightsHolder": "20th Century Studios", "imdbRating": 7.3},
    "scarface": {"title": "Scarface", "year": 1983, "director": "Brian De Palma", "rightsHolder": "Universal Pictures", "imdbRating": 8.3},
    "school-ties": {"title": "School Ties", "year": 1992, "director": "Robert Mandel", "rightsHolder": "Paramount Pictures", "imdbRating": 6.9},
    "scott-pilgrim-vs-the-world": {"title": "Scott Pilgrim vs. the World", "year": 2010, "director": "Edgar Wright", "rightsHolder": "Universal Pictures", "imdbRating": 7.5},
    "scream": {"title": "Scream", "year": 1996, "director": "Wes Craven", "rightsHolder": "Dimension Films / Paramount Pictures", "imdbRating": 7.4},
    "scrooge": {"title": "Scrooge", "year": 1970, "director": "Ronald Neame", "rightsHolder": "Cinema Center Films / Paramount Pictures", "imdbRating": 7.5},
    "scrooge-a-christmas-carol": {"title": "Scrooge: A Christmas Carol", "year": 2022, "director": "Stephen Donnelly", "rightsHolder": "Netflix", "imdbRating": 6.2},
    "sergeant-york": {"title": "Sergeant York", "year": 1941, "director": "Howard Hawks", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.7},
    "shaun-of-the-dead": {"title": "Shaun of the Dead", "year": 2004, "director": "Edgar Wright", "rightsHolder": "Universal Pictures / StudioCanal", "imdbRating": 7.8},
    "shawshank-redemption": {"title": "Shawshank Redemption", "year": 1994, "director": "Frank Darabont", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 9.3},
    "sherlock-holmes": {"title": "Sherlock Holmes", "year": 2009, "director": "Guy Ritchie", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.5},
    "sherlock-holmes-2": {"title": "Sherlock Holmes: A Game of Shadows", "year": 2011, "director": "Guy Ritchie", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.4},
    "sicario": {"title": "Sicario", "year": 2015, "director": "Denis Villeneuve", "rightsHolder": "Lionsgate", "imdbRating": 7.7},
    "sing-sing": {"title": "Sing Sing", "year": 2023, "director": "Greg Kwedar", "rightsHolder": "A24", "imdbRating": 7.6},
    "singin-in-the-rain": {"title": "Singin' in the Rain", "year": 1952, "director": "Stanley Donen and Gene Kelly", "rightsHolder": "MGM / Warner Bros. Discovery", "imdbRating": 8.3},
    "sleeping-beauty": {"title": "Sleeping Beauty", "year": 1959, "director": "Clyde Geronimi", "rightsHolder": "Walt Disney Pictures", "imdbRating": 7.2},
    "sleepless-in-seattle": {"title": "Sleepless in Seattle", "year": 1993, "director": "Nora Ephron", "rightsHolder": "TriStar Pictures / Sony Pictures", "imdbRating": 6.8},
    "snowden": {"title": "Snowden", "year": 2016, "director": "Oliver Stone", "rightsHolder": "Open Road Films", "imdbRating": 7.3},
    "some-like-it-hot": {"title": "Some Like It Hot", "year": 1959, "director": "Billy Wilder", "rightsHolder": "United Artists / MGM", "imdbRating": 8.2},
    "spirited": {"title": "Spirited", "year": 2022, "director": "Sean Anders", "rightsHolder": "Apple Original Films", "imdbRating": 6.6},
    "spotlight": {"title": "Spotlight", "year": 2015, "director": "Tom McCarthy", "rightsHolder": "Open Road Films / Participant", "imdbRating": 8.1},
    "spy-kids-all-the-time-in-the-world": {"title": "Spy Kids 4: All the Time in the World", "year": 2011, "director": "Robert Rodriguez", "rightsHolder": "Dimension Films / The Weinstein Company", "imdbRating": 3.6},
    "stand-by-me": {"title": "Stand By Me", "year": 1986, "director": "Rob Reiner", "rightsHolder": "Columbia Pictures", "imdbRating": 8.1},
    "sunset-boulevard": {"title": "Sunset Boulevard", "year": 1950, "director": "Billy Wilder", "rightsHolder": "Paramount Pictures", "imdbRating": 8.4},
    "superbad": {"title": "Superbad", "year": 2007, "director": "Greg Mottola", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.6},
    "superman": {"title": "Superman", "year": 1978, "director": "Richard Donner", "rightsHolder": "Warner Bros. Pictures / DC", "imdbRating": 7.4},
    "swimfan": {"title": "Swimfan", "year": 2002, "director": "John Polson", "rightsHolder": "20th Century Studios", "imdbRating": 5.1},
    "taxi-driver": {"title": "Taxi Driver", "year": 1976, "director": "Martin Scorsese", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 8.2},
    "ted": {"title": "Ted", "year": 2012, "director": "Seth MacFarlane", "rightsHolder": "Universal Pictures", "imdbRating": 6.9},
    "tenet": {"title": "Tenet", "year": 2020, "director": "Christopher Nolan", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.3},
    "terminator": {"title": "The Terminator", "year": 1984, "director": "James Cameron", "rightsHolder": "MGM / Orion Pictures", "imdbRating": 8.1},
    "the-adventures-of-sherlock-holmes": {"title": "The Adventures of Sherlock Holmes", "year": 1939, "director": "Alfred L. Werker", "rightsHolder": "20th Century Studios", "imdbRating": 7.2},
    "the-age-of-innocence": {"title": "The Age of Innocence", "year": 1993, "director": "Martin Scorsese", "rightsHolder": "Columbia Pictures", "imdbRating": 7.2},
    "the-aviator": {"title": "The Aviator", "year": 2004, "director": "Martin Scorsese", "rightsHolder": "Miramax / Warner Bros. Pictures", "imdbRating": 7.5},
    "the-babadook": {"title": "The Babadook", "year": 2014, "director": "Jennifer Kent", "rightsHolder": "IFC Films / Umbrella Entertainment", "imdbRating": 6.8},
    "the-banana-splits-movie": {"title": "The Banana Splits Movie", "year": 2019, "director": "Danishka Esterhazy", "rightsHolder": "Warner Bros. Home Entertainment", "imdbRating": 5.1},
    "the-banshees-of-inisherin": {"title": "The Banshees of Inisherin", "year": 2022, "director": "Martin McDonagh", "rightsHolder": "Searchlight Pictures", "imdbRating": 7.6},
    "the-bfg": {"title": "The BFG", "year": 2016, "director": "Steven Spielberg", "rightsHolder": "Walt Disney Pictures / Amblin Entertainment", "imdbRating": 6.3},
    "the-blues-brothers": {"title": "The Blues Brothers", "year": 1980, "director": "John Landis", "rightsHolder": "Universal Pictures", "imdbRating": 7.9},
    "the-bounty": {"title": "The Bounty", "year": 1984, "director": "Roger Donaldson", "rightsHolder": "Dino De Laurentiis Company / MGM", "imdbRating": 7.1},
    "the-breakfast-club": {"title": "The Breakfast Club", "year": 1985, "director": "John Hughes", "rightsHolder": "Universal Pictures", "imdbRating": 7.8},
    "the-cat-in-the-hat": {"title": "The Cat in the Hat", "year": 2003, "director": "Bo Welch", "rightsHolder": "Universal Pictures / DreamWorks Pictures", "imdbRating": 4.2},
    "the-change-up": {"title": "The Change-Up", "year": 2011, "director": "David Dobkin", "rightsHolder": "Universal Pictures", "imdbRating": 6.3},
    "the-conjuring": {"title": "The Conjuring", "year": 2013, "director": "James Wan", "rightsHolder": "Warner Bros. Pictures / New Line Cinema", "imdbRating": 7.5},
    "the-conversation": {"title": "The Conversation", "year": 1974, "director": "Francis Ford Coppola", "rightsHolder": "Paramount Pictures", "imdbRating": 7.7},
    "the-curious-case-of-benjamin-button": {"title": "The Curious Case of Benjamin Button", "year": 2008, "director": "David Fincher", "rightsHolder": "Paramount Pictures / Warner Bros. Pictures", "imdbRating": 7.8},
    "the-cutting-edge": {"title": "The Cutting Edge", "year": 1992, "director": "Paul Michael Glaser", "rightsHolder": "MGM", "imdbRating": 6.9},
    "the-departed": {"title": "The Departed", "year": 2006, "director": "Martin Scorsese", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.5},
    "the-elephant-man": {"title": "The Elephant Man", "year": 1980, "director": "David Lynch", "rightsHolder": "Paramount Pictures / StudioCanal", "imdbRating": 8.2},
    "the-eyes-of-tammy-faye": {"title": "The Eyes of Tammy Faye", "year": 2021, "director": "Michael Showalter", "rightsHolder": "Searchlight Pictures", "imdbRating": 6.6},
    "the-farewell": {"title": "The Farewell", "year": 2019, "director": "Lulu Wang", "rightsHolder": "A24", "imdbRating": 7.5},
    "the-father": {"title": "The Father", "year": 2020, "director": "Florian Zeller", "rightsHolder": "Sony Pictures Classics", "imdbRating": 8.2},
    "the-florida-project": {"title": "The Florida Project", "year": 2017, "director": "Sean Baker", "rightsHolder": "A24", "imdbRating": 7.6},
    "the-game": {"title": "The Game", "year": 1997, "director": "David Fincher", "rightsHolder": "PolyGram Filmed Entertainment / Universal Pictures", "imdbRating": 7.7},
    "the-green-mile": {"title": "The Green Mile", "year": 1999, "director": "Frank Darabont", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.6},
    "the-hurricane": {"title": "The Hurricane", "year": 1999, "director": "Norman Jewison", "rightsHolder": "Universal Pictures", "imdbRating": 7.6},
    "the-hustler": {"title": "The Hustler", "year": 1961, "director": "Robert Rossen", "rightsHolder": "20th Century Studios", "imdbRating": 7.9},
    "the-irishman": {"title": "The Irishman", "year": 2019, "director": "Martin Scorsese", "rightsHolder": "Netflix", "imdbRating": 7.8},
    "the-iron-giant": {"title": "The Iron Giant", "year": 1999, "director": "Brad Bird", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.1},
    "the-kids-are-all-right": {"title": "The Kids Are All Right", "year": 2010, "director": "Lisa Cholodenko", "rightsHolder": "Focus Features / Universal Pictures", "imdbRating": 7.0},
    "the-lego-batman-movie": {"title": "The Lego Batman Movie", "year": 2017, "director": "Chris McKay", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.3},
    "the-limey": {"title": "The Limey", "year": 1999, "director": "Steven Soderbergh", "rightsHolder": "Artisan Entertainment / Lionsgate", "imdbRating": 6.9},
    "the-lobster": {"title": "The Lobster", "year": 2015, "director": "Yorgos Lanthimos", "rightsHolder": "A24 / Film4", "imdbRating": 7.1},
    "the-lord-of-rings-the-two-towers": {"title": "The Lord of the Rings: The Two Towers", "year": 2002, "director": "Peter Jackson", "rightsHolder": "New Line Cinema / Warner Bros. Discovery", "imdbRating": 8.8},
    "the-lost-daughter": {"title": "The Lost Daughter", "year": 2021, "director": "Maggie Gyllenhaal", "rightsHolder": "Netflix", "imdbRating": 6.7},
    "the-man-who-fell-to-earth": {"title": "The Man Who Fell to Earth", "year": 1976, "director": "Nicolas Roeg", "rightsHolder": "StudioCanal", "imdbRating": 6.6},
    "the-martian": {"title": "The Martian", "year": 2015, "director": "Ridley Scott", "rightsHolder": "20th Century Studios", "imdbRating": 8.0},
    "the-master": {"title": "The Master", "year": 2012, "director": "Paul Thomas Anderson", "rightsHolder": "The Weinstein Company", "imdbRating": 7.1},
    "the-mist": {"title": "The Mist", "year": 2007, "director": "Frank Darabont", "rightsHolder": "MGM / Dimension Films", "imdbRating": 7.1},
    "the-muppet-christmas-carol": {"title": "The Muppet Christmas Carol", "year": 1992, "director": "Brian Henson", "rightsHolder": "Walt Disney Pictures / The Jim Henson Company", "imdbRating": 7.8},
    "the-notebook": {"title": "The Notebook", "year": 2004, "director": "Nick Cassavetes", "rightsHolder": "New Line Cinema / Warner Bros. Pictures", "imdbRating": 7.8},
    "the-polar-express": {"title": "The Polar Express", "year": 2004, "director": "Robert Zemeckis", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.6},
    "the-punisher": {"title": "The Punisher", "year": 2004, "director": "Jonathan Hensleigh", "rightsHolder": "Lionsgate / Marvel Enterprises", "imdbRating": 6.4},
    "the-ringer": {"title": "The Ringer", "year": 2005, "director": "Barry W. Blaustein", "rightsHolder": "Searchlight Pictures", "imdbRating": 5.8},
    "the-road": {"title": "The Road", "year": 2009, "director": "John Hillcoat", "rightsHolder": "Dimension Films", "imdbRating": 7.2},
    "the-rocky-horror-picture-show": {"title": "The Rocky Horror Picture Show", "year": 1975, "director": "Jim Sharman", "rightsHolder": "20th Century Studios", "imdbRating": 7.4},
    "the-shining": {"title": "The Shining", "year": 1980, "director": "Stanley Kubrick", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 8.4},
    "the-social-network": {"title": "The Social Network", "year": 2010, "director": "David Fincher", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 7.8},
    "the-space-children": {"title": "The Space Children", "year": 1958, "director": "Jack Arnold", "rightsHolder": "Paramount Pictures", "imdbRating": 4.4},
    "the-spongebob-movie-sponge-out-of-water": {"title": "The SpongeBob Movie: Sponge Out of Water", "year": 2015, "director": "Paul Tibbitt", "rightsHolder": "Paramount Pictures / Nickelodeon Movies", "imdbRating": 6.0},
    "the-sting": {"title": "The Sting", "year": 1973, "director": "George Roy Hill", "rightsHolder": "Universal Pictures", "imdbRating": 8.2},
    "the-sure-thing": {"title": "The Sure Thing", "year": 1985, "director": "Rob Reiner", "rightsHolder": "Embassy Pictures / MGM", "imdbRating": 7.0},
    "the-talented-mr-ripley": {"title": "The Talented Mr. Ripley", "year": 1999, "director": "Anthony Minghella", "rightsHolder": "Paramount Pictures / Miramax", "imdbRating": 7.4},
    "the-thin-red-line": {"title": "The Thin Red Line", "year": 1998, "director": "Terrence Malick", "rightsHolder": "20th Century Studios", "imdbRating": 7.6},
    "the-tingler": {"title": "The Tingler", "year": 1959, "director": "William Castle", "rightsHolder": "Columbia Pictures / Sony Pictures", "imdbRating": 6.6},
    "the-usual-suspects": {"title": "The Usual Suspects", "year": 1995, "director": "Bryan Singer", "rightsHolder": "MGM / Gramercy Pictures", "imdbRating": 8.5},
    "the-world-s-end": {"title": "The World's End", "year": 2013, "director": "Edgar Wright", "rightsHolder": "Universal Pictures / Focus Features", "imdbRating": 6.9},
    "thelma-and-louise": {"title": "Thelma & Louise", "year": 1991, "director": "Ridley Scott", "rightsHolder": "MGM", "imdbRating": 7.6},
    "there-will-be-blood": {"title": "There Will Be Blood", "year": 2007, "director": "Paul Thomas Anderson", "rightsHolder": "Paramount Vantage / Miramax Films", "imdbRating": 8.2},
    "thunder-force": {"title": "Thunder Force", "year": 2021, "director": "Ben Falcone", "rightsHolder": "Netflix", "imdbRating": 4.6},
    "to-kill-a-mockingbird": {"title": "To Kill a Mockingbird", "year": 1962, "director": "Robert Mulligan", "rightsHolder": "Universal Pictures", "imdbRating": 8.2},
    "tower": {"title": "Tower", "year": 2016, "director": "Keith Maitland", "rightsHolder": "Kino Lorber", "imdbRating": 7.9},
    "trading-places": {"title": "Trading Places", "year": 1983, "director": "John Landis", "rightsHolder": "Paramount Pictures", "imdbRating": 7.5},
    "trainspotting-2": {"title": "T2 Trainspotting", "year": 2017, "director": "Danny Boyle", "rightsHolder": "Sony Pictures", "imdbRating": 7.1},
    "trick-r-treat": {"title": "Trick 'r Treat", "year": 2007, "director": "Michael Dougherty", "rightsHolder": "Warner Bros. Pictures / Legendary Pictures", "imdbRating": 6.7},
    "true-grit": {"title": "True Grit", "year": 2010, "director": "Joel Coen and Ethan Coen", "rightsHolder": "Paramount Pictures", "imdbRating": 7.6},
    "true-lies": {"title": "True Lies", "year": 1994, "director": "James Cameron", "rightsHolder": "20th Century Studios", "imdbRating": 7.3},
    "twilight-eclipse": {"title": "The Twilight Saga: Eclipse", "year": 2010, "director": "David Slade", "rightsHolder": "Summit Entertainment / Lionsgate", "imdbRating": 5.1},
    "two-lovers": {"title": "Two Lovers", "year": 2008, "director": "James Gray", "rightsHolder": "Magnolia Pictures", "imdbRating": 7.0},
    "under-the-skin": {"title": "Under the Skin", "year": 2013, "director": "Jonathan Glazer", "rightsHolder": "A24 / StudioCanal", "imdbRating": 6.3},
    "unfriended": {"title": "Unfriended", "year": 2014, "director": "Levan Gabriadze", "rightsHolder": "Universal Pictures / Blumhouse Productions", "imdbRating": 5.6},
    "us": {"title": "Us", "year": 2019, "director": "Jordan Peele", "rightsHolder": "Universal Pictures", "imdbRating": 6.8},
    "van-wilder": {"title": "National Lampoon's Van Wilder", "year": 2002, "director": "Walt Becker", "rightsHolder": "Lionsgate / Artisan Entertainment", "imdbRating": 6.4},
    "viva-las-vegas": {"title": "Viva Las Vegas", "year": 1964, "director": "George Sidney", "rightsHolder": "MGM / Warner Bros. Discovery", "imdbRating": 6.4},
    "wall-e": {"title": "WALL-E", "year": 2008, "director": "Andrew Stanton", "rightsHolder": "Pixar / Walt Disney Pictures", "imdbRating": 8.4},
    "watchmen": {"title": "Watchmen", "year": 2009, "director": "Zack Snyder", "rightsHolder": "Warner Bros. Pictures / Paramount Pictures", "imdbRating": 7.6},
    "we-bought-a-zoo": {"title": "We Bought a Zoo", "year": 2011, "director": "Cameron Crowe", "rightsHolder": "20th Century Studios", "imdbRating": 7.0},
    "weapons": {"title": "Weapons", "year": 2025, "director": "Zach Cregger", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 7.4},
    "west-side-story": {"title": "West Side Story", "year": 1961, "director": "Jerome Robbins and Robert Wise", "rightsHolder": "United Artists / MGM", "imdbRating": 7.6},
    "wet-hot-american-summer": {"title": "Wet Hot American Summer", "year": 2001, "director": "David Wain", "rightsHolder": "USA Films / Universal Pictures", "imdbRating": 6.5},
    "what-we-do-in-the-shadows": {"title": "What We Do in the Shadows", "year": 2014, "director": "Jemaine Clement and Taika Waititi", "rightsHolder": "The Orchard / Paramount Pictures", "imdbRating": 7.6},
    "when-harry-met-sally": {"title": "When Harry Met Sally...", "year": 1989, "director": "Rob Reiner", "rightsHolder": "Castle Rock Entertainment / MGM", "imdbRating": 7.7},
    "wonder-boys": {"title": "Wonder Boys", "year": 2000, "director": "Curtis Hanson", "rightsHolder": "Paramount Pictures", "imdbRating": 7.2},
    "yes-man": {"title": "Yes Man", "year": 2008, "director": "Peyton Reed", "rightsHolder": "Warner Bros. Pictures", "imdbRating": 6.8},
    "you-can-count-on-me": {"title": "You Can Count on Me", "year": 2000, "director": "Kenneth Lonergan", "rightsHolder": "Paramount Classics", "imdbRating": 7.5},
    "zero-dark-thirty": {"title": "Zero Dark Thirty", "year": 2012, "director": "Kathryn Bigelow", "rightsHolder": "Sony Pictures", "imdbRating": 7.4},
    "zodiac": {"title": "Zodiac", "year": 2007, "director": "David Fincher", "rightsHolder": "Paramount Pictures / Warner Bros. Pictures", "imdbRating": 7.7},
}

PATTERN = re.compile(r"^(?P<hhmm>\d{2}-\d{2})_(?P<period>am|pm|both|unknown)_(?P<precision>[^_]+)_(?P<movie>.+)_(?P<index>\d+)\.mp4$")
RANGE_PATTERN = re.compile(r"^(?P<start>\d{2}-\d{2})_(?P<start_period>am|pm|both)_(?P<end>\d{2}-\d{2})_(?P<end_period>am|pm|both)_range_(?P<movie>.+)_(?P<index>\d+)\.mp4$")
BROAD_PATTERN = re.compile(r"^(?P<label>[a-z0-9-]+)_broad_(?P<movie>.+)_(?P<index>\d+)\.mp4$")
FALLBACK_PATTERN = re.compile(r"^fallback_(?P<movie>.+)_(?P<index>\d+)\.mp4$")

BROAD_LABELS = {
    "before-dawn": {"display": "Before dawn", "spans": [{"start": "04:00", "end": "05:30"}]},
    "dawn": {"display": "Dawn", "spans": [{"start": "05:30", "end": "07:00"}]},
    "daytime": {"display": "Daytime", "spans": [{"start": "11:00", "end": "16:00"}]},
    "dusk": {"display": "Dusk", "spans": [{"start": "18:00", "end": "20:00"}]},
    "early-morning": {"display": "Early morning", "spans": [{"start": "05:00", "end": "07:00"}]},
    "evening": {"display": "Evening", "spans": [{"start": "19:00", "end": "22:00"}]},
    "middle-night": {"display": "Middle of the night", "spans": [{"start": "01:00", "end": "04:00"}]},
    "morning": {"display": "Morning", "spans": [{"start": "07:00", "end": "10:00"}]},
    "nighttime": {"display": "Nighttime", "spans": [{"start": "22:00", "end": "01:00"}]},
}

def titleize(slug):
    metadata = MOVIE_META.get(slug, {})
    if metadata.get("title"):
        return metadata["title"]
    small = {"a", "an", "and", "for", "of", "on", "the", "to", "v"}
    words = slug.split("-")
    titled = [word.upper() if word in {"ii", "iii"} else word.capitalize() for word in words]
    for i, word in enumerate(titled):
        if i and word.lower() in small:
            titled[i] = word.lower()
    return " ".join(titled)

def to_24h(hhmm, period):
    hour, minute = [int(part) for part in hhmm.split("-")]
    if period == "am":
        hour = 0 if hour == 12 else hour
    elif period == "pm":
        hour = 12 if hour == 12 else hour + 12
    return hour * 60 + minute

def from_minute(value):
    value %= 1440
    return f"{value // 60:02d}:{value % 60:02d}"

def range_spans_for(start_hhmm, start_period, end_hhmm, end_period):
    periods = ["am", "pm"] if "both" in {start_period, end_period} else [start_period]
    spans = []
    for period in periods:
        start = to_24h(start_hhmm, period if start_period == "both" else start_period)
        end = to_24h(end_hhmm, period if end_period == "both" else end_period)
        spans.append({"start": from_minute(start), "end": from_minute(end)})
    return spans


def spans_for(hhmm, period, precision):
    if precision == "fallback":
        return [{"start": "00:00", "end": "23:59"}]
    base_periods = ["am", "pm"] if period == "both" else [period]
    spans = []
    for item in base_periods:
        center = to_24h(hhmm, item)
        if precision == "exact":
            start = end = center
        elif precision == "before":
            start, end = center - FLEXIBLE_SPAN_MINUTES, center
        elif precision == "after":
            start, end = center, center + FLEXIBLE_SPAN_MINUTES
        elif precision == "approx":
            start, end = center - FLEXIBLE_SPAN_MINUTES, center + FLEXIBLE_SPAN_MINUTES
        else:
            start, end = center - 10, center + 10
        spans.append({"start": from_minute(start), "end": from_minute(end)})
    return spans

def priority_for(precision):
    return {
        "exact": 1,
        "before": 2,
        "after": 2,
        "approx": 3,
        "range": 4,
        "broad": 5,
        "fallback": 9,
    }.get(precision, 6)

def scene_payload(path, movie, display_time, period, precision, spans):
    metadata = MOVIE_META.get(movie, {})
    return {
        "id": path.stem,
        "src": f"assets/medias/videos/movie-scenes/{path.name}",
        "movieTitle": titleize(movie),
        "movieSlug": movie,
        "releaseYear": metadata.get("year"),
        "director": metadata.get("director", "Director to verify"),
        "rightsHolder": metadata.get("rightsHolder", "Rights holder to verify"),
        "imdbRating": metadata.get("imdbRating"),
        "displayTime": display_time,
        "period": period,
        "precision": precision,
        "priority": priority_for(precision),
        "spans": spans,
    }

def parse_scene(path):
    match = RANGE_PATTERN.match(path.name)
    if match:
        data = match.groupdict()
        period = data["start_period"] if data["start_period"] == data["end_period"] else "unknown"
        return scene_payload(
            path,
            data["movie"],
            f'{data["start"].replace("-", ":")}-{data["end"].replace("-", ":")}',
            period,
            "range",
            range_spans_for(data["start"], data["start_period"], data["end"], data["end_period"]),
        )

    match = PATTERN.match(path.name)
    if match:
        data = match.groupdict()
        return scene_payload(
            path,
            data["movie"],
            data["hhmm"].replace("-", ":"),
            data["period"],
            data["precision"],
            spans_for(data["hhmm"], data["period"], data["precision"]),
        )

    match = BROAD_PATTERN.match(path.name)
    if match:
        data = match.groupdict()
        span = BROAD_LABELS.get(data["label"])
        if not span:
            print(f"Skipping unknown broad label: {path.name}")
            return None
        return scene_payload(
            path,
            data["movie"],
            span["display"],
            "unknown",
            "broad",
            span["spans"],
        )

    match = FALLBACK_PATTERN.match(path.name)
    if match:
        data = match.groupdict()
        return scene_payload(
            path,
            data["movie"],
            "Fallback",
            "unknown",
            "fallback",
            spans_for("00-00", "unknown", "fallback"),
        )

    print(f"Skipping unrecognized filename: {path.name}")
    return None


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    scenes = []
    for path in sorted(SCENES_DIR.glob("*.mp4")):
        if path.name.startswith("._"):
            continue
        scene = parse_scene(path)
        if scene:
            scenes.append(scene)
    payload = {
        "schemaVersion": 1,
        "generatedFrom": "movie-scenes filenames",
        "scenes": scenes,
    }
    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    OUT.write_text(json_text + "\n")
    JS_OUT.write_text("window.REEL_TIME_SCENES = " + json_text + ";\n")
    print(f"Wrote {OUT} and {JS_OUT} with {len(scenes)} scenes")

if __name__ == "__main__":
    main()
