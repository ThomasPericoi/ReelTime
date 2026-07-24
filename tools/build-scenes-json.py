#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT / "assets" / "movie-scenes"
DATA_DIR = ROOT / "assets" / "data"
OUT = DATA_DIR / "scenes.json"
JS_OUT = DATA_DIR / "scenes-data.js"

RIGHTS = {
    "a-clockwork-orange": "Warner Bros. Pictures",
    "a-fish-called-wanda": "MGM",
    "a-serious-man": "Focus Features / Universal Pictures",
    "all-the-presidents-men": "Warner Bros. Pictures",
    "american-hustle": "Sony Pictures",
    "american-made": "Universal Pictures",
    "back-to-the-future-part-3": "Universal Pictures",
    "before-sunrise": "Columbia Pictures",
    "blue-velvet": "MGM / De Laurentiis Entertainment Group",
    "burn-after-reading": "Focus Features / Universal Pictures",
    "captain-fantastic": "Bleecker Street",
    "carrie": "United Artists / MGM",
    "chef": "Open Road Films",
    "clueless": "Paramount Pictures",
    "dawn-of-the-dead": "United Film Distribution Company / Anchor Bay Entertainment",
    "demolition": "Fox Searchlight Pictures",
    "ed-wood": "Touchstone Pictures / Disney",
    "ex-machina": "A24 / Universal Pictures",
    "fargo": "Gramercy Pictures / MGM",
    "foxcatcher": "Sony Pictures Classics",
    "fury": "Sony Pictures",
    "goodfellas": "Warner Bros. Pictures",
    "green-book": "Universal Pictures / Participant",
    "insidious": "FilmDistrict / Sony Pictures",
    "lost-in-translation": "Focus Features / Universal Pictures",
    "manchester-by-the-sea": "Amazon Studios / Roadside Attractions",
    "mid90s": "A24",
    "midsommar": "A24",
    "mulholland-drive": "Universal Pictures / StudioCanal",
    "munich": "Universal Pictures / DreamWorks Pictures",
    "nightcrawler": "Open Road Films",
    "once-upon-a-time-in-hollywood": "Sony Pictures",
    "paris-texas": "20th Century Studios / Janus Films",
    "rainman": "MGM / United Artists",
    "rear-window": "Universal Pictures",
    "scarface": "Universal Pictures",
    "scott-pilgrim-vs-the-world": "Universal Pictures",
    "some-like-it-hot": "United Artists / MGM",
    "stand-by-me": "Columbia Pictures",
    "sunset-boulevard": "Paramount Pictures",
    "12-angry-men": "Orion-Nova Productions / MGM",
    "12-monkeys": "Universal Pictures",
    "127-hours": "Searchlight Pictures / Pathé",
    "a-beautiful-mind": "Universal Pictures / DreamWorks Pictures",
    "a-nightmare-on-elm-street": "New Line Cinema / Warner Bros. Discovery",
    "american-gangster": "Universal Pictures",
    "american-psycho": "Lionsgate",
    "apocalypse-now": "United Artists / Lionsgate",
    "basic-instinct": "StudioCanal / Lionsgate",
    "batman-returns": "Warner Bros. Pictures",
    "belfast": "Focus Features / Universal Pictures",
    "black-hawk-down": "Sony Pictures",
    "bone-tomahawk": "RLJ Entertainment",
    "cast-away": "20th Century Studios / DreamWorks Pictures",
    "citizen-kane": "Warner Bros. Discovery",
    "die-hard-2": "20th Century Studios",
    "donnie-darko": "Arrow Films / Newmarket Films",
    "dr-strangelove": "Sony Pictures / Columbia Pictures",
    "escape-from-new-york": "StudioCanal / AVCO Embassy",
    "eternal-sunshine-of-the-spotless-mind": "Focus Features / Universal Pictures",
    "evil-dead-2": "StudioCanal / Rosebud Releasing",
    "fantastic-mister-fox": "20th Century Studios",
    "ford-v-ferrari": "20th Century Studios",
    "good-morning-vietnam": "Touchstone Pictures / Disney",
    "good-will-hunting": "Miramax",
    "gremlins": "Warner Bros. Pictures",
    "in-the-loop": "IFC Films / BBC Films",
    "indiana-jones-3": "Lucasfilm / Paramount Pictures",
    "insomnia": "Warner Bros. Pictures",
    "jaws": "Universal Pictures",
    "little-miss-sunshine": "Searchlight Pictures",
    "lucky-number-slevin": "The Weinstein Company / MGM",
    "master-and-commander": "20th Century Studios",
    "mean-girls": "Paramount Pictures",
    "memento": "Summit Entertainment",
    "moonrise-kingdom": "Focus Features / Universal Pictures",
    "no-country-for-old-men": "Miramax / Paramount Vantage",
    "pig": "Neon",
    "pulp-fiction": "Miramax",
    "rocky": "MGM / United Artists",
    "shawshank-redemption": "Warner Bros. Pictures",
    "sicario": "Lionsgate",
    "spotlight": "Open Road Films / Participant",
    "terminator": "MGM / Orion Pictures",
    "the-aviator": "Miramax / Warner Bros. Pictures",
    "the-banshees-of-inisherin": "Searchlight Pictures",
    "the-blues-brothers": "Universal Pictures",
    "the-departed": "Warner Bros. Pictures",
    "the-father": "Sony Pictures Classics",
    "the-game": "PolyGram Filmed Entertainment / Universal Pictures",
    "the-green-mile": "Warner Bros. Pictures",
    "the-master": "The Weinstein Company",
    "the-road": "Dimension Films",
    "the-thin-red-line": "20th Century Studios",
    "wall-e": "Pixar / Walt Disney Pictures",
    "watchmen": "Warner Bros. Pictures / Paramount Pictures",
    "zero-dark-thirty": "Sony Pictures",
}

