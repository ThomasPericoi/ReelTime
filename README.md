# Reel Time

**Reel Time** is a talking clock made from movie scenes. Open it, press play, and let a film scene tell you the local time.

Production URL: [reel-time.thomaspericoi.com](https://reel-time.thomaspericoi.com)

## What it does

- Selects a scene from the current local time.
- Uses a cascade on first launch: exact match first, then broader/approximate scenes if needed.
- After the arrival scene, only exact-time scenes are used.
- Plays a 3-second vintage countdown with audio beeps.
- Shows film title, release year, director, and rights holder before and during playback.
- Simulates a 1920s-style projection with grain, flicker, vignette, and a short image-catch offset when the scene appears.
- Runs as plain static files. No framework, no build step, no server required.

## Scene coverage

Current library stats, generated from `assets/data/scenes.json`:

- Total scenes: **153**
- Exact-time scenes: **136**
- Exact minutes covered: **107 / 1440**
- Exact-time coverage: **7.4%**

`Exact minutes covered` counts unique exact minutes only. Scenes marked `both` count toward both their AM and PM hours.

| Hour | Exact minutes covered | Exact scene entries | All scene entries |
| --- | ---: | ---: | ---: |
| 00:00-00:59 | 4 | 5 | 9 |
| 01:00-01:59 | 7 | 9 | 11 |
| 02:00-02:59 | 5 | 13 | 14 |
| 03:00-03:59 | 3 | 12 | 13 |
| 04:00-04:59 | 5 | 7 | 9 |
| 05:00-05:59 | 4 | 8 | 9 |
| 06:00-06:59 | 3 | 8 | 9 |
| 07:00-07:59 | 5 | 9 | 12 |
| 08:00-08:59 | 7 | 15 | 21 |
| 09:00-09:59 | 4 | 6 | 9 |
| 10:00-10:59 | 4 | 10 | 10 |
| 11:00-11:59 | 3 | 8 | 10 |
| 12:00-12:59 | 5 | 9 | 11 |
| 13:00-13:59 | 7 | 8 | 8 |
| 14:00-14:59 | 5 | 11 | 11 |
| 15:00-15:59 | 2 | 8 | 9 |
| 16:00-16:59 | 6 | 7 | 9 |
| 17:00-17:59 | 3 | 4 | 5 |
| 18:00-18:59 | 3 | 3 | 4 |
| 19:00-19:59 | 3 | 7 | 10 |
| 20:00-20:59 | 6 | 12 | 17 |
| 21:00-21:59 | 3 | 8 | 11 |
| 22:00-22:59 | 5 | 14 | 14 |
| 23:00-23:59 | 5 | 13 | 17 |

## Structure

```text
index.html
README.md
assets/
  css/
    styles.css
  js/
    app.js
  data/
    scenes-data.js
    scenes.json
  movie-scenes/   # local video files, ignored by git
  sounds/
    countdown_beep.mp3
    projector.mp3
tools/
  build-scenes-json.py
```

`assets/data/scenes-data.js` is used by the browser, including when opening `index.html` directly via `file://`. `assets/data/scenes.json` is kept as the readable data export. Video scenes are intentionally ignored by git.

## Local use

Open `index.html` directly in a browser.

## Rebuild scene data

When scenes are added, renamed, or removed:

```bash
python3 tools/build-scenes-json.py
```

The generator reads filenames from `assets/movie-scenes/` and writes both `assets/data/scenes.json` and `assets/data/scenes-data.js`.

## Filename convention

```text
HH-MM_period_precision_movie-slug_###.mp4
```

Examples:

```text
08-30_am_exact_ford-v-ferrari_001.mp4
12-00_both_approx_gremlins_001.mp4
08-00_both_before_lucky-number-slevin_001.mp4
```

## Debug API

Open the browser console after the page loads:

```js
ReelTime.scenes({ exactOnly: true })
ReelTime.scenes({ time: "08:30" })
ReelTime.find({ query: "pulp" })
ReelTime.play({ query: "pulp" })
ReelTime.playAt("08:30", { exactOnly: true })
ReelTime.random({ exactOnly: true })
ReelTime.stop()
```

Audio helpers:

```js
ReelTime.audio.beep()
ReelTime.audio.projectorStart()
ReelTime.audio.projectorStop()
```

## Rights note

I don't have the rights of the movies. Please don't sue me.
