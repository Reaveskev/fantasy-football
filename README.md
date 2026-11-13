# Fantasy Football Lineup Optimizer

A Python tool that connects to an ESPN fantasy football league and picks the best starting lineup for the current week, using ESPN's weekly projections.

**Status:** v1 (start/sit). Built as a personal project for my own league; more features are on the roadmap below.

## Features

- Pulls your roster and this week's projections from your ESPN league (private leagues supported)
- Fills lineup slots in order (QB, RB, RB, WR, WR, TE, then FLEX) with the highest-projected eligible player
- Treats players on bye, OUT, or on injured reserve as 0 points so they're never started
- Flags players with any other designation (e.g. Questionable) so you can check them before kickoff
- Leaves a slot empty, with a warning, rather than starting someone who isn't playing
- Lists bench and inactive players with the reason they're inactive

## Requirements

- Python 3.10+
- An ESPN fantasy football league you belong to

## Setup

```bash
git clone <this-repo-url>
cd fantasy-football

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install espn_api nflreadpy python-dotenv
```

## Configuration

Create a `.env` file in the project root:

```
LEAGUE_ID=your_league_id
ESPN_S2=your_espn_s2_cookie
SWID={your-swid-cookie}
SEASON=2026
TEAM_ID=your_team_id
```

| Key               | Where to find it                                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------------------------ |
| `LEAGUE_ID`       | In your ESPN league page URL: `leagueId=...`                                                                 |
| `TEAM_ID`         | In your team page URL: `teamId=...`                                                                          |
| `ESPN_S2`, `SWID` | Browser cookies. Log in to ESPN, open dev tools → Application → Cookies → espn.com. Keep SWID's curly braces |
| `SEASON`          | The year the NFL season started (e.g. `2026` for the 2026–27 season)                                         |

`.env` is listed in `.gitignore`. Your ESPN cookies work like a password, so never commit them.

## Usage

```bash
python explore.py
```

Run it before the week's games start; once games kick off, projections are replaced by live scores.

## Sample Output

```
QB: Drake Maye 21.95
RB: Chuba Hubbard 20.01
RB: Derrick Henry 18.19
WR: Amon-Ra St. Brown 20.35
WR: Matthew Golden 17.22
TE: Sam LaPorta 11.44
FLEX: Bhayshul Tuten 17.26
Bench: Patrick Mahomes 17.52
Bench: DJ Moore 13.34
Bench: Germie Bernard 10.93
Bench: Rachaad White 10.85
Bench: Keenan Allen 8.69
Bench: Jordyn Tyson 8.59
Inactive: Puka Nacua INJURY_RESERVE
Inactive: Jonah Coleman Player on BYE
```

## Limitations

- Assumes a plain PPR league with a QB / RB / RB / WR / WR / TE / FLEX lineup
- Kickers and defenses are excluded
- Uses ESPN's unofficial API, which can change without notice
- v1 uses ESPN's own projections, so its lineup should match ESPN's

## Roadmap

1. **v2: Better projections.** My own projection: blend ESPN's projection with season average, then add opponent strength, recent-game weighting, usage stats, and betting lines.
2. **v3: Trades.** A trade grader based on rest-of-season value.
3. **v4: Draft tools.** Combined rankings that show how much experts disagree on each player, plus a live draft tracker.
