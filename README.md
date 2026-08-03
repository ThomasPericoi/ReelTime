# Reel Time

Reel Time is a talking clock made from movie scenes.

Open the site, press play, and let a film scene tell you the current local time. When no exact scene is available, Reel Time falls back to broader or approximate time references.

The project is intentionally compact: plain static files, no framework, no build step, and no server required.

## Demo

<https://reel-time.thomaspericoi.com>

## Features

* Selects a movie scene from the current local time.
* Prioritizes exact-time scenes when available.
* Uses approximate, before, after, broad, and generic fallback scenes to fill gaps.
* Plays a three-second countdown with audio beeps.
* Displays the film title, release year, director, and rights holder.
* Simulates a projection with grain, flicker, vignette, and image offset.
* Runs entirely as static HTML, CSS, JavaScript, JSON, video, and audio files.
* Provides a small console API for browsing and playing scenes.
* Presents a desktop-only experience on mobile, where browsers restrict timed video playback.

## Scene library

Current library statistics:

* Total scenes: **350**
* Exact-time scenes: **265**
* Exact minutes covered: **204 / 1440**
* Exact-time coverage: **14.2%**

`Exact minutes covered` counts unique exact minutes only.

Scenes marked as `both` count toward both their AM and PM equivalents.

### Exact minutes covered

| Hour | Minutes |
| --- | --- |
| 00:00-00:59 | 00:00, 00:10, 00:15, 00:30, 00:31, 00:45 |
| 01:00-01:59 | 01:00, 01:06, 01:10, 01:15, 01:17, 01:18, 01:21, 01:30, 01:45, 01:56 |
| 02:00-02:59 | 02:00, 02:15, 02:30, 02:45, 02:55, 02:59 |
| 03:00-03:59 | 03:00, 03:05, 03:08, 03:15, 03:30, 03:42, 03:45, 03:51 |
| 04:00-04:59 | 04:00, 04:05, 04:11, 04:15, 04:20, 04:30, 04:35, 04:36, 04:48 |
| 05:00-05:59 | 05:00, 05:02, 05:10, 05:15, 05:30, 05:35 |
| 06:00-06:59 | 06:00, 06:05, 06:10, 06:15, 06:30, 06:34, 06:35, 06:45, 06:53 |
| 07:00-07:59 | 07:00, 07:06, 07:07, 07:15, 07:22, 07:23, 07:30, 07:45 |
| 08:00-08:59 | 08:00, 08:12, 08:15, 08:17, 08:20, 08:30, 08:35, 08:42, 08:45, 08:59 |
| 09:00-09:59 | 09:00, 09:02, 09:15, 09:18, 09:20, 09:23, 09:30, 09:40, 09:45 |
| 10:00-10:59 | 10:00, 10:01, 10:15, 10:25, 10:30, 10:33, 10:44, 10:45, 10:46, 10:55 |
| 11:00-11:59 | 11:00, 11:01, 11:11, 11:30, 11:36, 11:40, 11:45, 11:46, 11:56, 11:57 |
| 12:00-12:59 | 12:00, 12:10, 12:15, 12:30, 12:31, 12:45 |
| 13:00-13:59 | 13:00, 13:04, 13:06, 13:10, 13:15, 13:17, 13:21, 13:30, 13:45, 13:56 |
| 14:00-14:59 | 14:00, 14:15, 14:30, 14:45, 14:55, 14:59 |
| 15:00-15:59 | 15:00, 15:08, 15:20, 15:30, 15:42, 15:45, 15:51 |
| 16:00-16:59 | 16:00, 16:05, 16:11, 16:15, 16:20, 16:29, 16:30, 16:33, 16:35, 16:36, 16:48 |
| 17:00-17:59 | 17:00, 17:02, 17:10, 17:15, 17:30, 17:35 |
| 18:00-18:59 | 18:00, 18:05, 18:10, 18:15, 18:30, 18:34, 18:35, 18:53 |
| 19:00-19:59 | 19:00, 19:06, 19:07, 19:15, 19:23, 19:30, 19:45 |
| 20:00-20:59 | 20:00, 20:12, 20:15, 20:17, 20:20, 20:30, 20:35, 20:45, 20:59 |
| 21:00-21:59 | 21:00, 21:02, 21:15, 21:18, 21:20, 21:23, 21:30, 21:40, 21:45 |
| 22:00-22:59 | 22:00, 22:01, 22:04, 22:15, 22:25, 22:30, 22:33, 22:44, 22:45, 22:46, 22:55 |
| 23:00-23:59 | 23:00, 23:01, 23:11, 23:30, 23:36, 23:40, 23:45, 23:46, 23:50, 23:55, 23:56, 23:57, 23:58 |

