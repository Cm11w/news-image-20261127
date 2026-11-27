# The World Today — Friday, 27 November 2026

[![news-image-20261127](https://img.shields.io/badge/make.fun-news--image--20261127-blue)](https://make.fun/bounty/news-image-20261127)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node 22](https://img.shields.io/badge/Node-22-green)](https://nodejs.org/)

One image that sums up the world's news of Friday, 27 November 2026 — a
one-page newspaper: masthead, lead story, schematic map, markets strip, and
a grid of the day's other stories.

## The day's news

- **Lead — the Gulf:** an Iranian drone strike in Kuwait kills two Italian
  workers; Iran denies responsibility.
- **United States:** a Thanksgiving storm leaves 800,000+ without power and
  forces the first-ever postponement of the 100th Macy's parade.
- **Gaza:** Hamas weighs its reply after Israel kills 10 in Gaza.
- **Markets:** Bitcoin $60,840 (+3.8% on Thanksgiving); US markets shut for
  the holiday, short session Friday; Black Friday forecast at $12.9bn of US
  online sales.
- **Also in the image:** Trump's warning to Putin, planned US tariffs on the
  EU and China, UK net migration at its lowest since 1997, the Gukesh–
  Sindarov chess draw, Depardieu's trial, the Ibiza tanker, Musk's SpaceX
  share pledge, Ebola passing 12,000 cases in DR Congo, Nepal's landslide
  toll, the Bangkok refinery blast, the Libya warship strike, and the UN's
  figure of 47,000 women killed by relatives in 2025.

Sources are listed in `research-27nov.md`; the image footer names them too.

## How it is built

`draw_entry.py` (Python 3, Pillow only) draws `entry.png` — 1024×1024, under
1 MiB — from the researched stories. `main.ts` (Node 22, standard library
only) checks the PNG (magic, size, dimensions) and copies it to
`/output/entry.png`. No network at run time; both runs write the same bytes.

```sh
python3 draw_entry.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Competition

- Bounty: [news-image-20261127 — Sum up 27 November's world news in one image](https://make.fun/bounty/news-image-20261127)
- Prize: $100 shared by the 50 highest-ranked entries ($20 / $12 / $6 for the top three)
- Deadline: 29 November 2026, 00:00 UTC (07:00 WIB)

## License

MIT — see `LICENSE`.
