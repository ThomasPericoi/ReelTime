(() => {
  "use strict";

  /*________________________________________ CONFIG ________________________________________*/

  const SELECTORS = {
    app: "#app",
    scene: "#scene",
    startPanel: "#startPanel",
    startButton: "#startButton",
    startMessage: "#startMessage",
    posterWall: "#posterWall",
    countdown: "#countdown",
    countdownNumber: "#countdownNumber",
    titleCard: "#titleCard",
    idle: "#idle",
    localTime: "#localTime",
    idleMessage: "#idleMessage",
    movieTitle: "#movieTitle",
    sceneMatch: "#sceneMatch",
    rightsIntro: "#rightsIntro",
    playbackStatus: "#playbackStatus",
    currentCredit: "#currentCredit",
    overlayMatch: "#overlayMatch",
    overlayMovie: "#overlayMovie",
    overlayRights: "#overlayRights",
    nextCountdown: "#nextCountdown",
    nextTimer: "#nextTimer",
    replayButton: "#replayButton",
    cornerSignature: "#cornerSignature",
    volumeControl: "#volumeControl",
    volumeRange: "#volumeRange",
    volumeValue: "#volumeValue",
    favicon: "#favicon",
  };

  const PRIORITY = {
    exact: 1,
    before: 2,
    after: 2,
    approx: 3,
    range: 4,
    broad: 5,
    fallback: 9,
  };

  const FLEXIBLE_PRECISIONS = new Set(["approx", "before", "after"]);
  const TIME_FORMAT_KEY = "reel-time-hour-format";
  const TIME_FORMATS = createTimeFormatters();
  const ONGOING_PRECISIONS = new Set(["exact", ...FLEXIBLE_PRECISIONS]);

  const SOUND_PATHS = {
    countdownBeep: "assets/medias/sounds/countdown_beep_001.mp3",
    projector: "assets/medias/sounds/projector_001.mp3",
    titleNoises: [
      "assets/medias/sounds/ahem_001.mp3",
      "assets/medias/sounds/ahem_002.mp3",
      "assets/medias/sounds/hush_001.mp3",
      "assets/medias/sounds/hush_002.mp3",
    ],
  };

  const IDLE_MESSAGE = "Waiting for the next scene to play. Grab some pop-corn.";

  const POSTER_BASE_PATH = "assets/medias/images/movie-posters/";
  const POSTER_FILES = [
    "12-angry-men.jpg",
    "12-monkeys.jpg",
    "127-hours.jpg",
    "3-10-to-yuma.jpg",
    "8-bit-christmas.jpg",
    "a-beautiful-mind.jpg",
    "a-christmas-story.jpg",
    "a-clockwork-orange.jpg",
    "a-fish-called-wanda.jpg",
    "a-nightmare-on-elm-street.jpg",
    "a-serious-man.jpg",
    "a-star-is-born.jpg",
    "all-the-president-s-men.jpg",
    "american-gangster.jpg",
    "american-hustle.jpg",
    "american-made.jpg",
    "american-psycho.jpg",
    "and-justice-for-all.jpg",
    "annie.jpg",
    "anora.jpg",
    "ant-man-and-the-wasp-quantumania.jpg",
    "antichrist.jpg",
    "apocalypse-now.jpg",
    "asteroid-city.jpg",
    "babe.jpg",
    "back-to-the-future-part-3.jpg",
    "back-to-the-future.jpg",
    "basic-instinct.jpg",
    "batman-returns.jpg",
    "beetlejuice.jpg",
    "before-sunrise.jpg",
    "being-john-malkovich.jpg",
    "being-the-ricardos.jpg",
    "being-there.jpg",
    "belfast.jpg",
    "big.jpg",
    "black-hawk-down.jpg",
    "blue-velvet.jpg",
    "bone-tomahawk.jpg",
    "bugonia.jpg",
    "burn-after-reading.jpg",
    "captain-fantastic.jpg",
    "carrie.jpg",
    "casablanca.jpg",
    "cast-away.jpg",
    "chef.jpg",
    "child-s-play.jpg",
    "citizen-kane.jpg",
    "clueless.jpg",
    "crazy-stupid-love.jpg",
    "darkest-hour.jpg",
    "dave.jpg",
    "dawn-of-the-dead.jpg",
    "demolition.jpg",
    "den-of-thieves.jpg",
    "die-hard-2.jpg",
    "donnie-darko.jpg",
    "dr-strangelove.jpg",
    "dumb-and-dumber.jpg",
    "ed-wood.jpg",
    "election.jpg",
    "escape-from-new-york.jpg",
    "eternal-sunshine-of-the-spotless-mind.jpg",
    "evil-dead-2.jpg",
    "ex-machina.jpg",
    "eyes-wide-shut.jpg",
    "fantastic-mister-fox.jpg",
    "fargo.jpg",
    "father-of-the-bride.jpg",
    "fifth-element.jpg",
    "flubber.jpg",
    "ford-v-ferrari.jpg",
    "foul-play.jpg",
    "four-lions.jpg",
    "foxcatcher.jpg",
    "from-dusk-till-dawn.jpg",
    "from-russia-with-love.jpg",
    "fury.jpg",
    "ghostbusters.jpg",
    "good-morning-vietnam.jpg",
    "good-time.jpg",
    "good-will-hunting.jpg",
    "goodfellas.jpg",
    "gran-torino.jpg",
    "green-book.jpg",
    "gremlins-2.jpg",
    "gremlins.jpg",
    "halloween-3.jpg",
    "hostel-2.jpg",
    "i-saw-the-tv-glow.jpg",
    "in-the-loop.jpg",
    "in-the-name-of-the-father.jpg",
    "incredibles-2.jpg",
    "indiana-jones-3.jpg",
    "insidious.jpg",
    "insomnia.jpg",
    "inspector-gadget-2.jpg",
    "into-the-wild.jpg",
    "jacob-s-ladder.jpg",
    "jaws.jpg",
    "jumpin-jack-flash.jpg",
    "labyrinth.jpg",
    "lady-and-the-tramp.jpg",
    "late-night-with-the-devil.jpeg",
    "leon-the-professional.jpg",
    "lethal-weapon-3.jpg",
    "lethal-weapon.jpg",
    "little-miss-sunshine.jpg",
    "live-and-let-die.jpg",
    "lolita.jpg",
    "lost-in-translation.jpg",
    "lucky-number-slevin.jpg",
    "manchester-by-the-sea.jpg",
    "marty-supreme.jpg",
    "master-and-commander.jpg",
    "mean-girls.jpg",
    "memento.jpg",
    "men-in-black-2.jpg",
    "mickey-17.jpg",
    "mid90s.jpg",
    "midsommar.jpeg",
    "mission-impossible-3.jpg",
    "mommie-dearest.jpg",
    "mona-lisa-smile.jpg",
    "moonrise-kingdom.jpg",
    "mulholland-drive.jpg",
    "munich.jpg",
    "night-school.jpg",
    "nightcrawler.jpg",
    "no-country-for-old-men.jpg",
    "no-hard-feelings.jpg",
    "no-strings-attached.jpg",
    "nocturnal-animals.jpg",
    "nosferatu.jpg",
    "notorious.jpg",
    "novocaine.jpg",
    "ocean-s-eleven.jpg",
    "ocean-s-twelve.jpg",
    "once-upon-a-time-in-america.jpg",
    "once-upon-a-time-in-hollywood.jpg",
    "paddington.jpg",
    "paris-texas.jpg",
    "percy-jackson.jpg",
    "pig.jpg",
    "pinocchio.jpg",
    "point-break.jpg",
    "predator.jpg",
    "primal-fear.jpg",
    "primer.jpg",
    "pulp-fiction.jpg",
    "quick-change.jpg",
    "rainman.jpg",
    "rear-window.jpg",
    "road-house.jpg",
    "rocky.jpg",
    "roman-holiday.jpg",
    "sabrina.jpg",
    "sandlot.jpg",
    "scarface.jpg",
    "school-ties.jpg",
    "scott-pilgrim-vs-the-world.jpg",
    "scrooge.jpg",
    "sergeant-york.jpg",
    "shaun-of-the-dead.jpg",
    "shawshank-redemption.jpg",
    "sherlock-holmes-2.jpg",
    "sicario.jpg",
    "sing-sing.jpg",
    "sleeping-beauty.jpg",
    "sleepless-in-seattle.jpg",
    "snowden.jpg",
    "some-like-it-hot.jpg",
    "spirited.jpg",
    "spotlight.jpg",
    "stand-by-me.jpg",
    "sunset-boulevard.jpg",
    "superbad.jpg",
    "taxi-driver.jpg",
    "ted.jpg",
    "tenet.jpg",
    "terminator.jpg",
    "the-age-of-innocence.jpg",
    "the-aviator.jpg",
    "the-babadook.jpg",
    "the-banshees-of-inisherin.jpg",
    "the-blues-brothers.jpg",
    "the-breakfast-club.jpg",
    "the-cat-in-the-hat.jpg",
    "the-change-up.jpg",
    "the-conjuring.jpg",
    "the-conversation.jpg",
    "the-cutting-edge.jpg",
    "the-departed.jpg",
    "the-elephant-man.jpg",
    "the-eyes-of-tammy-faye.jpg",
    "the-farewell.jpg",
    "the-father.jpg",
    "the-florida-project.jpg",
    "the-game.jpg",
    "the-green-mile.jpg",
    "the-hustler.jpg",
    "the-irishman.jpg",
    "the-iron-giant.jpg",
    "the-lego-batman-movie.jpg",
    "the-lobster.jpg",
    "the-lost-daughter.jpg",
    "the-man-who-fell-to-earth.jpg",
    "the-martian.jpg",
    "the-master.jpg",
    "the-mist.jpg",
    "the-notebook.jpg",
    "the-road.jpg",
    "the-rocky-horror-picture-show.jpg",
    "the-social-network.jpg",
    "the-space-children.jpg",
    "the-spongebob-movie-sponge-out-of-water.jpg",
    "the-sting.jpg",
    "the-strange-case-of-benjamin-button.jpg",
    "the-thin-red-line.jpg",
    "the-usual-suspects.jpg",
    "the-world-s-end.jpg",
    "thelma-and-louise.jpg",
    "there-will-be-blood.jpg",
    "to-kill-a-mockingbird.jpg",
    "trading-places.jpg",
    "trainspotting-2.jpg",
    "true-grit.jpg",
    "true-lies.jpg",
    "under-the-skin.jpg",
    "unfriended.jpg",
    "us.jpg",
    "wall-e.jpg",
    "watchmen.jpg",
    "we-bought-a-zoo.jpg",
    "weapons.jpg",
    "west-side-story.jpg",
    "wet-hot-american-summer.jpg",
    "what-we-do-in-the-shadows.jpg",
    "when-harry-met-sally.jpg",
    "wonder-boys.jpg",
    "yes-man.jpg",
    "you-can-count-on-me.jpg",
    "zero-dark-thirty.jpg",
    "zodiac.jpg",
  ];

  const TIMING = {
    countdownStepMs: 1000,
    titleCardMs: 2200,
    projectorFadeMs: 1800,
    quickFadeMs: 500,
    endLookSeconds: 1.25,
  };

  const VOLUME = {
    countdownBeep: 0.6,
    projector: 0.35,
    titleNoise: 0.5,
    master: 0.8,
  };

  const FAVICON = {
    paper: "#f4ecd8",
    ink: "#050505",
    rec: "#c6261a",
  };

  /*_____________________________________ APP STATE ______________________________________*/

  const el = Object.fromEntries(
    Object.entries(SELECTORS).map(([key, selector]) => [key, document.querySelector(selector)]),
  );

  const state = {
    scenes: [],
    currentScene: null,
    currentSceneDate: null,
    hasStarted: false,
    isPlayingSequence: false,
    isScenePlaying: false,
    sequenceToken: 0,
    nextCheckAt: null,
    timers: [],
    renderedLocalTime: "",
    renderedNextTimer: "",
    masterVolume: VOLUME.master,
    playedFlexibleSceneIds: new Set(),
    lastPlayedMinuteKey: "",
  };

  const audio = {
    projector: null,
    fadeFrame: null,
  };

  const panels = [el.countdown, el.titleCard, el.idle];

  /*_______________________________________ APP BOOT _______________________________________*/

  init();

  async function init() {
    if (globalThis.AsciiPrinter) {
      AsciiPrinter.printByName("television");
    }
    setFaviconLetter();
    tickClock();
    window.setInterval(tickClock, 1000);
    initVolumeControl();
    initPosterWall();
    el.startButton.addEventListener("click", startClock, { once: true });
    el.replayButton.addEventListener("click", replayCurrentScene);

    try {
      const library = await loadSceneLibrary();
      state.scenes = library.scenes.map(normalizeScene).sort(sortScenes);
      installConsoleApi();
      el.startMessage.textContent = "A talking clock made of movie scenes. Leave it open and wait for cinema to tell you the time.";
      el.startButton.disabled = false;
    } catch {
      el.startMessage.textContent = "Could not load the scene library. Check that assets/data/scenes-data.js is available.";
    }
  }

  /*_____________________________________ POSTER WALL ______________________________________*/

  function initPosterWall() {
    if (!el.posterWall || !POSTER_FILES.length || prefersReducedMotion()) return;

    const isCompactViewport = window.matchMedia("(max-width: 720px)").matches;
    const columnCount = isCompactViewport ? 5 : 8;
    const rowsPerColumn = isCompactViewport ? 8 : 9;
    const pool = createPosterPool();
    const fragment = document.createDocumentFragment();

    el.posterWall.textContent = "";
    el.posterWall.style.setProperty("--poster-columns", columnCount);

    for (let columnIndex = 0; columnIndex < columnCount; columnIndex += 1) {
      const column = document.createElement("div");
      column.className = "poster-wall__column";
      column.style.setProperty("--poster-duration", `${250 + columnIndex * 5}s`);
      column.style.setProperty("--poster-offset", `${(columnIndex % 3) * -4}rem`);
      if (columnIndex % 2) column.classList.add("poster-wall__column--reverse");

      const group = document.createElement("div");
      group.className = "poster-wall__group";
      for (let rowIndex = 0; rowIndex < rowsPerColumn; rowIndex += 1) {
        group.append(createPoster(pool.next().value));
      }

      column.append(group, group.cloneNode(true));
      fragment.append(column);
    }

    el.posterWall.append(fragment);
    window.setTimeout(() => {
      window.requestAnimationFrame(() => el.posterWall.classList.add("is-visible"));
    }, 500);
  }

  function* createPosterPool() {
    let pool = [];
    while (true) {
      if (!pool.length) pool = shuffle(POSTER_FILES);
      yield pool.pop();
    }
  }

  function createPoster(src) {
    const img = document.createElement("img");
    img.className = "poster-wall__poster";
    img.src = `${POSTER_BASE_PATH}${src}`;
    img.alt = "";
    img.loading = "lazy";
    img.decoding = "async";
    return img;
  }

  /*____________________________________ SCENE LIBRARY ____________________________________*/

  async function loadSceneLibrary() {
    if (window.REEL_TIME_SCENES?.scenes?.length) return window.REEL_TIME_SCENES;

    if (location.protocol !== "file:") {
      const response = await fetch("assets/data/scenes.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`assets/data/scenes.json returned ${response.status}`);
      return response.json();
    }

    throw new Error("assets/data/scenes-data.js is required when opening Reel Time as a local file.");
  }

  /*______________________________________ SCHEDULER ______________________________________*/

  function startClock() {
    enterPlaybackMode();
    applySceneVolume();
    scheduleFromNow({ playImmediately: true, mode: "arrival" });
  }

  function enterPlaybackMode() {
    state.hasStarted = true;
    el.startPanel.hidden = true;
    el.cornerSignature.hidden = false;
    el.volumeControl.hidden = false;
  }

  function tickClock() {
    updateClockFace();
    tickScheduler();
  }

  function tickScheduler() {
    if (!state.hasStarted || !state.scenes.length || state.isPlayingSequence) return;
    if (!state.nextCheckAt || Date.now() >= state.nextCheckAt.getTime()) {
      scheduleFromNow({ playImmediately: false, mode: "ongoing" });
    }
  }

  function scheduleFromNow({ playImmediately, mode }) {
    const now = new Date();
    const selected = selectScene(now, { mode });

    if (selected && playImmediately) {
      playSequence(selected, now);
      return;
    }

    if (selected && selected.id !== state.currentScene?.id && !hasPlayedThisMinute(now)) {
      playSequence(selected, now);
      return;
    }

    state.nextCheckAt = findNextPlayableTime(afterCurrentMinute(now), { mode: "ongoing" });
    showIdle(idleMessageFor(state.currentScene, state.currentSceneDate));
  }

  /*__________________________________ PLAYBACK SEQUENCE __________________________________*/

  async function playSequence(scene, contextDate = sceneContextDate(scene)) {
    const token = beginSequence(scene, contextDate);

    try {
      await showCountdown(token);
      startProjectorSound();
      await showTitleCard(scene, token, contextDate);
      state.nextCheckAt = findNextPlayableTime(new Date(), { mode: "ongoing" });
      showNextCountdown();
      const didPlay = await playScene(scene, token, contextDate);
      if (didPlay) settleVideo();
      else resetVideo();
      setFaviconLetter();
      await fadeOutProjectorSound();
    } finally {
      if (token !== state.sequenceToken) return;
      state.isPlayingSequence = false;
      state.nextCheckAt = findNextPlayableTime(new Date(), { mode: "ongoing" });
      scheduleFromNow({ playImmediately: false, mode: "ongoing" });
      if (!state.isPlayingSequence) {
        restoreRoomLight();
        showReplayButton();
      }
    }
  }

  function beginSequence(scene, contextDate) {
    state.sequenceToken += 1;
    state.isPlayingSequence = true;
    state.currentScene = scene;
    state.currentSceneDate = new Date(contextDate);
    state.lastPlayedMinuteKey = minuteKey(new Date());
    rememberFlexibleScene(scene);
    clearManagedTimers();
    hideSequenceUi();
    resetVideo();
    dimRoom();
    return state.sequenceToken;
  }

  async function showCountdown(token) {
    showPanel(el.countdown);
    for (const value of [3, 2, 1]) {
      if (token !== state.sequenceToken) return;
      el.countdownNumber.textContent = value;
      setFaviconCountdown(value);
      playCountdownBeep();
      await sleep(TIMING.countdownStepMs);
    }
    el.countdown.hidden = true;
  }

  async function showTitleCard(scene, token, contextDate) {
    if (token !== state.sequenceToken) return;
    setFaviconRecording();
    el.movieTitle.textContent = scene.movieTitle;
    el.sceneMatch.textContent = sceneMatchLine(scene, contextDate);
    el.rightsIntro.textContent = creditLine(scene);
    maybePlayTitleNoise();
    showPanel(el.titleCard);
    await sleep(TIMING.titleCardMs);
    el.titleCard.hidden = true;
  }

  function playScene(scene, token, contextDate) {
    return new Promise((resolve) => {
      if (token !== state.sequenceToken) {
        resolve(false);
        return;
      }

      hidePanels();
      setCreditOverlay(scene, contextDate);
      prepareSceneVideo(scene);
      requestAnimationFrame(() => el.scene.classList.add("gate-hit"));

      const finish = (didPlay) => {
        state.isScenePlaying = false;
        resolve(didPlay);
      };

      el.scene.ontimeupdate = () => updateEndingLook(token);
      el.scene.onended = () => finish(true);
      el.scene.onerror = () => finish(false);

      state.isScenePlaying = true;
      el.scene.play().catch(() => finish(false));
    });
  }

  function prepareSceneVideo(scene) {
    const src = encodeURI(scene.src);
    if (el.scene.getAttribute("src") !== src) {
      el.scene.src = src;
      el.scene.load();
    }

    el.scene.classList.remove("gate-hit", "is-ending");
    el.scene.defaultMuted = false;
    el.scene.muted = false;
    el.scene.removeAttribute("muted");
    applySceneVolume();
  }

  function updateEndingLook(token) {
    if (token !== state.sequenceToken || !Number.isFinite(el.scene.duration)) return;
    const remaining = el.scene.duration - el.scene.currentTime;
    el.scene.classList.toggle("is-ending", remaining <= TIMING.endLookSeconds);
  }

  /*____________________________________ SCENE MATCHING ____________________________________*/

  function selectScene(date, options = {}) {
    const pool = bestScenePool(date, options);
    return pool.length ? randomItem(pool) : null;
  }

  function bestScenePool(date, options = {}) {
    const minute = date.getHours() * 60 + date.getMinutes();
    const matches = state.scenes.filter((scene) => isPlayableScene(scene, minute, options));
    if (!matches.length) return [];

    const bestPriority = Math.min(...matches.map((scene) => scene.priority));
    const priorityMatches = matches.filter((scene) => scene.priority === bestPriority);
    const bestSpanSize = Math.min(...priorityMatches.map(spanSize));
    return priorityMatches.filter((scene) => spanSize(scene) === bestSpanSize);
  }

  function isPlayableScene(scene, minute, options) {
    if (!coversMinute(scene, minute)) return false;
    if (options.exactOnly) return scene.precision === "exact";
    if (options.mode === "ongoing") return isOngoingScene(scene);
    return true;
  }

  function isOngoingScene(scene) {
    if (!ONGOING_PRECISIONS.has(scene.precision)) return false;
    if (!isFlexibleScene(scene)) return true;
    return !state.playedFlexibleSceneIds.has(scene.id);
  }

  function isFlexibleScene(scene) {
    return FLEXIBLE_PRECISIONS.has(scene.precision);
  }

  function rememberFlexibleScene(scene) {
    if (isFlexibleScene(scene)) state.playedFlexibleSceneIds.add(scene.id);
  }

  function findNextPlayableTime(fromDate, options = {}) {
    const start = new Date(fromDate);
    start.setSeconds(0, 0);
    start.setMinutes(start.getMinutes() + 1);

    for (let offset = 0; offset < 1440; offset += 1) {
      const candidate = new Date(start.getTime() + offset * 60_000);
      if (selectScene(candidate, options)) return candidate;
    }

    return new Date(start.getTime() + 60_000);
  }

  function hasPlayedThisMinute(date) {
    return state.lastPlayedMinuteKey === minuteKey(date);
  }

  function minuteKey(date) {
    return `${date.getFullYear()}-${date.getMonth()}-${date.getDate()}-${date.getHours()}-${date.getMinutes()}`;
  }

  function afterCurrentMinute(date) {
    const next = new Date(date);
    next.setSeconds(0, 0);
    return next;
  }

  /*__________________________________ SCENE NORMALIZATION _________________________________*/

  function normalizeScene(scene) {
    const { id, ...rest } = scene;
    const spans = (scene.spans || [{ start: scene.spanStart, end: scene.spanEnd }]).map((span) => ({
      start: span.start,
      end: span.end,
      startMinute: toMinuteOfDay(span.start),
      endMinute: toMinuteOfDay(span.end),
    }));

    return {
      id,
      ...rest,
      spans,
      priority: scene.priority ?? PRIORITY[scene.precision] ?? 9,
    };
  }

  function sortScenes(a, b) {
    return (
      a.priority - b.priority ||
      spanSize(a) - spanSize(b) ||
      a.movieTitle.localeCompare(b.movieTitle) ||
      a.id.localeCompare(b.id)
    );
  }

  function coversMinute(scene, minute) {
    return scene.spans.some((span) => {
      if (span.startMinute <= span.endMinute) {
        return minute >= span.startMinute && minute <= span.endMinute;
      }
      return minute >= span.startMinute || minute <= span.endMinute;
    });
  }

  function spanSize(scene) {
    return Math.min(
      ...scene.spans.map((span) => {
        if (span.startMinute <= span.endMinute) return span.endMinute - span.startMinute + 1;
        return 1440 - span.startMinute + span.endMinute + 1;
      }),
    );
  }

  function idleMessageFor(scene, date) {
    if (!scene) return [IDLE_MESSAGE];
    const contextDate = date || sceneContextDate(scene);
    const count = sceneSlotCountForScene(scene, contextDate);
    if (count <= 1) return [IDLE_MESSAGE];
    return [`The time slot "${timeSlotLabel(scene, contextDate)}" has ${count} different scenes.`, IDLE_MESSAGE];
  }

  function sceneSlotCountForScene(scene, date) {
    if (scene.precision === "fallback") {
      return state.scenes.filter((candidate) => candidate.precision === "fallback").length;
    }

    if (scene.precision === "broad") {
      return state.scenes.filter((candidate) =>
        candidate.precision === "broad" && candidate.displayTime === scene.displayTime,
      ).length;
    }

    const referenceSpan = matchingSpan(scene, date) || scene.spans[0];
    const referenceTarget = sceneTargetMinute(scene, referenceSpan);

    return state.scenes.filter((candidate) =>
      candidate.precision === scene.precision &&
      candidate.spans.some((span) => sceneTargetMinute(candidate, span) === referenceTarget),
    ).length;
  }

  function timeSlotLabel(scene, date) {
    if (scene.precision === "fallback") return "lost track of time";
    if (scene.precision === "broad") return scene.displayTime.toLowerCase();

    const span = matchingSpan(scene, date) || scene.spans[0];
    const target = sceneTargetTime(scene, span);
    const labels = {
      exact: "exactly",
      before: "before",
      after: "after",
      approx: "approximately",
      range: "around",
    };

    return `${labels[scene.precision] || scene.precision} ${target}`;
  }

  function sceneTargetMinute(scene, span) {
    if (scene.precision === "before") return span.endMinute;
    if (scene.precision === "after") return span.startMinute;
    if (scene.precision === "approx" || scene.precision === "range") return centerMinute(span);
    return span.startMinute;
  }

  /*_______________________________________ AUDIO _________________________________________*/

  function initVolumeControl() {
    el.volumeRange.value = Math.round(state.masterVolume * 100);
    updateVolumeControl();
    el.volumeRange.addEventListener("input", () => {
      setMasterVolume(Number(el.volumeRange.value) / 100);
    });
  }

  function applySceneVolume() {
    el.scene.volume = state.masterVolume;
  }

  function setMasterVolume(value) {
    state.masterVolume = clamp(value, 0, 1);
    applySceneVolume();
    if (audio.projector && !audio.fadeFrame) audio.projector.volume = scaledVolume(VOLUME.projector);
    updateVolumeControl();
  }

  function updateVolumeControl() {
    el.volumeValue.textContent = `${Math.round(state.masterVolume * 100)}%`;
  }

  function scaledVolume(value) {
    return value * state.masterVolume;
  }

  function playCountdownBeep() {
    playOneShot(SOUND_PATHS.countdownBeep, VOLUME.countdownBeep);
  }

  function maybePlayTitleNoise() {
    if (Math.random() >= 0.25) return;
    const noise = randomItem(SOUND_PATHS.titleNoises);
    playOneShot(noise, VOLUME.titleNoise);
  }

  function playOneShot(src, volume) {
    const sound = new Audio(src);
    sound.volume = scaledVolume(volume);
    sound.play().catch(() => { });
  }

  function startProjectorSound() {
    cancelProjectorFade();
    if (!audio.projector) {
      audio.projector = new Audio(SOUND_PATHS.projector);
      audio.projector.loop = true;
    }
    audio.projector.pause();
    audio.projector.currentTime = 0;
    audio.projector.volume = scaledVolume(VOLUME.projector);
    audio.projector.play().catch(() => { });
  }


  function fadeOutProjectorSound(duration = TIMING.projectorFadeMs) {
    return new Promise((resolve) => {
      if (!audio.projector || audio.projector.paused) {
        resolve();
        return;
      }

      cancelProjectorFade();
      const initialVolume = audio.projector.volume;
      const startedAt = performance.now();

      const step = (now) => {
        const progress = Math.min(1, (now - startedAt) / duration);
        audio.projector.volume = initialVolume * (1 - progress);

        if (progress < 1) {
          audio.fadeFrame = requestAnimationFrame(step);
          return;
        }

        audio.projector.pause();
        audio.projector.currentTime = 0;
        audio.projector.volume = scaledVolume(VOLUME.projector);
        audio.fadeFrame = null;
        resolve();
      };

      audio.fadeFrame = requestAnimationFrame(step);
    });
  }

  function cancelProjectorFade() {
    if (!audio.fadeFrame) return;
    cancelAnimationFrame(audio.fadeFrame);
    audio.fadeFrame = null;
  }

  function stopPlayback(options = {}) {
    state.sequenceToken += 1;
    clearManagedTimers();
    fadeOutProjectorSound(TIMING.quickFadeMs);
    resetVideo();
    state.isPlayingSequence = false;
    restoreRoomLight();
    hidePanels();
    setFaviconLetter();
    if (options.showIdle !== false) showIdle(idleMessageFor(state.currentScene, state.currentSceneDate));
  }

  /*__________________________________________ UI __________________________________________*/

  function dimRoom() {
    el.app.classList.add("is-room-dark");
  }

  function restoreRoomLight() {
    el.app.classList.remove("is-room-dark");
  }

  function settleVideo() {
    el.scene.pause();
    el.app.classList.add("has-freeze-frame");
    el.scene.classList.remove("gate-hit");
    el.scene.classList.add("is-ending");
    clearSceneHandlers();
  }

  function resetVideo() {
    state.isScenePlaying = false;
    el.scene.pause();
    el.scene.defaultMuted = false;
    el.scene.muted = false;
    el.scene.removeAttribute("muted");
    el.app.classList.remove("has-freeze-frame");
    el.scene.classList.remove("gate-hit", "is-ending");
    clearSceneHandlers();
    el.scene.removeAttribute("src");
    el.scene.load();
  }

  function clearSceneHandlers() {
    el.scene.ontimeupdate = null;
    el.scene.onended = null;
    el.scene.onerror = null;
  }

  function showPanel(panel) {
    hidePanels();
    panel.hidden = false;
  }

  function hidePanels() {
    panels.forEach((panel) => {
      panel.hidden = true;
    });
  }

  function hideSequenceUi() {
    clearCreditOverlay();
    hidePlaybackStatus();
    hideNextCountdown();
    hideReplayButton();
  }

  function showIdle(message) {
    clearCreditOverlay();
    renderIdleMessage(message);
    el.idle.hidden = false;
    if (state.hasStarted) {
      showPlaybackStatus();
      showNextCountdown();
    }
  }

  function renderIdleMessage(message) {
    const lines = Array.isArray(message) ? message : [message];
    el.idleMessage.replaceChildren();
    lines.forEach((line, index) => {
      if (index) el.idleMessage.append(document.createElement("br"));
      el.idleMessage.append(document.createTextNode(line));
    });
  }

  function setCreditOverlay(scene, contextDate) {
    showPlaybackStatus();
    el.currentCredit.hidden = false;
    el.overlayMatch.textContent = sceneMatchLine(scene, contextDate);
    el.overlayMovie.textContent = scene.movieTitle;
    el.overlayRights.textContent = creditLine(scene);
  }

  function clearCreditOverlay() {
    el.currentCredit.hidden = true;
    el.overlayMatch.textContent = "";
    el.overlayMovie.textContent = "";
    el.overlayRights.textContent = "";
  }

  function showNextCountdown() {
    el.nextCountdown.hidden = false;
    updateClockFace();
  }

  function showReplayButton() {
    el.replayButton.hidden = !state.currentScene;
  }

  function hideReplayButton() {
    el.replayButton.hidden = true;
  }

  function hideNextCountdown() {
    el.nextCountdown.hidden = true;
  }

  function showPlaybackStatus() {
    el.playbackStatus.hidden = false;
  }

  function hidePlaybackStatus() {
    el.playbackStatus.hidden = true;
  }

  function updateClockFace() {
    const now = new Date();
    renderText(el.localTime, "renderedLocalTime", formatClockTime(now));

    if (state.nextCheckAt) {
      const nextTimer = formatDuration(Math.max(0, state.nextCheckAt.getTime() - now.getTime()));
      renderText(el.nextTimer, "renderedNextTimer", nextTimer);
    }
  }

  function renderText(node, cacheKey, value) {
    if (state[cacheKey] === value) return;
    state[cacheKey] = value;
    node.textContent = value;
  }

  function setFaviconLetter() {
    setFaviconIcon(
      `<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" fill="${FAVICON.ink}" font-family="Limelight, Georgia, serif" font-size="44">R</text>`,
    );
  }

  function setFaviconCountdown(value) {
    setFaviconIcon(
      `<text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" fill="${FAVICON.paper}" font-family="Limelight, Georgia, serif" font-size="42">${value}</text>`,
      FAVICON.ink,
    );
  }

  function setFaviconRecording() {
    setFaviconIcon(`<circle cx="32" cy="32" r="17" fill="${FAVICON.rec}"/>`, FAVICON.ink);
  }

  function setFaviconIcon(content, background = FAVICON.paper) {
    setFaviconSvg(`
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
        <rect width="64" height="64" rx="6" fill="${background}"/>
        ${content}
      </svg>
    `);
  }

  function setFaviconSvg(svg) {
    el.favicon.href = `data:image/svg+xml,${encodeURIComponent(svg.trim())}`;
  }

  /*_______________________________________ CREDITS _______________________________________*/

  function rightsLine(scene) {
    return `Rights held by ${scene.rightsHolder || "Rights holder to verify"}`;
  }

  function filmMetaLine(scene) {
    const year = scene.releaseYear || "Year to verify";
    const director = scene.director || "Director to verify";
    return `${year} · Directed by ${director}`;
  }

  function creditLine(scene) {
    return `${filmMetaLine(scene)} · ${rightsLine(scene)}`;
  }

  function sceneMatchLine(scene, date = new Date()) {
    if (scene.precision === "fallback") return "Best time match: Lost track of time";
    if (scene.precision === "broad") return `Best time match: ${scene.displayTime}`;

    const span = matchingSpan(scene, date) || scene.spans[0];
    const target = sceneTargetTime(scene, span);
    const labels = {
      exact: "Exactly",
      before: "Before",
      after: "After",
      approx: "Approximately",
      range: "Around",
    };

    return `Best time match: ${labels[scene.precision] || titleCase(scene.precision)} ${target}`;
  }

  function matchingSpan(scene, date) {
    const minute = date.getHours() * 60 + date.getMinutes();
    return scene.spans.find((span) => coversSpanMinute(span, minute));
  }

  function sceneTargetTime(scene, span) {
    if (!span) return formatSceneTime(scene.displayTime);
    if (scene.precision === "before") return formatSceneTime(span.end);
    if (scene.precision === "after") return formatSceneTime(span.start);
    if (scene.precision === "approx" || scene.precision === "range") return formatMinuteAsSceneTime(centerMinute(span));
    return formatSceneTime(span.start);
  }

  function coversSpanMinute(span, minute) {
    if (span.startMinute <= span.endMinute) {
      return minute >= span.startMinute && minute <= span.endMinute;
    }
    return minute >= span.startMinute || minute <= span.endMinute;
  }

  function centerMinute(span) {
    const size = span.startMinute <= span.endMinute
      ? span.endMinute - span.startMinute
      : 1440 - span.startMinute + span.endMinute;
    return (span.startMinute + Math.round(size / 2)) % 1440;
  }

  function titleCase(value) {
    return String(value).replace(/-/g, " ").replace(/\b\w/g, (letter) => letter.toUpperCase());
  }

  /*______________________________________ CONSOLE API _______________________________________*/

  function filterScenes(scenes, options = {}) {
    let result = [...scenes];
    if (options.exactOnly) result = result.filter((scene) => scene.precision === "exact");
    if (options.precision) result = result.filter((scene) => scene.precision === options.precision);
    if (options.period) result = result.filter((scene) => scene.period === options.period);
    if (options.time) {
      const minute = timeToMinute(options.time);
      result = result.filter((scene) => coversMinute(scene, minute));
    }
    return result;
  }

  function findScenes(options = {}) {
    const normalized = typeof options === "string" ? { query: options } : options;
    const value = String(normalized.query || "").toLowerCase();
    return filterScenes(state.scenes, normalized).filter((scene) =>
      scene.id.toLowerCase().includes(value) ||
      scene.movieTitle.toLowerCase().includes(value) ||
      scene.movieSlug.toLowerCase().includes(value) ||
      scene.displayTime.includes(value),
    );
  }

  function consolePlay(options = {}) {
    const normalized = typeof options === "string" ? { query: options } : options;
    const scene =
      (normalized.id && state.scenes.find((item) => item.id === normalized.id)) ||
      (Number.isInteger(normalized.index) && filterScenes(state.scenes, normalized)[normalized.index]) ||
      (normalized.query && findScenes(normalized)[0]);

    if (!scene) throw new Error(`No scene found for ${JSON.stringify(normalized)}`);
    return forcePlay(scene, sceneContextDate(scene, normalized));
  }

  function consolePlayAt(hhmm, options = {}) {
    const scene = selectScene(atLocalTime(hhmm), {
      exactOnly: Boolean(options.exactOnly),
      mode: options.mode,
    });
    if (!scene) throw new Error(`No scene found at ${hhmm}`);
    return forcePlay(scene, atLocalTime(hhmm));
  }

  function consolePlayRandom(options = {}) {
    const pool = filterScenes(state.scenes, options);
    if (!pool.length) throw new Error("No scenes available");
    const scene = pool[Math.floor(Math.random() * pool.length)];
    return forcePlay(scene, sceneContextDate(scene, options));
  }

  function replayCurrentScene() {
    if (!state.currentScene || state.isPlayingSequence) return;
    forcePlay(state.currentScene, state.currentSceneDate || sceneContextDate(state.currentScene));
  }

  function forcePlay(scene, contextDate = sceneContextDate(scene)) {
    stopPlayback({ showIdle: false });
    enterPlaybackMode();
    playSequence(scene, contextDate);
    return scene;
  }

  function apiHelp() {
    return {
      now: "ReelTime.now({ mode: 'arrival' | 'ongoing', exactOnly: true })",
      scenes: "ReelTime.scenes({ exactOnly, precision, period, time })",
      find: "ReelTime.find({ query, precision, time })",
      at: "ReelTime.at('08:30', { mode, exactOnly })",
      next: "ReelTime.next({ mode: 'ongoing', exactOnly })",
      play: "ReelTime.play({ id | query | index })",
      playAt: "ReelTime.playAt('08:30', { mode, exactOnly })",
      random: "ReelTime.random({ precision, exactOnly })",
      stop: "ReelTime.stop()",
      timeFormat: "ReelTime.timeFormat()",
      setTimeFormat: "ReelTime.setTimeFormat('auto' | '12' | '24')",
    };
  }

  function installConsoleApi() {
    window.ReelTime = {
      help: () => apiHelp(),
      state,
      now: (options = {}) => nowReport(options),
      current: () => sceneSnapshot(state.currentScene),
      scenes: (options = {}) => filterScenes(state.scenes, options),
      find: (options = {}) => findScenes(options),
      at: (hhmm, options = {}) => selectScene(atLocalTime(hhmm), {
        exactOnly: Boolean(options.exactOnly),
        mode: options.mode,
      }),
      next: (options = {}) => nextReport({
        exactOnly: Boolean(options.exactOnly),
        mode: options.mode || "ongoing",
      }),
      nextExact: () => nextReport({ exactOnly: true }),
      play: (options = {}) => consolePlay(options),
      playAt: (hhmm, options = {}) => consolePlayAt(hhmm, options),
      random: (options = {}) => consolePlayRandom(options),
      stop: () => stopPlayback(),
      timeFormat: () => timeFormatReport(),
      setTimeFormat: (mode = "auto") => setTimeFormatPreference(mode),
      audio: {
        beep: () => playCountdownBeep(),
        projectorStart: () => startProjectorSound(),
        projectorStop: () => fadeOutProjectorSound(),
      },
    };
  }

  /*__________________________________ REEL TIME HELPERS __________________________________*/

  function sceneContextDate(scene, options = {}) {
    if (options.time) return atLocalTime(options.time);

    const now = new Date();
    const currentMinute = now.getHours() * 60 + now.getMinutes();
    if (coversMinute(scene, currentMinute)) return now;

    return atLocalMinute(scene.spans[0].startMinute);
  }

  function atLocalMinute(minute) {
    const date = new Date();
    date.setHours(Math.floor(minute / 60), minute % 60, 0, 0);
    return date;
  }

  function atLocalTime(hhmm) {
    const [hour, minute] = parseTime(hhmm);
    const date = new Date();
    date.setHours(hour, minute, 0, 0);
    return date;
  }

  function timeToMinute(hhmm) {
    const [hour, minute] = parseTime(hhmm);
    return hour * 60 + minute;
  }

  function parseTime(hhmm) {
    const match = String(hhmm).match(/^(\d{1,2}):(\d{2})$/);
    if (!match) throw new Error("Expected time in HH:MM format");
    return [Number(match[1]), Number(match[2])];
  }

  function toMinuteOfDay(value) {
    const [hour, minute] = value.split(":").map(Number);
    return hour * 60 + minute;
  }

  function clamp(value, min, max) {
    return Math.min(max, Math.max(min, value));
  }

  function formatClockTime(date) {
    return TIME_FORMATS.clock.format(date);
  }

  function formatSceneTime(value) {
    const [hour, minute] = parseTime(value);
    return formatMinuteAsSceneTime(hour * 60 + minute);
  }

  function formatMinuteAsSceneTime(minute) {
    const value = ((minute % 1440) + 1440) % 1440;
    return TIME_FORMATS.scene.format(new Date(2000, 0, 1, Math.floor(value / 60), value % 60));
  }

  function createTimeFormatters() {
    const hour12 = shouldUse12HourTime();
    return {
      mode: storedTimeFormatPreference(),
      hour12,
      clock: new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit", second: "2-digit", hour12 }),
      scene: new Intl.DateTimeFormat(undefined, { hour: "numeric", minute: "2-digit", hour12 }),
    };
  }

  function shouldUse12HourTime() {
    const preference = storedTimeFormatPreference();
    if (preference === "12") return true;
    if (preference === "24") return false;

    const resolved = new Intl.DateTimeFormat(undefined, { hour: "numeric" }).resolvedOptions();
    if (resolved.hourCycle === "h23" || resolved.hourCycle === "h24") return false;
    if (resolved.hourCycle === "h11" || resolved.hourCycle === "h12") return !isLikely24HourRegion();

    return !formatLooks24Hour(new Intl.DateTimeFormat(undefined, { hour: "numeric" }));
  }

  function isLikely24HourRegion() {
    const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
    if (/^(Europe|Africa|Asia)\//.test(timeZone)) return true;
    const languages = navigator.languages?.length ? navigator.languages : [navigator.language || ""];
    return languages.some((language) => !/\b(en-US|en-CA|en-PH)\b/i.test(language));
  }

  function formatLooks24Hour(formatter) {
    return /\b13\b/.test(formatter.format(new Date(2000, 0, 1, 13, 0, 0)));
  }

  function storedTimeFormatPreference() {
    try {
      const value = window.localStorage.getItem(TIME_FORMAT_KEY);
      return ["auto", "12", "24"].includes(value) ? value : "auto";
    } catch {
      return "auto";
    }
  }

  function setTimeFormatPreference(mode = "auto") {
    if (!["auto", "12", "24"].includes(mode)) throw new Error("Expected 'auto', '12', or '24'");
    try {
      if (mode === "auto") window.localStorage.removeItem(TIME_FORMAT_KEY);
      else window.localStorage.setItem(TIME_FORMAT_KEY, mode);
    } catch {
      // Ignore storage failures; the current page can still update its formatter.
    }
    Object.assign(TIME_FORMATS, createTimeFormatters());
    state.renderedLocalTime = "";
    state.renderedNextTimer = "";
    updateClockFace();
    return timeFormatReport();
  }

  function timeFormatReport() {
    return {
      mode: TIME_FORMATS.mode,
      hour12: TIME_FORMATS.hour12,
      sample: TIME_FORMATS.clock.format(new Date(2000, 0, 1, 13, 5, 9)),
      timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone,
      languages: navigator.languages?.length ? [...navigator.languages] : [navigator.language],
    };
  }

  function minuteToTime(minute) {
    const value = ((minute % 1440) + 1440) % 1440;
    return `${pad2(Math.floor(value / 60))}:${pad2(value % 60)}`;
  }

  function formatDuration(ms) {
    const total = Math.ceil(ms / 1000);
    const minutes = Math.floor(total / 60);
    const seconds = total % 60;
    return `${pad2(minutes)}:${pad2(seconds)}`;
  }

  function prefersReducedMotion() {
    return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  }

  function shuffle(items) {
    const copy = [...items];
    for (let index = copy.length - 1; index > 0; index -= 1) {
      const swapIndex = Math.floor(Math.random() * (index + 1));
      [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
    }
    return copy;
  }

  function randomItem(items) {
    return items[Math.floor(Math.random() * items.length)];
  }

  function pad2(value) {
    return String(value).padStart(2, "0");
  }

  function sleep(ms) {
    return new Promise((resolve) => {
      const timer = window.setTimeout(resolve, ms);
      state.timers.push(timer);
    });
  }

  function clearManagedTimers() {
    for (const timer of state.timers) window.clearTimeout(timer);
    state.timers = [];
  }

})();
