# Finding "Other Settings" for the Unanticipated-Fatigue Project

**Project:** *Performance Declines and the Misallocation of High-Value Work*
**Authors:** Carl Meyer, Germán Reyes, and Jason Somerville
**Builds on:** the *Cognitive Endurance* agenda (`papers/reyes_endurance.pdf`),
extending it beyond test-takers.
**Prepared:** 2026-06-09 · branch `claude/performance-decline-data-search-xwe3lh`

> **Framing note (from the title).** "Misallocation of **high-value** work" is
> sharper than generic effort misallocation: the cost of the unanticipated
> fade is largest when the *most consequential* task lands in a fatigued slot.
> So the screen below should up-weight settings where (a) we can tag which
> units of work are high-stakes and (b) we can see whether high-stakes work
> gets scheduled into — or pushed out of — the fatigued window. The
> physician sawtooth (a viral-vs-bacterial call placed late in the session),
> chess endgames (the highest-leverage, most fatigue-sensitive decisions), and
> contest problem-ordering all let us separate *high-value* from routine work.

---

## 1. What we are looking for (the screen)

The test-taker result has two empirical pieces:

1. **Performance declines within a bout of cognitive work** (the fatigue
   effect — students answer a given question worse when it appears later in
   the exam).
2. **People do not anticipate the decline** — they expect roughly *constant*
   performance, so they mis-allocate effort over time.

To make the broader point with other occupations/settings, a dataset must
clear **three** hurdles. The user named the first two; the third is what
turns a "fatigue" finding into *this* paper's contribution.

| # | Criterion | Operationalization |
|---|-----------|--------------------|
| **C1** | **Objective performance** | A measured-not-self-reported quality/productivity signal: error rate, blunder, defect, accuracy, output. Not satisfaction or a survey. |
| **C2** | **Timestamps** | Each performance observation is time-stamped so we can place it on a within-day / within-session clock and estimate the decline slope. |
| **C3** | **An anticipation handle** | Some forward-looking choice we can observe (or elicit) — how the worker *allocated effort/time* before the decline hit — so we can test whether they planned for the fade. Ideally a "plan vs. realized" gap, or a revealed schedule choice. |

A setting that clears **C1+C2** lets us *replicate the decline* (the easy,
already-well-trodden part). A setting that *also* clears **C3** lets us make
the paper's actual point. We should sort candidates by C3, because C1+C2 are
common and C3 is the binding constraint.

