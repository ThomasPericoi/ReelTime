#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT / "assets" / "movie-scenes"
DATA_DIR = ROOT / "assets" / "data"
OUT = DATA_DIR / "scenes.json"
JS_OUT = DATA_DIR / "scenes-data.js"

MOVIE_META = {
    "12-angry-men": {"title": '12 Angry Men', "year": 1957, "director": 'Sidney Lumet', "rightsHolder": 'Orion-Nova Productions / MGM'},
    "12-monkeys": {"title": '12 Monkeys', "year": 1995, "director": 'Terry Gilliam', "rightsHolder": 'Universal Pictures'},
    "127-hours": {"title": '127 Hours', "year": 2010, "director": 'Danny Boyle', "rightsHolder": 'Searchlight Pictures / Pathé'},
    "3-10-to-yuma": {"title": '3:10 to Yuma', "year": 2007, "director": 'James Mangold', "rightsHolder": 'Lionsgate'},
    "a-beautiful-mind": {"title": 'A Beautiful Mind', "year": 2001, "director": 'Ron Howard', "rightsHolder": 'Universal Pictures / DreamWorks Pictures'},
    "a-christmas-story": {"title": 'A Christmas Story', "year": 1983, "director": 'Bob Clark', "rightsHolder": 'MGM / Warner Bros. Pictures'},
    "a-clockwork-orange": {"title": 'A Clockwork Orange', "year": 1971, "director": 'Stanley Kubrick', "rightsHolder": 'Warner Bros. Pictures'},
    "a-fish-called-wanda": {"title": 'A Fish Called Wanda', "year": 1988, "director": 'Charles Crichton', "rightsHolder": 'MGM'},
    "a-nightmare-on-elm-street": {"title": 'A Nightmare on Elm Street', "year": 1984, "director": 'Wes Craven', "rightsHolder": 'New Line Cinema / Warner Bros. Discovery'},
    "a-serious-man": {"title": 'A Serious Man', "year": 2009, "director": 'Joel Coen and Ethan Coen', "rightsHolder": 'Focus Features / Universal Pictures'},
    "all-the-presidents-men": {"title": "All the President's Men", "year": 1976, "director": 'Alan J. Pakula', "rightsHolder": 'Warner Bros. Pictures'},
    "american-gangster": {"title": 'American Gangster', "year": 2007, "director": 'Ridley Scott', "rightsHolder": 'Universal Pictures'},
    "american-hustle": {"title": 'American Hustle', "year": 2013, "director": 'David O. Russell', "rightsHolder": 'Sony Pictures'},
    "american-made": {"title": 'American Made', "year": 2017, "director": 'Doug Liman', "rightsHolder": 'Universal Pictures'},
    "american-psycho": {"title": 'American Psycho', "year": 2000, "director": 'Mary Harron', "rightsHolder": 'Lionsgate'},
    "anora": {"title": 'Anora', "year": 2024, "director": 'Sean Baker', "rightsHolder": 'Neon'},
    "antichrist": {"title": 'Antichrist', "year": 2009, "director": 'Lars von Trier', "rightsHolder": 'IFC Films / Zentropa'},
    "apocalypse-now": {"title": 'Apocalypse Now', "year": 1979, "director": 'Francis Ford Coppola', "rightsHolder": 'United Artists / Lionsgate'},
    "asteroid-city": {"title": 'Asteroid City', "year": 2023, "director": 'Wes Anderson', "rightsHolder": 'Focus Features / Universal Pictures'},
    "back-to-the-future": {"title": 'Back to the Future', "year": 1985, "director": 'Robert Zemeckis', "rightsHolder": 'Universal Pictures'},
    "back-to-the-future-part-3": {"title": 'Back to the Future Part III', "year": 1990, "director": 'Robert Zemeckis', "rightsHolder": 'Universal Pictures'},
    "basic-instinct": {"title": 'Basic Instinct', "year": 1992, "director": 'Paul Verhoeven', "rightsHolder": 'StudioCanal / Lionsgate'},
    "batman-returns": {"title": 'Batman Returns', "year": 1992, "director": 'Tim Burton', "rightsHolder": 'Warner Bros. Pictures'},
    "beau-is-afraid": {"title": 'Beau Is Afraid', "year": 2023, "director": 'Ari Aster', "rightsHolder": 'A24'},
    "beetlejuice": {"title": 'Beetlejuice', "year": 1988, "director": 'Tim Burton', "rightsHolder": 'Warner Bros. Pictures'},
    "before-sunrise": {"title": 'Before Sunrise', "year": 1995, "director": 'Richard Linklater', "rightsHolder": 'Columbia Pictures'},
    "being-john-malkovich": {"title": 'Being John Malkovich', "year": 1999, "director": 'Spike Jonze', "rightsHolder": 'USA Films / Universal Pictures'},
    "belfast": {"title": 'Belfast', "year": 2021, "director": 'Kenneth Branagh', "rightsHolder": 'Focus Features / Universal Pictures'},
    "big-fish": {"title": 'Big Fish', "year": 2003, "director": 'Tim Burton', "rightsHolder": 'Columbia Pictures / Sony Pictures'},
    "black-hawk-down": {"title": 'Black Hawk Down', "year": 2001, "director": 'Ridley Scott', "rightsHolder": 'Sony Pictures'},
    "blue-velvet": {"title": 'Blue Velvet', "year": 1986, "director": 'David Lynch', "rightsHolder": 'MGM / De Laurentiis Entertainment Group'},
    "bone-tomahawk": {"title": 'Bone Tomahawk', "year": 2015, "director": 'S. Craig Zahler', "rightsHolder": 'RLJ Entertainment'},
    "bugonia": {"title": 'Bugonia', "year": 2025, "director": 'Yorgos Lanthimos', "rightsHolder": 'Focus Features / Universal Pictures'},
    "burn-after-reading": {"title": 'Burn After Reading', "year": 2008, "director": 'Joel Coen and Ethan Coen', "rightsHolder": 'Focus Features / Universal Pictures'},
    "captain-fantastic": {"title": 'Captain Fantastic', "year": 2016, "director": 'Matt Ross', "rightsHolder": 'Bleecker Street'},
    "carrie": {"title": 'Carrie', "year": 1976, "director": 'Brian De Palma', "rightsHolder": 'United Artists / MGM'},
    "cast-away": {"title": 'Cast Away', "year": 2000, "director": 'Robert Zemeckis', "rightsHolder": '20th Century Studios / DreamWorks Pictures'},
    "chef": {"title": 'Chef', "year": 2014, "director": 'Jon Favreau', "rightsHolder": 'Open Road Films'},
    "citizen-kane": {"title": 'Citizen Kane', "year": 1941, "director": 'Orson Welles', "rightsHolder": 'Warner Bros. Discovery'},
    "civil-war": {"title": 'Civil War', "year": 2024, "director": 'Alex Garland', "rightsHolder": 'A24'},
    "clueless": {"title": 'Clueless', "year": 1995, "director": 'Amy Heckerling', "rightsHolder": 'Paramount Pictures'},
    "darkest-hour": {"title": 'Darkest Hour', "year": 2017, "director": 'Joe Wright', "rightsHolder": 'Focus Features / Universal Pictures'},
    "dawn-of-the-dead": {"title": 'Dawn of the Dead', "year": 1978, "director": 'George A. Romero', "rightsHolder": 'United Film Distribution Company / Anchor Bay Entertainment'},
    "demolition": {"title": 'Demolition', "year": 2015, "director": 'Jean-Marc Vallée', "rightsHolder": 'Fox Searchlight Pictures'},
    "die-hard-2": {"title": 'Die Hard 2', "year": 1990, "director": 'Renny Harlin', "rightsHolder": '20th Century Studios'},
    "donnie-darko": {"title": 'Donnie Darko', "year": 2001, "director": 'Richard Kelly', "rightsHolder": 'Arrow Films / Newmarket Films'},
    "dr-strangelove": {"title": 'Dr. Strangelove', "year": 1964, "director": 'Stanley Kubrick', "rightsHolder": 'Sony Pictures / Columbia Pictures'},
    "ed-wood": {"title": 'Ed Wood', "year": 1994, "director": 'Tim Burton', "rightsHolder": 'Touchstone Pictures / Disney'},
    "escape-from-new-york": {"title": 'Escape From New York', "year": 1981, "director": 'John Carpenter', "rightsHolder": 'StudioCanal / AVCO Embassy'},
    "eternal-sunshine-of-the-spotless-mind": {"title": 'Eternal Sunshine of the Spotless Mind', "year": 2004, "director": 'Michel Gondry', "rightsHolder": 'Focus Features / Universal Pictures'},
    "evil-dead-2": {"title": 'Evil Dead II', "year": 1987, "director": 'Sam Raimi', "rightsHolder": 'StudioCanal / Rosebud Releasing'},
    "ex-machina": {"title": 'Ex Machina', "year": 2014, "director": 'Alex Garland', "rightsHolder": 'A24 / Universal Pictures'},
    "eyes-wide-shut": {"title": 'Eyes Wide Shut', "year": 1999, "director": 'Stanley Kubrick', "rightsHolder": 'Warner Bros. Pictures'},
    "fantastic-mister-fox": {"title": 'Fantastic Mr. Fox', "year": 2009, "director": 'Wes Anderson', "rightsHolder": '20th Century Studios'},
    "fargo": {"title": 'Fargo', "year": 1996, "director": 'Joel Coen', "rightsHolder": 'Gramercy Pictures / MGM'},
    "fifth-element": {"title": 'The Fifth Element', "year": 1997, "director": 'Luc Besson', "rightsHolder": 'Gaumont / Sony Pictures'},
    "ford-v-ferrari": {"title": 'Ford v Ferrari', "year": 2019, "director": 'James Mangold', "rightsHolder": '20th Century Studios'},
    "four-lions": {"title": 'Four Lions', "year": 2010, "director": 'Chris Morris', "rightsHolder": 'Film4 / StudioCanal'},
    "foxcatcher": {"title": 'Foxcatcher', "year": 2014, "director": 'Bennett Miller', "rightsHolder": 'Sony Pictures Classics'},
    "from-dusk-till-dawn": {"title": 'From Dusk Till Dawn', "year": 1996, "director": 'Robert Rodriguez', "rightsHolder": 'Miramax / Dimension Films'},
    "fury": {"title": 'Fury', "year": 2014, "director": 'David Ayer', "rightsHolder": 'Sony Pictures'},
    "ghostbusters": {"title": 'Ghostbusters', "year": 1984, "director": 'Ivan Reitman', "rightsHolder": 'Columbia Pictures / Sony Pictures'},
    "good-morning-vietnam": {"title": 'Good Morning Vietnam', "year": 1987, "director": 'Barry Levinson', "rightsHolder": 'Touchstone Pictures / Disney'},
    "good-time": {"title": 'Good Time', "year": 2017, "director": 'Josh Safdie and Benny Safdie', "rightsHolder": 'A24'},
    "good-will-hunting": {"title": 'Good Will Hunting', "year": 1997, "director": 'Gus Van Sant', "rightsHolder": 'Miramax'},
    "goodfellas": {"title": 'Goodfellas', "year": 1990, "director": 'Martin Scorsese', "rightsHolder": 'Warner Bros. Pictures'},
    "green-book": {"title": 'Green Book', "year": 2018, "director": 'Peter Farrelly', "rightsHolder": 'Universal Pictures / Participant'},
    "gremlins": {"title": 'Gremlins', "year": 1984, "director": 'Joe Dante', "rightsHolder": 'Warner Bros. Pictures'},
    "i-saw-the-tv-glow": {"title": 'I Saw the TV Glow', "year": 2024, "director": 'Jane Schoenbrun', "rightsHolder": 'A24'},
    "in-the-loop": {"title": 'In the Loop', "year": 2009, "director": 'Armando Iannucci', "rightsHolder": 'IFC Films / BBC Films'},
    "in-the-name-of-the-father": {"title": 'In the Name of the Father', "year": 1993, "director": 'Jim Sheridan', "rightsHolder": 'Universal Pictures'},
    "indiana-jones-3": {"title": 'Indiana Jones and the Last Crusade', "year": 1989, "director": 'Steven Spielberg', "rightsHolder": 'Lucasfilm / Paramount Pictures'},
    "insidious": {"title": 'Insidious', "year": 2010, "director": 'James Wan', "rightsHolder": 'FilmDistrict / Sony Pictures'},
    "insomnia": {"title": 'Insomnia', "year": 2002, "director": 'Christopher Nolan', "rightsHolder": 'Warner Bros. Pictures'},
    "into-the-wild": {"title": 'Into the Wild', "year": 2007, "director": 'Sean Penn', "rightsHolder": 'Paramount Vantage'},
    "jacob-s-ladder": {"title": "Jacob's Ladder", "year": 1990, "director": 'Adrian Lyne', "rightsHolder": 'TriStar Pictures / StudioCanal'},
    "jaws": {"title": 'Jaws', "year": 1975, "director": 'Steven Spielberg', "rightsHolder": 'Universal Pictures'},
    "labyrinth": {"title": 'Labyrinth', "year": 1986, "director": 'Jim Henson', "rightsHolder": 'TriStar Pictures / The Jim Henson Company'},
    "late-night-with-the-devil": {"title": 'Late Night with the Devil', "year": 2023, "director": 'Cameron Cairnes and Colin Cairnes', "rightsHolder": 'IFC Films / Shudder'},
    "little-miss-sunshine": {"title": 'Little Miss Sunshine', "year": 2006, "director": 'Jonathan Dayton and Valerie Faris', "rightsHolder": 'Searchlight Pictures'},
    "lord-of-the-rings-3": {"title": 'The Lord of the Rings: The Return of the King', "year": 2003, "director": 'Peter Jackson', "rightsHolder": 'New Line Cinema / Warner Bros. Pictures'},
    "lost-in-translation": {"title": 'Lost In Translation', "year": 2003, "director": 'Sofia Coppola', "rightsHolder": 'Focus Features / Universal Pictures'},
    "lucky-number-slevin": {"title": 'Lucky Number Slevin', "year": 2006, "director": 'Paul McGuigan', "rightsHolder": 'The Weinstein Company / MGM'},
    "manchester-by-the-sea": {"title": 'Manchester By the Sea', "year": 2016, "director": 'Kenneth Lonergan', "rightsHolder": 'Amazon Studios / Roadside Attractions'},
    "marty-supreme": {"title": 'Marty Supreme', "year": 2025, "director": 'Josh Safdie', "rightsHolder": 'A24'},
    "master-and-commander": {"title": 'Master and Commander', "year": 2003, "director": 'Peter Weir', "rightsHolder": '20th Century Studios'},
    "mean-girls": {"title": 'Mean Girls', "year": 2004, "director": 'Mark Waters', "rightsHolder": 'Paramount Pictures'},
    "memento": {"title": 'Memento', "year": 2000, "director": 'Christopher Nolan', "rightsHolder": 'Summit Entertainment'},
    "mickey-17": {"title": 'Mickey 17', "year": 2025, "director": 'Bong Joon Ho', "rightsHolder": 'Warner Bros. Pictures'},
    "mid90s": {"title": 'Mid90s', "year": 2018, "director": 'Jonah Hill', "rightsHolder": 'A24'},
    "midsommar": {"title": 'Midsommar', "year": 2019, "director": 'Ari Aster', "rightsHolder": 'A24'},
    "moonrise-kingdom": {"title": 'Moonrise Kingdom', "year": 2012, "director": 'Wes Anderson', "rightsHolder": 'Focus Features / Universal Pictures'},
    "mulholland-drive": {"title": 'Mulholland Drive', "year": 2001, "director": 'David Lynch', "rightsHolder": 'Universal Pictures / StudioCanal'},
    "munich": {"title": 'Munich', "year": 2005, "director": 'Steven Spielberg', "rightsHolder": 'Universal Pictures / DreamWorks Pictures'},
    "neon-demon": {"title": 'The Neon Demon', "year": 2016, "director": 'Nicolas Winding Refn', "rightsHolder": 'Amazon Studios / Broad Green Pictures'},
    "nightcrawler": {"title": 'Nightcrawler', "year": 2014, "director": 'Dan Gilroy', "rightsHolder": 'Open Road Films'},
    "no-country-for-old-men": {"title": 'No Country for Old Men', "year": 2007, "director": 'Joel Coen and Ethan Coen', "rightsHolder": 'Miramax / Paramount Vantage'},
    "nocturnal-animals": {"title": 'Nocturnal Animals', "year": 2016, "director": 'Tom Ford', "rightsHolder": 'Focus Features / Universal Pictures'},
    "nosferatu": {"title": 'Nosferatu', "year": 2024, "director": 'Robert Eggers', "rightsHolder": 'Focus Features / Universal Pictures'},
    "novocaine": {"title": 'Novocaine', "year": 2025, "director": 'Dan Berk and Robert Olsen', "rightsHolder": 'Paramount Pictures'},
    "ocean-s-eleven": {"title": "Ocean's Eleven", "year": 2001, "director": 'Steven Soderbergh', "rightsHolder": 'Warner Bros. Pictures'},
    "once-upon-a-time-in-america": {"title": 'Once Upon a Time in America', "year": 1984, "director": 'Sergio Leone', "rightsHolder": 'Warner Bros. Pictures'},
    "once-upon-a-time-in-hollywood": {"title": 'Once Upon a Time in Hollywood', "year": 2019, "director": 'Quentin Tarantino', "rightsHolder": 'Sony Pictures'},
    "paddington": {"title": 'Paddington', "year": 2014, "director": 'Paul King', "rightsHolder": 'StudioCanal'},
    "paris-texas": {"title": 'Paris, Texas', "year": 1984, "director": 'Wim Wenders', "rightsHolder": '20th Century Studios / Janus Films'},
    "pig": {"title": 'Pig', "year": 2021, "director": 'Michael Sarnoski', "rightsHolder": 'Neon'},
    "point-break": {"title": 'Point Break', "year": 1991, "director": 'Kathryn Bigelow', "rightsHolder": '20th Century Studios'},
    "poor-things": {"title": 'Poor Things', "year": 2023, "director": 'Yorgos Lanthimos', "rightsHolder": 'Searchlight Pictures'},
    "pulp-fiction": {"title": 'Pulp Fiction', "year": 1994, "director": 'Quentin Tarantino', "rightsHolder": 'Miramax'},
    "rainman": {"title": 'Rain Man', "year": 1988, "director": 'Barry Levinson', "rightsHolder": 'MGM / United Artists'},
    "rear-window": {"title": 'Rear Window', "year": 1954, "director": 'Alfred Hitchcock', "rightsHolder": 'Universal Pictures'},
    "rocky": {"title": 'Rocky', "year": 1976, "director": 'John G. Avildsen', "rightsHolder": 'MGM / United Artists'},
    "sandlot": {"title": 'The Sandlot', "year": 1993, "director": 'David Mickey Evans', "rightsHolder": '20th Century Studios'},
    "scarface": {"title": 'Scarface', "year": 1983, "director": 'Brian De Palma', "rightsHolder": 'Universal Pictures'},
    "scott-pilgrim-vs-the-world": {"title": 'Scott Pilgrim vs. the World', "year": 2010, "director": 'Edgar Wright', "rightsHolder": 'Universal Pictures'},
    "shaun-of-the-dead": {"title": 'Shaun of the Dead', "year": 2004, "director": 'Edgar Wright', "rightsHolder": 'Universal Pictures / StudioCanal'},
    "shawshank-redemption": {"title": 'Shawshank Redemption', "year": 1994, "director": 'Frank Darabont', "rightsHolder": 'Warner Bros. Pictures'},
    "sicario": {"title": 'Sicario', "year": 2015, "director": 'Denis Villeneuve', "rightsHolder": 'Lionsgate'},
    "sing-sing": {"title": 'Sing Sing', "year": 2023, "director": 'Greg Kwedar', "rightsHolder": 'A24'},
    "snowden": {"title": 'Snowden', "year": 2016, "director": 'Oliver Stone', "rightsHolder": 'Open Road Films'},
    "some-like-it-hot": {"title": 'Some Like It Hot', "year": 1959, "director": 'Billy Wilder', "rightsHolder": 'United Artists / MGM'},
    "spotlight": {"title": 'Spotlight', "year": 2015, "director": 'Tom McCarthy', "rightsHolder": 'Open Road Films / Participant'},
    "stand-by-me": {"title": 'Stand By Me', "year": 1986, "director": 'Rob Reiner', "rightsHolder": 'Columbia Pictures'},
    "sunset-boulevard": {"title": 'Sunset Boulevard', "year": 1950, "director": 'Billy Wilder', "rightsHolder": 'Paramount Pictures'},
    "taxi-driver": {"title": 'Taxi Driver', "year": 1976, "director": 'Martin Scorsese', "rightsHolder": 'Columbia Pictures / Sony Pictures'},
    "terminator": {"title": 'The Terminator', "year": 1984, "director": 'James Cameron', "rightsHolder": 'MGM / Orion Pictures'},
    "the-age-of-innocence": {"title": 'The Age of Innocence', "year": 1993, "director": 'Martin Scorsese', "rightsHolder": 'Columbia Pictures'},
    "the-aviator": {"title": 'The Aviator', "year": 2004, "director": 'Martin Scorsese', "rightsHolder": 'Miramax / Warner Bros. Pictures'},
    "the-babadook": {"title": 'The Babadook', "year": 2014, "director": 'Jennifer Kent', "rightsHolder": 'IFC Films / Umbrella Entertainment'},
    "the-banshees-of-inisherin": {"title": 'The Banshees of Inisherin', "year": 2022, "director": 'Martin McDonagh', "rightsHolder": 'Searchlight Pictures'},
    "the-blues-brothers": {"title": 'The Blues Brothers', "year": 1980, "director": 'John Landis', "rightsHolder": 'Universal Pictures'},
    "the-breakfast-club": {"title": 'The Breakfast Club', "year": 1985, "director": 'John Hughes', "rightsHolder": 'Universal Pictures'},
    "the-conjuring": {"title": 'The Conjuring', "year": 2013, "director": 'James Wan', "rightsHolder": 'Warner Bros. Pictures / New Line Cinema'},
    "the-conversation": {"title": 'The Conversation', "year": 1974, "director": 'Francis Ford Coppola', "rightsHolder": 'Paramount Pictures'},
    "the-departed": {"title": 'The Departed', "year": 2006, "director": 'Martin Scorsese', "rightsHolder": 'Warner Bros. Pictures'},
    "the-elephant-man": {"title": 'The Elephant Man', "year": 1980, "director": 'David Lynch', "rightsHolder": 'Paramount Pictures / StudioCanal'},
    "the-farewell": {"title": 'The Farewell', "year": 2019, "director": 'Lulu Wang', "rightsHolder": 'A24'},
    "the-father": {"title": 'The Father', "year": 2020, "director": 'Florian Zeller', "rightsHolder": 'Sony Pictures Classics'},
    "the-florida-project": {"title": 'The Florida Project', "year": 2017, "director": 'Sean Baker', "rightsHolder": 'A24'},
    "the-game": {"title": 'The Game', "year": 1997, "director": 'David Fincher', "rightsHolder": 'PolyGram Filmed Entertainment / Universal Pictures'},
    "the-green-mile": {"title": 'The Green Mile', "year": 1999, "director": 'Frank Darabont', "rightsHolder": 'Warner Bros. Pictures'},
    "the-lobster": {"title": 'The Lobster', "year": 2015, "director": 'Yorgos Lanthimos', "rightsHolder": 'A24 / Film4'},
    "the-man-who-fell-to-earth": {"title": 'The Man Who Fell to Earth', "year": 1976, "director": 'Nicolas Roeg', "rightsHolder": 'StudioCanal'},
    "the-martian": {"title": 'The Martian', "year": 2015, "director": 'Ridley Scott', "rightsHolder": '20th Century Studios'},
    "the-master": {"title": 'The Master', "year": 2012, "director": 'Paul Thomas Anderson', "rightsHolder": 'The Weinstein Company'},
    "the-notebook": {"title": 'The Notebook', "year": 2004, "director": 'Nick Cassavetes', "rightsHolder": 'New Line Cinema / Warner Bros. Pictures'},
    "the-road": {"title": 'The Road', "year": 2009, "director": 'John Hillcoat', "rightsHolder": 'Dimension Films'},
    "the-shining": {"title": 'The Shining', "year": 1980, "director": 'Stanley Kubrick', "rightsHolder": 'Warner Bros. Pictures'},
    "the-social-network": {"title": 'The Social Network', "year": 2010, "director": 'David Fincher', "rightsHolder": 'Columbia Pictures / Sony Pictures'},
    "the-sting": {"title": 'The Sting', "year": 1973, "director": 'George Roy Hill', "rightsHolder": 'Universal Pictures'},
    "the-strange-case-of-benjamin-button": {"title": 'The Curious Case of Benjamin Button', "year": 2008, "director": 'David Fincher', "rightsHolder": 'Paramount Pictures / Warner Bros. Pictures'},
    "the-thin-red-line": {"title": 'The Thin Red Line', "year": 1998, "director": 'Terrence Malick', "rightsHolder": '20th Century Studios'},
    "the-usual-suspects": {"title": 'The Usual Suspects', "year": 1995, "director": 'Bryan Singer', "rightsHolder": 'MGM / Gramercy Pictures'},
    "the-worlds-end": {"title": "The World's End", "year": 2013, "director": 'Edgar Wright', "rightsHolder": 'Universal Pictures / Focus Features'},
    "thelma-and-louise": {"title": 'Thelma & Louise', "year": 1991, "director": 'Ridley Scott', "rightsHolder": 'MGM'},
    "tower": {"title": 'Tower', "year": 2016, "director": 'Keith Maitland', "rightsHolder": 'Kino Lorber'},
    "trainspotting-2": {"title": 'T2 Trainspotting', "year": 2017, "director": 'Danny Boyle', "rightsHolder": 'Sony Pictures'},
    "trick-r-treat": {"title": "Trick 'r Treat", "year": 2007, "director": 'Michael Dougherty', "rightsHolder": 'Warner Bros. Pictures / Legendary Pictures'},
    "true-grit": {"title": 'True Grit', "year": 2010, "director": 'Joel Coen and Ethan Coen', "rightsHolder": 'Paramount Pictures'},
    "true-lies": {"title": 'True Lies', "year": 1994, "director": 'James Cameron', "rightsHolder": '20th Century Studios'},
    "under-the-skin": {"title": 'Under the Skin', "year": 2013, "director": 'Jonathan Glazer', "rightsHolder": 'A24 / StudioCanal'},
    "us": {"title": 'Us', "year": 2019, "director": 'Jordan Peele', "rightsHolder": 'Universal Pictures'},
    "wall-e": {"title": 'WALL-E', "year": 2008, "director": 'Andrew Stanton', "rightsHolder": 'Pixar / Walt Disney Pictures'},
    "watchmen": {"title": 'Watchmen', "year": 2009, "director": 'Zack Snyder', "rightsHolder": 'Warner Bros. Pictures / Paramount Pictures'},
    "weapons": {"title": 'Weapons', "year": 2025, "director": 'Zach Cregger', "rightsHolder": 'Warner Bros. Pictures'},
    "what-we-do-in-the-shadows": {"title": 'What We Do in the Shadows', "year": 2014, "director": 'Jemaine Clement and Taika Waititi', "rightsHolder": 'The Orchard / Paramount Pictures'},
    "when-harry-met-sally": {"title": 'When Harry Met Sally...', "year": 1989, "director": 'Rob Reiner', "rightsHolder": 'Castle Rock Entertainment / MGM'},
    "wonder-boys": {"title": 'Wonder Boys', "year": 2000, "director": 'Curtis Hanson', "rightsHolder": 'Paramount Pictures'},
    "you-can-count-on-me": {"title": 'You Can Count on Me', "year": 2000, "director": 'Kenneth Lonergan', "rightsHolder": 'Paramount Classics'},
    "zero-dark-thirty": {"title": 'Zero Dark Thirty', "year": 2012, "director": 'Kathryn Bigelow', "rightsHolder": 'Sony Pictures'},
    "zodiac": {"title": 'Zodiac', "year": 2007, "director": 'David Fincher', "rightsHolder": 'Paramount Pictures / Warner Bros. Pictures'},
}