MOVIE_META = {
    "a-clockwork-orange": {"year": 1971, "director": "Stanley Kubrick"},
    "a-fish-called-wanda": {"year": 1988, "director": "Charles Crichton"},
    "a-serious-man": {"year": 2009, "director": "Joel Coen and Ethan Coen"},
    "all-the-presidents-men": {"year": 1976, "director": "Alan J. Pakula"},
    "american-hustle": {"year": 2013, "director": "David O. Russell"},
    "american-made": {"year": 2017, "director": "Doug Liman"},
    "back-to-the-future-part-3": {"year": 1990, "director": "Robert Zemeckis"},
    "before-sunrise": {"year": 1995, "director": "Richard Linklater"},
    "blue-velvet": {"year": 1986, "director": "David Lynch"},
    "burn-after-reading": {"year": 2008, "director": "Joel Coen and Ethan Coen"},
    "captain-fantastic": {"year": 2016, "director": "Matt Ross"},
    "carrie": {"year": 1976, "director": "Brian De Palma"},
    "chef": {"year": 2014, "director": "Jon Favreau"},
    "clueless": {"year": 1995, "director": "Amy Heckerling"},
    "dawn-of-the-dead": {"year": 1978, "director": "George A. Romero"},
    "demolition": {"year": 2015, "director": "Jean-Marc Vallée"},
    "ed-wood": {"year": 1994, "director": "Tim Burton"},
    "ex-machina": {"year": 2014, "director": "Alex Garland"},
    "fargo": {"year": 1996, "director": "Joel Coen"},
    "foxcatcher": {"year": 2014, "director": "Bennett Miller"},
    "fury": {"year": 2014, "director": "David Ayer"},
    "goodfellas": {"year": 1990, "director": "Martin Scorsese"},
    "green-book": {"year": 2018, "director": "Peter Farrelly"},
    "insidious": {"year": 2010, "director": "James Wan"},
    "lost-in-translation": {"year": 2003, "director": "Sofia Coppola"},
    "manchester-by-the-sea": {"year": 2016, "director": "Kenneth Lonergan"},
    "mid90s": {"year": 2018, "director": "Jonah Hill"},
    "midsommar": {"year": 2019, "director": "Ari Aster"},
    "mulholland-drive": {"year": 2001, "director": "David Lynch"},
    "munich": {"year": 2005, "director": "Steven Spielberg"},
    "nightcrawler": {"year": 2014, "director": "Dan Gilroy"},
    "once-upon-a-time-in-hollywood": {"year": 2019, "director": "Quentin Tarantino"},
    "paris-texas": {"year": 1984, "director": "Wim Wenders"},
    "rainman": {"year": 1988, "director": "Barry Levinson"},
    "rear-window": {"year": 1954, "director": "Alfred Hitchcock"},
    "scarface": {"year": 1983, "director": "Brian De Palma"},
    "scott-pilgrim-vs-the-world": {"year": 2010, "director": "Edgar Wright"},
    "some-like-it-hot": {"year": 1959, "director": "Billy Wilder"},
    "stand-by-me": {"year": 1986, "director": "Rob Reiner"},
    "sunset-boulevard": {"year": 1950, "director": "Billy Wilder"},
    "12-angry-men": {"year": 1957, "director": "Sidney Lumet"},
    "12-monkeys": {"year": 1995, "director": "Terry Gilliam"},
    "127-hours": {"year": 2010, "director": "Danny Boyle"},
    "a-beautiful-mind": {"year": 2001, "director": "Ron Howard"},
    "a-nightmare-on-elm-street": {"year": 1984, "director": "Wes Craven"},
    "american-gangster": {"year": 2007, "director": "Ridley Scott"},
    "american-psycho": {"year": 2000, "director": "Mary Harron"},
    "apocalypse-now": {"year": 1979, "director": "Francis Ford Coppola"},
    "basic-instinct": {"year": 1992, "director": "Paul Verhoeven"},
    "batman-returns": {"year": 1992, "director": "Tim Burton"},
    "belfast": {"year": 2021, "director": "Kenneth Branagh"},
    "black-hawk-down": {"year": 2001, "director": "Ridley Scott"},
    "bone-tomahawk": {"year": 2015, "director": "S. Craig Zahler"},
    "cast-away": {"year": 2000, "director": "Robert Zemeckis"},
    "citizen-kane": {"year": 1941, "director": "Orson Welles"},
    "die-hard-2": {"year": 1990, "director": "Renny Harlin"},
    "donnie-darko": {"year": 2001, "director": "Richard Kelly"},
    "dr-strangelove": {"year": 1964, "director": "Stanley Kubrick"},
    "escape-from-new-york": {"year": 1981, "director": "John Carpenter"},
    "eternal-sunshine-of-the-spotless-mind": {"year": 2004, "director": "Michel Gondry"},
    "evil-dead-2": {"year": 1987, "director": "Sam Raimi"},
    "fantastic-mister-fox": {"year": 2009, "director": "Wes Anderson"},
    "ford-v-ferrari": {"year": 2019, "director": "James Mangold"},
    "good-morning-vietnam": {"year": 1987, "director": "Barry Levinson"},
    "good-will-hunting": {"year": 1997, "director": "Gus Van Sant"},
    "gremlins": {"year": 1984, "director": "Joe Dante"},
    "in-the-loop": {"year": 2009, "director": "Armando Iannucci"},
    "indiana-jones-3": {"year": 1989, "director": "Steven Spielberg"},
    "insomnia": {"year": 2002, "director": "Christopher Nolan"},
    "jaws": {"year": 1975, "director": "Steven Spielberg"},
    "little-miss-sunshine": {"year": 2006, "director": "Jonathan Dayton and Valerie Faris"},
    "lucky-number-slevin": {"year": 2006, "director": "Paul McGuigan"},
    "master-and-commander": {"year": 2003, "director": "Peter Weir"},
    "mean-girls": {"year": 2004, "director": "Mark Waters"},
    "memento": {"year": 2000, "director": "Christopher Nolan"},
    "moonrise-kingdom": {"year": 2012, "director": "Wes Anderson"},
    "no-country-for-old-men": {"year": 2007, "director": "Joel Coen and Ethan Coen"},
    "pig": {"year": 2021, "director": "Michael Sarnoski"},
    "pulp-fiction": {"year": 1994, "director": "Quentin Tarantino"},
    "rocky": {"year": 1976, "director": "John G. Avildsen"},
    "shawshank-redemption": {"year": 1994, "director": "Frank Darabont"},
    "sicario": {"year": 2015, "director": "Denis Villeneuve"},
    "spotlight": {"year": 2015, "director": "Tom McCarthy"},
    "terminator": {"year": 1984, "director": "James Cameron"},
    "the-aviator": {"year": 2004, "director": "Martin Scorsese"},
    "the-banshees-of-inisherin": {"year": 2022, "director": "Martin McDonagh"},
    "the-blues-brothers": {"year": 1980, "director": "John Landis"},
    "the-departed": {"year": 2006, "director": "Martin Scorsese"},
    "the-father": {"year": 2020, "director": "Florian Zeller"},
    "the-game": {"year": 1997, "director": "David Fincher"},
    "the-green-mile": {"year": 1999, "director": "Frank Darabont"},
    "the-master": {"year": 2012, "director": "Paul Thomas Anderson"},
    "the-road": {"year": 2009, "director": "John Hillcoat"},
    "the-thin-red-line": {"year": 1998, "director": "Terrence Malick"},
    "wall-e": {"year": 2008, "director": "Andrew Stanton"},
    "watchmen": {"year": 2009, "director": "Zack Snyder"},
    "zero-dark-thirty": {"year": 2012, "director": "Kathryn Bigelow"},
}

