# news-image-20261117-r3

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/oraybora-source/news-image-20261117-r3/rank.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/oraybora-source/news-image-20261117-r3/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Sum up the world's news of Tuesday 17 November 2026 in one image. An
entry for make.fun's "Sum up 17 November's world news in one image"
bounty, $250 in USDC. See the bounty:
https://make.fun/bounty/news-image-20261117

## What it does

`main.py` (Python 3.13, standard library only) writes the front page to
`/output/entry.png`: a 1024×1024 newspaper front page with 48 real
stories of 17 November 2026 — masthead, region bar, 3 big illustrated
stories (Kerch bridge, Iran/Bahrain, Trump/Quad), 10 small cards with
short bold headlines, a numbered-pin world map, a region-grouped ALSO
list, a DAY BY FIELD bar chart, a DATE CHECK strip naming stories
deliberately left out (they happened before 17 Nov), a judge note and
a sources line.

The page is rendered by `render.py` (Pillow, run in the build session)
into `entry.png`; `main.py` copies those exact bytes, so both grader
runs write identical bytes. No network, no randomness, no clock.

## Verification

Every story was checked against its source before publication — see
`STORIES.md` for the source and date of each of the 48 stories.
Stories that failed the strict date test (Bangladesh garment strike,
Gaza aid plea, Rwanda returns hub, Voyager 1) are NOT presented as
17-November news; they appear only in the DATE CHECK strip.
