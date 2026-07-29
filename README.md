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
- Presents a desktop-only experience on mobile, where browsers restrict timed video playback.

## Library stats

Current library stats, generated from `assets/data/scenes.json`:

- Total scenes: **290**
- Exact-time scenes: **232**
- Exact minutes covered: **169 / 1440**
- Exact-time share: **11.7%**

`Exact minutes covered` counts unique exact minutes only. Scenes marked `both` count toward both their AM and PM hours.

Exact minutes currently covered by at least one exact-time scene:

| Hour | Minutes |
| --- | --- |
| 00:00-00:59 | 00:00, 00:10, 00:15, 00:30, 00:31, 00:45 |
| 01:00-01:59 | 01:00, 01:06, 01:10, 01:15, 01:17, 01:18, 01:21, 01:30, 01:56 |
| 02:00-02:59 | 02:00, 02:15, 02:30, 02:45, 02:55, 02:59 |
| 03:00-03:59 | 03:00, 03:05, 03:08, 03:30, 03:42, 03:51 |
| 04:00-04:59 | 04:00, 04:11, 04:20, 04:30, 04:35, 04:36, 04:48 |
| 05:00-05:59 | 05:00, 05:02, 05:10, 05:30, 05:35 |
| 06:00-06:59 | 06:00, 06:05, 06:10, 06:15, 06:34, 06:35, 06:45, 06:53 |
| 07:00-07:59 | 07:00, 07:06, 07:15, 07:22, 07:23, 07:30 |
| 08:00-08:59 | 08:00, 08:12, 08:15, 08:17, 08:20, 08:30, 08:35, 08:42, 08:45 |
| 09:00-09:59 | 09:00, 09:15, 09:18, 09:30, 09:45 |
| 10:00-10:59 | 10:00, 10:01, 10:15, 10:25, 10:30, 10:33, 10:44, 10:45, 10:46, 10:55 |
| 11:00-11:59 | 11:00, 11:11, 11:30, 11:36, 11:40, 11:45, 11:56, 11:57 |
| 12:00-12:59 | 12:00, 12:10, 12:15, 12:30, 12:31, 12:45 |
| 13:00-13:59 | 13:00, 13:04, 13:06, 13:10, 13:15, 13:17, 13:21, 13:30, 13:56 |
| 14:00-14:59 | 14:00, 14:15, 14:30, 14:45, 14:55, 14:59 |
| 15:00-15:59 | 15:00, 15:08, 15:20, 15:30, 15:42, 15:51 |
| 16:00-16:59 | 16:00, 16:11, 16:20, 16:29, 16:30, 16:33, 16:35, 16:36, 16:48 |
| 17:00-17:59 | 17:00, 17:02, 17:10, 17:35 |
| 18:00-18:59 | 18:00, 18:05, 18:10, 18:15, 18:34, 18:35, 18:53 |
| 19:00-19:59 | 19:00, 19:06, 19:23, 19:30 |
| 20:00-20:59 | 20:00, 20:12, 20:15, 20:17, 20:20, 20:30, 20:35, 20:45 |
| 21:00-21:59 | 21:00, 21:15, 21:18, 21:30 |
| 22:00-22:59 | 22:00, 22:01, 22:04, 22:15, 22:25, 22:30, 22:33, 22:44, 22:45, 22:46, 22:55 |
| 23:00-23:59 | 23:00, 23:11, 23:30, 23:36, 23:40, 23:45, 23:55, 23:56, 23:57, 23:58 |

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

## Console API

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