TITLE_FIXES = {
    "a-fish-called-wanda": "A Fish Called Wanda",
    "a-serious-man": "A Serious Man",
    "all-the-presidents-men": "All the President's Men",
    "back-to-the-future-part-3": "Back to the Future Part III",
    "mid90s": "Mid90s",
    "once-upon-a-time-in-hollywood": "Once Upon a Time in Hollywood",
    "paris-texas": "Paris, Texas",
    "rainman": "Rain Man",
    "scott-pilgrim-vs-the-world": "Scott Pilgrim vs. the World",
    "127-hours": "127 Hours",
    "12-angry-men": "12 Angry Men",
    "12-monkeys": "12 Monkeys",
    "a-nightmare-on-elm-street": "A Nightmare on Elm Street",
    "dr-strangelove": "Dr. Strangelove",
    "evil-dead-2": "Evil Dead II",
    "fantastic-mister-fox": "Fantastic Mr. Fox",
    "ford-v-ferrari": "Ford v Ferrari",
    "indiana-jones-3": "Indiana Jones and the Last Crusade",
    "terminator": "The Terminator",
    "wall-e": "WALL-E",
}

PATTERN = re.compile(r"^(?P<hhmm>\d{2}-\d{2})_(?P<period>am|pm|both|unknown)_(?P<precision>[^_]+)_(?P<movie>.+)_(?P<index>\d+)\.mp4$")


def titleize(slug):
    if slug in TITLE_FIXES:
        return TITLE_FIXES[slug]
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
            start, end = center - 7, center + 7
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


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    scenes = []
    for path in sorted(SCENES_DIR.glob("*.mp4")):
        if path.name.startswith("._"):
            continue
        match = PATTERN.match(path.name)
        if not match:
            print(f"Skipping unrecognized filename: {path.name}")
            continue
        data = match.groupdict()
        movie = data["movie"]
        metadata = MOVIE_META.get(movie, {})
        scenes.append({
            "id": path.stem,
            "src": f"assets/movie-scenes/{path.name}",
            "movieTitle": titleize(movie),
            "movieSlug": movie,
            "releaseYear": metadata.get("year"),
            "director": metadata.get("director", "Director to verify"),
            "rightsHolder": RIGHTS.get(movie, "Rights holder to verify"),
            "displayTime": data["hhmm"].replace("-", ":"),
            "period": data["period"],
            "precision": data["precision"],
            "priority": priority_for(data["precision"]),
            "spans": spans_for(data["hhmm"], data["period"], data["precision"]),
        })
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
