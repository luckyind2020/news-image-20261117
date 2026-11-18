# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/luckyind2020/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/luckyind2020/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One image summing up Tuesday 17 November 2026's world news, drawn as a newspaper front page: the Kerch Bridge strike, tankers hit at Hormuz, Trump's Asia trip, the EU-Rwanda return hub, Nvidia's first earnings since Huang's exit — plus the day's briefs.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`). Standard library only, no network, fully deterministic — two runs write the same bytes.

## How the image was made

`tools/render.py` draws the front page with Pillow and the DejaVu fonts from the checked news data in `tools/news.py`. Every story was verified against several reports first published on 17 November 2026 (BBC, Reuters, AP, CNBC, Al Jazeera, The Guardian); claims that were not independently verified that day are attributed in the text. Re-render locally with:

```sh
python3 tools/render.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=4ha9jy2z&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