PATTERN = re.compile(r"^(?P<hhmm>\d{2}-\d{2})_(?P<period>am|pm|both|unknown)_(?P<precision>[^_]+)_(?P<movie>.+)_(?P<index>\d+)\.mp4$")
BROAD_PATTERN = re.compile(r"^(?P<label>[a-z0-9-]+)_broad_(?P<movie>.+)_(?P<index>\d+)\.mp4$")
FALLBACK_PATTERN = re.compile(r"^fallback_(?P<movie>.+)_(?P<index>\d+)\.mp4$")

SPAN_LABELS = {
    "dawn": {"display": "Dawn", "spans": [{"start": "04:50", "end": "06:50"}]},
    "dusk": {"display": "Dusk", "spans": [{"start": "18:00", "end": "20:10"}]},
    "early-morning": {"display": "Early morning", "spans": [{"start": "05:00", "end": "07:30"}]},
    "evening": {"display": "Evening", "spans": [{"start": "19:00", "end": "22:00"}]},
    "midday": {"display": "Midday", "spans": [{"start": "11:30", "end": "12:45"}]},
    "middle-night": {"display": "Middle of the night", "spans": [{"start": "00:30", "end": "04:00"}]},
    "morning": {"display": "Morning", "spans": [{"start": "07:00", "end": "11:30"}]},
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
            start, end = center - 5, center
        elif precision == "after":
            start, end = center, center + 5
        elif precision == "approx":
            start, end = center - 5, center + 5
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
        "src": f"assets/movie-scenes/{path.name}",
        "movieTitle": titleize(movie),
        "movieSlug": movie,
        "releaseYear": metadata.get("year"),
        "director": metadata.get("director", "Director to verify"),
        "rightsHolder": metadata.get("rightsHolder", "Rights holder to verify"),
        "displayTime": display_time,
        "period": period,
        "precision": precision,
        "priority": priority_for(precision),
        "spans": spans,
    }

def parse_scene(path):
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
        span = SPAN_LABELS.get(data["label"])
        if not span:
            print(f"Skipping unknown span label: {path.name}")
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