## Scene selection

On the first launch, Reel Time selects a scene using the following priority:

1. Exact time.
2. Approximate time.
3. Scene occurring shortly before or after the current time.
4. Broad period of the day.
5. Generic fallback scene.

After the arrival scene, exact scenes remain the priority.

Approximate, before, and after scenes can each be used once per page load to reduce repetition.

## Filename convention

### Exact and approximate scenes use

```text
HH-MM_period_precision_movie-slug_###.mp4
```

Examples:

```text
08-30_am_exact_ford-v-ferrari_001.mp4
12-00_both_approx_gremlins_001.mp4
08-00_both_before_lucky-number-slevin_001.mp4
```

Accepted period values include:

```text
am
pm
both
```

Accepted precision values include:

```text
exact
approx
before
after
```

### Broad scenes use

```text
broad-label_broad_movie-slug_###.mp4
```

Example:

```text
dawn_broad_sunset-boulevard_001.mp4
```

### Generic fallback scenes use

```text
fallback_movie-slug_###.mp4
```

Example:

```text
fallback_you-can-count-on-me_001.mp4
```

## Console API

Reel Time exposes a small API through the global `ReelTime` object.

Open the browser console after the page loads.

### Browse scenes

```js
ReelTime.scenes();
```

Return exact-time scenes only:

```js
ReelTime.scenes({ exactOnly: true });
```

Return scenes associated with a specific time:

```js
ReelTime.scenes({ time: "08:30" });
```

Search scenes by film name or metadata:

```js
ReelTime.find({ query: "pulp" });
```

### Play scenes

Play the first scene matching a query:

```js
ReelTime.play({ query: "pulp" });
```

Play a scene associated with a specific time:

```js
ReelTime.playAt("08:30");
```

Only use exact scenes:

```js
ReelTime.playAt("08:30", { exactOnly: true });
```

Play a random scene:

```js
ReelTime.random();
```

Play a random exact-time scene:

```js
ReelTime.random({ exactOnly: true });
```

Stop playback:

```js
ReelTime.stop();
```

### Audio

Play the countdown beep:

```js
ReelTime.audio.beep();
```

Start the projector sound:

```js
ReelTime.audio.projectorStart();
```

Stop the projector sound:

```js
ReelTime.audio.projectorStop();
```

## Maintenance scripts

No dependency installation or build step is required for the site itself.

Open `index.html` directly in a browser.

When scenes are added, renamed, or removed, rebuild the scene library:

```bash
python3 tools/build-scenes-json.py
```

`build-scenes-json.py` reads filenames from `assets/medias/videos/movie-scenes/`, resolves movie metadata from `MOVIE_META`, applies `SPAN_LABELS`, and regenerates:

```text
assets/data/scenes.json
assets/data/scenes-data.js
```

`scenes.json` is the readable data export. `scenes-data.js` is loaded directly by the browser, including when opening the project through `file://`.

When MP4 files need to be cleaned after renaming or importing, run:

```bash
python3 tools/clean-mp4-metadata.py
```

`clean-mp4-metadata.py` removes inherited MP4 metadata and chapters, keeps the media streams without re-encoding, sets the internal video title to the filename, and applies `faststart` for better browser playback.

## Structure

```text
index.html
README.md
assets/
  css/
    styles.css
  js/
    app.js
    ascii-printer.min.js
  data/
    scenes-data.js
    scenes.json
  medias/
    images/
      high-noon-cover.jpeg
      movie-posters/
    sounds/
      ahem_001.mp3
      ahem_002.mp3
      countdown_beep_001.mp3
      hush_001.mp3
      hush_002.mp3
      projector_001.mp3
    videos/
      movie-scenes/
tools/
  build-scenes-json.py
  clean-mp4-metadata.py
```

The local video files stored in `assets/medias/videos/movie-scenes/` are intentionally ignored by Git.

## Stack

* HTML.
* CSS.
* Vanilla JavaScript.
* Python for scene-data generation.
* Static audio and video files.

## Rights notice

Reel Time uses short excerpts from films for a non-commercial experimental project.

The films, scenes, characters, music, trademarks, and related materials belong to their respective rights holders.

No ownership of third-party material is claimed.

Please don't sue me.
