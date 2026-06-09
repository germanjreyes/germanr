# Copy-paste prompt for local Claude Code

Paste everything in the fenced block below into Claude Code running on your PC,
from inside the `germanr` repo on branch
`claude/performance-decline-data-search-xwe3lh`.

---

```
You are helping with an economics research project. Read
research/performance-decline-anticipation/PLAN.md in this repo first — it has
the full context. Short version below so you can act without me re-explaining.

## Project
Title: "Performance Declines and the Misallocation of High-Value Work."
Authors: Carl Meyer, Germán Reyes, Jason Somerville. It extends Germán's
"Cognitive Endurance" paper (papers/reyes_endurance.pdf), which shows that
test-takers' performance declines over an exam AND that they don't anticipate
this fade, so they misallocate effort. We now want to show the same two facts
in OTHER settings (not test-takers).

## What every dataset must deliver
- C1 OBJECTIVE PERFORMANCE: a measured (not self-reported) quality/error
  signal — e.g. chess blunder / centipawn loss, a wrong-answer verdict.
- C2 TIMESTAMPS: each performance observation is time-stamped, so we can place
  it on a within-day clock (time-of-day) AND a within-session clock
  (minutes/units into the bout).
- C3 ANTICIPATION HANDLE: a forward-looking effort/time-allocation choice we
  can observe, to test whether people planned for the fade. Bonus if we can
  flag HIGH-VALUE vs routine work (the title), e.g. chess endgames or the
  hardest contest problems.

## Environment note
A previous (sandboxed) session could NOT reach the internet, so the datasets
below were only cataloged, never downloaded. YOU are on my real machine with
network access — so your job is to actually pull them.

## Tasks, in order

### 0. Setup
- Create a Python env and install: pandas, numpy, matplotlib, requests
  (and pyarrow). Put all new work under
  research/performance-decline-anticipation/ in subfolders: data/ (gitignored,
  raw pulls), code/, output/. Add a .gitignore so we never commit multi-GB raw
  data — commit code, small derived CSVs, and figures only.

### 1. Codeforces (do this FIRST — easiest, clean JSON API)
- Use the official API (https://codeforces.com/apiHelp). Key endpoints:
  user.status (a user's submissions), contest.standings, problemset.problems,
  user.rated to enumerate users. Each submission has creationTimeSeconds (UTC)
  and a verdict (OK / WRONG_ANSWER / RUNTIME_ERROR / TIME_LIMIT_EXCEEDED / ...).
  User profiles have a country (user.info) -> use it to convert UTC to local
  hour of day. Respect rate limits (~1 request / 2 sec); cache to data/.
- There is also an open bulk dump (~17.6M submissions to end-2024, see the
  Codeforces blog) if the API is too slow — find it and prefer it for scale.
- Build a tidy submission-level dataframe: user, country, local_hour,
  contest_id, problem_index, verdict, minutes_into_contest, attempt_number.
- DELIVERABLES:
  (a) wrong-answer rate vs local hour-of-day (the within-day decline);
  (b) wrong-answer rate vs minutes-into-contest (the within-session decline);
  (c) split (b) by problem difficulty so we can see whether HIGH-VALUE (hard)
      problems are attempted in fatigued late windows;
  (d) a first-pass anticipation cut: per contestant, the order they attack
      problems and time budgeted per problem.
  Save figures to output/ and a short markdown note interpreting them.

### 2. Lichess (heavier — engine-scored chess)
- Two access paths; pick based on scale you need:
  - REST API for targeted per-player history:
    https://lichess.org/api/games/user/{username}?evals=true&clocks=true&pgnInJson=true
    (NDJSON; gives per-move evals + clocks + UTC start). Good for a few
    thousand active players.
  - Bulk monthly PGN dumps from https://database.lichess.org/ for scale
    (tens of GB; ~6% have computer eval; most rapid/classical have clocks).
    Stream-parse, don't load whole file in memory; use python-chess.
- Performance measures (C1): per-move centipawn loss and blunder/mistake/
  inaccuracy flags from the eval. Session/time (C2): game UTC start (->local
  hour via player profile country) and per-move clocks; order a player's games
  within a day to build a "games-into-session" clock.
- DELIVERABLES:
  (a) blunder rate vs local hour-of-day;
  (b) blunder rate vs game-number-within-a-day-session (does playing more
      games back-to-back / late at night raise blunders?);
  (c) HIGH-VALUE cut: blunder rate by game phase (opening/middlegame/endgame)
      — endgames are the highest-leverage, most fatigue-sensitive decisions;
  (d) anticipation cut: do players bank clock for later phases, or burn it
      early and then have to make fatigued endgame moves while also low on
      time? Plot clock-remaining at the start of the endgame vs session length.
  Save figures + a short interpretation note.

### 3. (Optional, if time) Umpires via pybaseball/Statcast
- Pull pitch-level Statcast data (pybaseball). C1 = call correct vs tracked
  location; C2 = pitch timestamp + pitch-count-in-game. Plot miscall rate vs
  pitch count. This is a clean DECLINE replication only (no anticipation).

## Working style
- Make each dataset reproducible from a single script (params at top: sample
  size, date range). Print row counts and a few sanity checks.
- Keep raw data out of git; commit code + small derived CSVs + figures.
- After each dataset, give me a 3-line readout: did performance decline, how
  big, and what the anticipation cut suggests.
- Commit to branch claude/performance-decline-data-search-xwe3lh with clear
  messages. Do NOT open a pull request unless I ask.
- If an API/license blocks bulk use, tell me instead of scraping around it.
```

---

*Generated to hand this work off from the web sandbox (no network) to local
Claude Code (has network). See PLAN.md for the full dataset catalog and
rationale.*
