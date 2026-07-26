# Reel Time

**Reel Time** is a talking clock made from movie scenes. Open it, press play, and let a film scene tell you the local time.

Production URL: [reel-time.thomaspericoi.com](https://reel-time.thomaspericoi.com)

## What it does

- Selects a scene from the current local time.
- Uses a cascade on first launch: exact match first, then broader/approximate scenes if needed.
- After the arrival scene, exact scenes stay first; `approx`, `before`, and `after` scenes can fill gaps once each per page load.
- Plays a 3-second vintage countdown with audio beeps.
- Shows film title, release year, director, and rights holder before and during playback.
- Simulates a 1920s-style projection with grain, flicker, vignette, and a short image-catch offset when the scene appears.
- Runs as plain static files. No framework, no build step, no server required.

## Library stats

Current library stats, generated from `assets/data/scenes.json`:

- Total scenes: **228**
- Exact-time scenes: **186**
- Exact minutes covered: **135 / 1440**
- Exact-time share: **9.4%**

`Exact minutes covered` counts unique exact minutes only. Scenes marked `both` count toward both their AM and PM hours.

| Hour | Exact minutes covered | Exact scene entries | All scene entries |
| --- | ---: | ---: | ---: |
| 00:00-00:59 | 5 | 8 | 19 |
| 01:00-01:59 | 9 | 12 | 17 |
| 02:00-02:59 | 5 | 16 | 21 |
| 03:00-03:59 | 6 | 19 | 27 |
| 04:00-04:59 | 5 | 9 | 17 |
| 05:00-05:59 | 5 | 12 | 20 |
| 06:00-06:59 | 7 | 12 | 20 |
| 07:00-07:59 | 6 | 11 | 20 |
| 08:00-08:59 | 8 | 21 | 30 |
| 09:00-09:59 | 5 | 11 | 16 |
| 10:00-10:59 | 4 | 12 | 14 |
| 11:00-11:59 | 4 | 10 | 16 |
| 12:00-12:59 | 5 | 11 | 16 |
| 13:00-13:59 | 8 | 11 | 13 |
| 14:00-14:59 | 5 | 14 | 17 |
| 15:00-15:59 | 6 | 14 | 20 |
| 16:00-16:59 | 6 | 7 | 13 |
| 17:00-17:59 | 4 | 8 | 13 |
| 18:00-18:59 | 6 | 7 | 13 |
| 19:00-19:59 | 4 | 10 | 20 |
| 20:00-20:59 | 7 | 17 | 27 |
| 21:00-21:59 | 4 | 12 | 19 |
| 22:00-22:59 | 5 | 15 | 18 |
| 23:00-23:59 | 6 | 15 | 24 |

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
  movie-posters/
  movie-scenes/   # local video files, ignored by git
  sounds/
    ahem_001.mp3
    ahem_002.mp3
    countdown_beep_001.mp3
    hush_001.mp3
    hush_002.mp3
    projector_001.mp3
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
dawn_broad_sunset-boulevard_001.mp4
fallback_you-can-count-on-me_001.mp4
```

Broad scenes use this alternate convention:

```text
broad-label_broad_movie-slug_###.mp4
```

Fallback scenes use:

```text
fallback_movie-slug_###.mp4
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
