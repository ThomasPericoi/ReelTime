(() => {
  "use strict";

  /*________________________________________ CONFIG ________________________________________*/

  const SELECTORS = {
    app: "#app",
    scene: "#scene",
    startPanel: "#startPanel",
    startButton: "#startButton",
    startMessage: "#startMessage",
    countdown: "#countdown",
    countdownNumber: "#countdownNumber",
    titleCard: "#titleCard",
    idle: "#idle",
    localTime: "#localTime",
    localTimeAmPm: "#localTimeAmPm",
    idleMessage: "#idleMessage",
    movieTitle: "#movieTitle",
    sceneMatch: "#sceneMatch",
    rightsIntro: "#rightsIntro",
    playbackStatus: "#playbackStatus",
    currentCredit: "#currentCredit",
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
  const ONGOING_PRECISIONS = new Set(["exact", ...FLEXIBLE_PRECISIONS]);

  const SOUND_PATHS = {
    countdownBeep: "assets/sounds/countdown_beep.mp3",
    projector: "assets/sounds/projector.mp3",
  };

  const IDLE_MESSAGE = "Waiting for the next scene. Grab some pop-corn.";

  const TIMING = {
    countdownStepMs: 1000,
    titleCardMs: 2200,
    projectorFadeMs: 1800,
    quickFadeMs: 500,
    endLookSeconds: 1.25,
  };

  const VOLUME = {
    countdownBeep: 0.7,
    projector: 0.35,
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
    hasStarted: false,
    isPlayingSequence: false,
    sequenceToken: 0,
    nextCheckAt: null,
    timers: [],
    renderedLocalTime: "",
    renderedLocalTimeAmPm: "",
    renderedNextTimer: "",
    masterVolume: VOLUME.master,
    playedFlexibleSceneIds: new Set(),
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
    el.startButton.addEventListener("click", startClock, { once: true });
    el.replayButton.addEventListener("click", replayCurrentScene);

    try {
      const library = await loadSceneLibrary();
      state.scenes = library.scenes.map(normalizeScene).sort(sortScenes);
      installDebugApi();
      el.startMessage.textContent = "A talking clock made of movie scenes. Press play and let cinema tell you the time.";
      el.startButton.disabled = false;
    } catch {
      el.startMessage.textContent = "Could not load the scene library. Check that assets/data/scenes-data.js is available.";
    }
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

  async function primeFuturePlayback() {
    const now = new Date();
    const scene =
      selectScene(now, { mode: "arrival" }) ||
      selectScene(findNextPlayableTime(now, { mode: "ongoing" }), { mode: "ongoing" });

    if (!scene) return;

    try {
      prepareSceneVideo(scene);
      forceSceneMuted();
      await el.scene.play();
      el.scene.pause();
      el.scene.currentTime = 0;
    } catch {
      // Browsers may refuse deferred media priming; playback has a muted fallback at scene start.
    } finally {
      allowSceneAudio();
      applySceneVolume();
    }
  }

  /*______________________________________ SCHEDULER ______________________________________*/

  async function startClock() {
    applySceneVolume();
    await primeFuturePlayback();
    enterPlaybackMode();
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
    const selected = selectScene(new Date(), { mode });

    if (selected && playImmediately) {
      playSequence(selected);
      return;
    }

    if (selected && selected.id !== state.currentScene?.id) {
      playSequence(selected);
      return;
    }

    state.nextCheckAt = findNextPlayableTime(new Date(), { mode: "ongoing" });
    showIdle(IDLE_MESSAGE);
  }

  /*__________________________________ PLAYBACK SEQUENCE __________________________________*/

  async function playSequence(scene) {
    const token = beginSequence(scene);

    try {
      await showCountdown(token);
      startProjectorSound();
      await showTitleCard(scene, token);
      state.nextCheckAt = findNextPlayableTime(new Date(), { mode: "ongoing" });
      showNextCountdown();
      const didPlay = await playScene(scene, token);
      if (didPlay) {
        settleVideo();
      } else {
        resetVideo();
      }
      setFaviconLetter();
      await fadeOutProjectorSound(TIMING.quickFadeMs);
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

  function beginSequence(scene) {
    state.sequenceToken += 1;
    state.isPlayingSequence = true;
    state.currentScene = scene;
    rememberFlexibleScene(scene);
    clearManagedTimers();
    hideSequenceUi();
    resetVideoUnlessPrimed(scene);
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

  async function showTitleCard(scene, token) {
    if (token !== state.sequenceToken) return;
    setFaviconRecording();
    el.movieTitle.textContent = scene.movieTitle;
    el.sceneMatch.textContent = sceneMatchLine(scene, new Date());
    el.rightsIntro.textContent = creditLine(scene);
    showPanel(el.titleCard);
    await sleep(TIMING.titleCardMs);
    el.titleCard.hidden = true;
  }

  function playScene(scene, token) {
    return new Promise((resolve) => {
      if (token !== state.sequenceToken) {
        resolve(false);
        return;
      }

      hidePanels();
      setCreditOverlay(scene);
      el.scene.classList.remove("gate-hit", "is-ending");
      prepareSceneVideo(scene);
      requestAnimationFrame(() => el.scene.classList.add("gate-hit"));

      el.scene.ontimeupdate = () => updateEndingLook(token);
      el.scene.onended = () => resolve(true);
      el.scene.onerror = () => resolve(false);
      startSceneVideo().then(resolve);
    });
  }

  function prepareSceneVideo(scene) {
    const src = encodeURI(scene.src);
    if (el.scene.getAttribute("src") !== src) {
      el.scene.src = src;
      el.scene.load();
    }
    applySceneVolume();
    allowSceneAudio();
  }

  async function startSceneVideo() {
    try {
      await el.scene.play();
      return true;
    } catch {
      return startSceneVideoMuted();
    }
  }

  async function startSceneVideoMuted() {
    try {
      forceSceneMuted();
      await el.scene.play();
      window.setTimeout(tryRestoreSceneAudio, 250);
      return true;
    } catch {
      return false;
    }
  }

  function forceSceneMuted() {
    el.scene.defaultMuted = true;
    el.scene.muted = true;
    el.scene.setAttribute("muted", "");
  }

  function allowSceneAudio() {
    el.scene.defaultMuted = false;
    el.scene.muted = false;
    el.scene.removeAttribute("muted");
  }

  function tryRestoreSceneAudio() {
    allowSceneAudio();
    applySceneVolume();

    if (el.scene.paused && !el.scene.ended) {
      forceSceneMuted();
      el.scene.play().catch(() => { });
    }
  }

  function updateEndingLook(token) {
    if (token !== state.sequenceToken || !Number.isFinite(el.scene.duration)) return;
    const remaining = el.scene.duration - el.scene.currentTime;
    el.scene.classList.toggle("is-ending", remaining <= TIMING.endLookSeconds);
  }

  /*____________________________________ SCENE MATCHING ____________________________________*/

  function selectScene(date, options = {}) {
    const minute = date.getHours() * 60 + date.getMinutes();
    return state.scenes.find((scene) => isPlayableScene(scene, minute, options)) || null;
  }

  function isPlayableScene(scene, minute, options) {
    if (!coversMinute(scene, minute)) return false;
    if (scene.id === options.excludeSceneId) return false;
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
    const beep = new Audio(SOUND_PATHS.countdownBeep);
    beep.volume = scaledVolume(VOLUME.countdownBeep);
    beep.play().catch(() => { });
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

  function stopPlayback() {
    state.sequenceToken += 1;
    clearManagedTimers();
    fadeOutProjectorSound(TIMING.quickFadeMs);
    resetVideo();
    state.isPlayingSequence = false;
    restoreRoomLight();
    hidePanels();
    setFaviconLetter();
    showIdle(IDLE_MESSAGE);
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

  function resetVideoUnlessPrimed(scene) {
    if (el.scene.getAttribute("src") !== encodeURI(scene.src)) {
      resetVideo();
      return;
    }

    el.scene.pause();
    el.scene.currentTime = 0;
    el.app.classList.remove("has-freeze-frame");
    el.scene.classList.remove("gate-hit", "is-ending");
    clearSceneHandlers();
  }

  function resetVideo() {
    el.scene.pause();
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
    el.idleMessage.textContent = message;
    el.idle.hidden = false;
    if (state.hasStarted) {
      showPlaybackStatus();
      showNextCountdown();
    }
  }

  function setCreditOverlay(scene) {
    showPlaybackStatus();
    el.currentCredit.hidden = false;
    el.overlayMovie.textContent = scene.movieTitle;
    el.overlayRights.textContent = creditLine(scene);
  }

  function clearCreditOverlay() {
    el.currentCredit.hidden = true;
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
    renderText(el.localTimeAmPm, "renderedLocalTimeAmPm", formatClockTimeAmPm(now));

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
    if (scene.precision === "fallback") return "Local time: Lost track of time";
    if (scene.precision === "broad") return `Local time: ${scene.displayTime}`;

    const span = matchingSpan(scene, date) || scene.spans[0];
    const target = sceneTargetTime(scene, span);
    const labels = {
      exact: "Exactly",
      before: "Before",
      after: "After",
      approx: "Approximately",
      range: "Around",
    };

    return `Local time: ${labels[scene.precision] || titleCase(scene.precision)} ${target}`;
  }

  function matchingSpan(scene, date) {
    const minute = date.getHours() * 60 + date.getMinutes();
    return scene.spans.find((span) => coversSpanMinute(span, minute));
  }

  function sceneTargetTime(scene, span) {
    if (!span) return scene.displayTime;
    if (scene.precision === "before") return span.end;
    if (scene.precision === "after") return span.start;
    if (scene.precision === "approx" || scene.precision === "range") return minuteToTime(centerMinute(span));
    return span.start;
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
    if (options.wideOnly) result = result.filter((scene) => scene.precision !== "exact");
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

  function debugPlay(options = {}) {
    const normalized = typeof options === "string" ? { query: options } : options;
    const scene =
      (normalized.id && state.scenes.find((item) => item.id === normalized.id)) ||
      (Number.isInteger(normalized.index) && filterScenes(state.scenes, normalized)[normalized.index]) ||
      (normalized.query && findScenes(normalized)[0]);

    if (!scene) throw new Error(`No scene found for ${JSON.stringify(normalized)}`);
    return forcePlay(scene);
  }

  function debugPlayAt(hhmm, options = {}) {
    const scene = selectScene(atLocalTime(hhmm), {
      exactOnly: Boolean(options.exactOnly),
      mode: options.mode,
    });
    if (!scene) throw new Error(`No scene found at ${hhmm}`);
    return forcePlay(scene);
  }

  function debugPlayRandom(options = {}) {
    const pool = filterScenes(state.scenes, options);
    if (!pool.length) throw new Error("No scenes available");
    return forcePlay(pool[Math.floor(Math.random() * pool.length)]);
  }

  function replayCurrentScene() {
    if (!state.currentScene || state.isPlayingSequence) return;
    forcePlay(state.currentScene);
  }

  function forcePlay(scene) {
    stopPlayback();
    enterPlaybackMode();
    playSequence(scene);
    return scene;
  }

  function apiHelp() {
    return {
      now: "ReelTime.now({ mode: 'arrival' | 'ongoing', exactOnly: true })",
      scenes: "ReelTime.scenes({ exactOnly, wideOnly, precision, period, time })",
      find: "ReelTime.find({ query, precision, time })",
      at: "ReelTime.at('08:30', { mode, exactOnly })",
      next: "ReelTime.next({ mode: 'ongoing', exactOnly })",
      play: "ReelTime.play({ id | query | index })",
      playAt: "ReelTime.playAt('08:30', { mode, exactOnly })",
      random: "ReelTime.random({ precision, exactOnly })",
      stop: "ReelTime.stop()",
    };
  }

  function installDebugApi() {
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
      play: (options = {}) => debugPlay(options),
      playAt: (hhmm, options = {}) => debugPlayAt(hhmm, options),
      random: (options = {}) => debugPlayRandom(options),
      stop: () => stopPlayback(),
      audio: {
        beep: () => playCountdownBeep(),
        projectorStart: () => startProjectorSound(),
        projectorStop: () => fadeOutProjectorSound(),
      },
    };
  }

  /*__________________________________ REEL TIME HELPERS __________________________________*/

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
    return `${pad2(date.getHours())}:${pad2(date.getMinutes())}:${pad2(date.getSeconds())}`;
  }

  function formatClockTimeAmPm(date) {
    const hour = date.getHours();
    const meridiem = hour >= 12 ? "PM" : "AM";
    const hour12 = hour % 12 || 12;
    return `${hour12}:${pad2(date.getMinutes())}:${pad2(date.getSeconds())} ${meridiem}`;
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