### Why C3 is the real screen — link to theory
The mechanism is **projection bias over one's own effort cost / fatigue**:
when fresh, people underweight how costly effort will feel once fatigued, so
they front-load and leave nothing for later (Kaufmann 2022, *Projection Bias
in Effort Choices*; Loewenstein–O'Donoghue–Rabin 2003). The endurance paper's
"students expect constant performance" is the static version of this. The
ideal new setting gives us a *revealed* allocation decision to point at.

---

## 2. Candidate settings — ranked catalog

Tiered by how well each clears **C3** (the anticipation handle), since C1/C2
are necessary but not sufficient. "Access" = how hard the data is to get.

### Tier A — clears all three, data is gettable (build here first)

#### A1. Online chess (Lichess full game database) ⭐ top pick
- **C1 performance:** per-move quality from an engine — blunder / mistake /
  inaccuracy flags and centipawn loss. Lichess ships engine evaluations for
  analyzed games; the full move list + clocks is in every game.
- **C2 timestamps:** every game has a UTC start time **and** per-move clock
  times, so we get both *time-of-day* and *minutes-into-the-session*.
- **C3 anticipation — this is the gem:** chess is an explicit
  **effort-over-time allocation problem**. The player's *clock usage* is a
  revealed plan: a fatigue-naive player spends time evenly (or front-loads on
  the opening) and then has to make the hardest, most fatigue-sensitive
  endgame decisions while both tired *and* short on time. We can test whether
  players who have been on a long playing session (many games back-to-back,
  or late at night) (a) blunder more — C1/C2 — and (b) fail to bank more
  clock for later, or fail to stop playing — C3. The "should I play one more
  game at 1 a.m.?" decision is a clean misallocation margin.
- **Access:** `database.lichess.org` publishes monthly PGN dumps (tens of GB
  each, billions of games, ~6% with engine eval and most rapid/classical with
  clocks). REST API for targeted pulls (`/api/games/user/{id}` streams a
  player's full history with `evals=true&clocks=true`). Free, open license.
- **Cons:** time-of-day is server UTC; need user country/timezone (partly
  available) to recover *local* time. Engine-evaluated subset is selected.
- **Reference points:** Antiochian's 68M-game Lichess blunder study; van
  Harreveld et al. on time pressure & chess errors; Künn–Palacios–Pestel on
  air-quality and chess error rates (same engine-blunder methodology — a
  direct template for our C1 measure).

#### A2. Competitive programming (Codeforces) ⭐ strong, very clean data
- **C1 performance:** submission **verdict** (Accepted vs Wrong-Answer /
  Runtime-Error / TLE) = an objective coding-mistake measure, and number of
  failed attempts before solving.
- **C2 timestamps:** `creationTimeSeconds` on every submission (UTC).
- **C3 anticipation:** contests are **fixed-length effort-allocation games**
  (e.g., 2 h, 5–8 problems). Order in which a contestant attacks problems,
  time spent per problem, and whether they keep submitting buggy code late in
  the contest reveal their plan. Test: do solvers who are deep into a long
  session (or contests held late local night) make more late-window errors,
  and did they budget for it?
- **Access:** **open, official** — the Codeforces API (`user.status`,
  `contest.standings`) plus a published full dump (~17.6M submissions to
  end-2024; another ~98M-submission dump). Per-user country is on profiles →
  recover local time of day.
- **Cons:** population is self-selected expert hobbyists; "performance" is
  contest-shaped, not a job.

### Tier B — clears C1+C2 cleanly, C3 is observable-but-indirect (great for replicating the decline; anticipation needs a design)

#### B1. Physician decision fatigue (prescribing / screening over the clinic session)
- **C1:** *inappropriate* care as the day wears on — antibiotic prescribing
  for viral ARIs rises (Linder et al. 2014), opioid prescribing for low-back
  pain rises (OR ≈ 1.6, 4th vs 1st hour; Philpot et al. 2018), cancer-
  screening orders fall (Hsiang et al. 2019). All objective from EHR.
- **C2:** appointment time-stamped to the clinic hour; classic **sawtooth**
  that resets after the lunch break — a beautiful within-session signature.
- **C3 angle:** schedulers/patients choose appointment slots; do late-slot
  patients (or the clinic) anticipate the quality fade? A panel-scheduling
  natural experiment is the anticipation test.
- **Access:** mostly proprietary EHR; but several published datasets/replication
  packages exist, and the BEACH (Australian GP) data has been used for this.

#### B2. Colonoscopy adenoma detection rate (ADR) by session position
- **C1:** ADR / polyp detection — a hard quality outcome with downstream
  cancer consequences. Falls later in the day (29.3%→25.3% AM vs PM; ~7%
  relative drop and ~20% shorter withdrawal time by end of day in an 86k-scope
  multi-site study).
- **C2:** procedure start time, queue position within shift.
- **C3:** block scheduling — were hard cases mis-scheduled into fatigued slots?
- **Access:** proprietary endoscopy registries; published aggregates usable
  for calibration / a reduced-form replication.

#### B3. Baseball home-plate umpires (ball/strike accuracy)
- **C1:** call correctness vs. the tracked pitch location (Statcast /
  pitch-tracking) — a per-pitch objective error.
- **C2:** every pitch is time-stamped; pitch count within game = fatigue clock.
- **C3:** weaker — umpires don't choose effort allocation. Useful as a clean
  *decline* replication with millions of pitches, free (Baseball Savant /
  `pybaseball`), not as an anticipation setting.

### Tier C — strong C3 (anticipation is the whole point) but performance is physical, not cognitive

#### C1. Marathon / endurance-race pacing ⭐ best *pure* anticipation story
- **C1:** split pace (km/mile) — objective output over time.
- **C2:** chip splits every 5 km; many races + Strava give second-level data.
- **C3 — textbook misallocation:** most recreational runners run **positive
  splits** ("hit the wall" at ~30 km) — they go out at a pace they cannot
  sustain, i.e., they *do not anticipate their own fatigue* and mis-allocate
  effort across the race. Elites who pace it (negative/even splits) are the
  counterfactual. This is almost exactly the paper's thesis in a physical
  domain, with a *plan* (target pace / early pace) vs *realization* gap
  measurable per runner.
- **Access:** public race results with 5 km splits; Strava API; published
  100k-runner datasets.
- **Caveat:** physical fatigue. Frame as a *complementary* domain showing the
  misallocation logic generalizes, not as cognitive endurance.

### Tier D — keep on the radar (good C1/C2, sourcing or C3 harder)
- **Data-entry / transcription / typing platforms** (keystroke logs → speed &
  error by minute-on-task and time-of-day; some open keystroke datasets).
- **Call-center** handle-time & first-call-resolution over shift (proprietary).
- **Fruit/field pickers** — Bandiera–Barankay–Rasul-style per-worker hourly
  productivity (proprietary firm data; the canonical effort-over-day series).
- **Air-traffic / TSA screeners, radiologists** (shift fatigue; access hard).
- **eSports** (LoL/Dota/CS) match logs with fine performance metrics + UTC
  timestamps + long sessions (public APIs) — a chess-like option.
- **Stack Overflow / GitHub commits** late at night → revert/bug rate
  (timestamps public; "mistake" proxy noisier).

---

## 3. Recommendation

**Build the headline result on chess (A1) and Codeforces (A2).** Both are
free, open, individually-timestamped, have an *objective* mistake measure,
and — crucially — are **effort-allocation games**, so C3 is identified from
revealed behavior (clock/ time budgeting and the "play one more game late at
night" margin) without needing a survey. Use **physician decision-fatigue
(B1)** and **marathon pacing (C1)** as the two illustrative "this generalizes"
panels: B1 because it is a high-stakes real occupation with a clean
within-day sawtooth, C1 because positive splits are the most legible
"people don't plan for their own fade" fact in any field.

**Suggested division of labor for the decline vs. anticipation tests:**

| Setting | Decline test (C1/C2) | Anticipation test (C3) |
|--------|----------------------|------------------------|
| Chess | blunder/centipawn-loss vs. game# in session & local hour | time banked for later phases; choice to keep playing while degrading |
| Codeforces | wrong-verdict rate vs. minutes-into-contest & local hour | problem-order & time budget; late-window buggy resubmits |
| Physician | inappropriate Rx/screening vs. clinic hour (sawtooth) | scheduling: are hard cases/patients placed in fatigued slots? |
| Marathon | pace vs. distance (the fade) | early pace as a *plan*; positive-split gap = unanticipated fatigue |

---

## 4. Concrete next steps (pipeline)

1. **Chess MVP (1–2 days of compute):**
   - Pull one month of Lichess analyzed rapid/classical games (or stream a few
     thousand high-activity players via the API with `evals=true&clocks=true`).
   - For each move: engine `eval`, blunder flag, ply, clock; for each game:
     UTC start, player, derive local hour from profile country.
   - Build the *session clock*: order a player's games within a day; estimate
     blunder rate vs. (i) local hour-of-day and (ii) game-number-in-session.
   - **C3:** regress clock-spent-late-in-game and stop/continue decisions on
     accumulated session length.
2. **Codeforces MVP:** pull the open dump; per submission compute wrong-rate by
   minutes-into-contest and by solver's local hour; per contestant recover the
   problem-attack order to proxy the plan.
3. **Decline-replication panels:** assemble the B1/C1 aggregates from published
   estimates (and any open replication packages) for the cross-setting figure.
4. **Anticipation elicitation (optional new data):** a short Prolific/MTurk
   study mirroring the endurance paper's belief elicitation, but for chess
   players / runners: "predict your accuracy in game 1 vs game 6 tonight" →
   compare predicted vs realized fade (direct C3 in a controlled setting).

> **Note on this environment:** the sandbox blocks outbound network from the
> shell (Lichess/Codeforces/PMC return 403 here), so the live pulls above must
> run where the data hosts are reachable. The figure in `figures/` is therefore
> a *calibrated illustration from published estimates*, not a fresh pull —
> see its header for exact sources.

---

## 5. Proof-of-concept figure

`figures/performance_over_day.png` (script: `make_proof_of_concept.py`) plots,
on the **vertical axis, an objective performance index over the working
day/session** for several settings, normalized to the first hour = 100, to
show the user's requested pattern — *performance declines over the course of a
day in non-test settings too*. Every series is reconstructed from the cited
study's reported estimates and is labeled **illustrative / calibrated**, not a
raw data pull (which this sandbox can't do — see note above).

---

## 6. Key references
- Reyes (2026), *Cognitive Endurance, Talent Selection, and the Labor Market
  Returns to Human Capital* (this project's anchor).
- Kaufmann (2022), *Projection Bias in Effort Choices*, **GEB**.
- Loewenstein, O'Donoghue & Rabin (2003), *Projection Bias in Predicting
  Future Utility*, **QJE**.
- Linder et al. (2014), *Time of Day and the Decision to Prescribe Antibiotics*,
  **JAMA Intern. Med.**
- Philpot et al. (2018), *Time of day is associated with opioid prescribing*,
  **J. Gen. Intern. Med.**
- Hsiang et al. (2019), decision fatigue & cancer screening, **JAMA Netw Open**.
- "Adenoma Detection Rate Falls at the End of the Day…", multi-site (PMC6715419).
- Chan et al. / Tetlock-style umpire accuracy; psychophysics of home-plate
  calls (*Sci. Rep.* 2024).
- Künn, Palacios & Pestel — air quality and chess (engine-blunder method).
- Frontiers in Physiology (2025), negative-split marathon pacing review.
- Codeforces open submissions dataset (end-2024); Codeforces API.
- Lichess open database (`database.lichess.org`).
