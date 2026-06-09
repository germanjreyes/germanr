"""
Proof-of-concept: objective performance declines over the working day/session
in settings OTHER than test-taking.

IMPORTANT — this figure is a *calibrated illustration*, not a fresh data pull.
The sandbox that produced it blocks outbound network from the shell, so the
series below are reconstructed from the point estimates reported in the cited
studies and normalized to (first hour = 100) so different settings are
comparable on one axis. Replace each series with a live pull (Lichess /
Codeforces / EHR) when running where those hosts are reachable; see ../PLAN.md.

Sources for the calibration points:
- Physician antibiotic prescribing (decision fatigue, *inappropriate* care
  rises => "appropriate-care index" falls within each 4-hour session, resets
  after lunch): Linder et al. 2014, JAMA Internal Medicine. Baseline ~44%
  prescribing rising ~5 pp across a session.
- Colonoscopy adenoma detection rate (ADR) by time of day: ~29.3% (AM) ->
  ~25.3% (PM); ~7% relative drop by end of day (multi-site, PMC6715419;
  Sanaka et al.).
- Online-chess engine blunder rate rising with time-on-task / late hours
  (shape from Antiochian 68M-game Lichess analysis & Kuenn-Palacios-Pestel
  engine-blunder method) -> "accuracy index" falls.
- College-exam (ENEM) within-test performance decline -> the project's own
  anchor (Reyes 2026): performance on a given question falls with its position.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Series 1: Physician decision fatigue (Linder 2014) -- "appropriate care" index
# Two 4-hour sessions with a lunch reset (the characteristic sawtooth).
# Inappropriate antibiotic prescribing rises ~5 pp over each session; we plot
# 100 - (excess inappropriate), i.e. a quality index that fades then resets.
hours = np.arange(0, 8)  # clinic hours into the day (0-3 AM session, 4-7 PM)
appropriate = np.array([100, 98, 96, 94,  # morning fade
                        100, 98, 96, 94])  # reset after lunch, fade again

# Series 2: Colonoscopy ADR by hour into the day (monotone fade, no reset).
adr_hours = np.arange(0, 8)
adr_index = np.array([100, 98, 96, 94, 92, 90, 88, 86])  # 29.3 -> ~25.3%

# Series 3: Online-chess accuracy index vs games-into-a-late-session.
chess_games = np.arange(0, 8)
chess_index = 100 - 1.6 * chess_games  # blunder rate climbs with time-on-task

# Series 4: Exam anchor (Reyes 2026) -- performance vs question position.
exam_pos = np.linspace(0, 8, 9)
exam_index = 100 - 2.0 * exam_pos  # within-test decline (the test-taker result)

# ----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8.6, 5.4))

ax.plot(exam_pos, exam_index, "o-", lw=2.4, color="#1f3a93",
        label="College exam — within-test (Reyes 2026, the anchor)")
ax.plot(hours, appropriate, "s-", lw=2.0, color="#c0392b",
        label="Physician appropriate-care index (Linder 2014, sawtooth)")
ax.plot(adr_hours, adr_index, "^-", lw=2.0, color="#16a085",
        label="Colonoscopy adenoma detection (PMC6715419)")
ax.plot(chess_games, chess_index, "d-", lw=2.0, color="#8e44ad",
        label="Online-chess accuracy vs games into session (Lichess)")

ax.axhline(100, color="grey", lw=0.8, ls=":")
ax.set_xlabel("Time into the working day / session  "
              "(hours, exam questions, or games — each setting's own clock)")
ax.set_ylabel("Objective performance index\n(first hour / start = 100)")
ax.set_title("Performance declines over the day in non-test settings, too\n"
             "(calibrated illustration — see script header for sources)",
             fontsize=11)
ax.set_ylim(80, 103)
ax.legend(fontsize=8.4, loc="lower left", framealpha=0.95)
ax.grid(True, alpha=0.25)

fig.text(0.5, -0.02,
         "Illustrative reconstruction from published point estimates, "
         "normalized to start = 100; not a raw data pull. Replace with live "
         "Lichess / Codeforces / EHR pulls.",
         ha="center", fontsize=7.5, style="italic", color="#555555")

fig.tight_layout()
out = __file__.rsplit("/", 1)[0] + "/performance_over_day.png"
fig.savefig(out, dpi=160, bbox_inches="tight")
print("wrote", out)
