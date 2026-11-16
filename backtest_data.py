from config import  load_config
from espn_client import get_league
from pathlib import Path
import json



OFFENSE = {"QB", "RB", "WR", "TE"}


# Grab each players data from a specific week
def week_rows(league, week):
    rows = []

    for matchup in league.box_scores(week=week):
        for player in matchup.home_lineup + matchup.away_lineup:
            if player.position not in OFFENSE:
                continue
            
            row = {
                "season": league.year,
                "week": week,
                "player_id": player.playerId,
                "name": player.name,
                "position": player.position,
                "projected": player.projected_points,
                "actual": player.points,
                "slot": player.slot_position,
                "fantasy_team": player.onTeamId,
                "nfl_team": player.proTeam,
                "opponent": player.pro_opponent,
                "on_bye": player.on_bye_week,
                "injury_status": player.injuryStatus,
                "game_played": player.game_played
            }

            rows.append(row)

    return rows




# Grab each players data from the season

def season_rows(league):
    all_rows = []
    
    for week in range(1, league.current_week):
        rows = week_rows(league, week)
        all_rows.extend(rows)


    return all_rows
        


# Read season data from file if current, or fetch and create from espn
def load_season_rows(league, force_refresh=False):
    last_week = league.current_week - 1
    p = Path(f"data/cache/offense_{league.year}_thru_wk{last_week}.json")

    if p.exists() and not force_refresh:
        with open(p, "r", encoding="utf-8") as file:
            rows = json.load(file)
        print("Loaded from cache")
        return rows

    else:
        print("Fetching from espn")  
        rows = season_rows(league)
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, "w", encoding="utf-8") as file:
            json.dump(rows, file, indent=4)
          
        return rows



# Mean Absolute Error
def mae(rows):
    if not rows:
        raise ValueError("mae() got no rows. Check the pool filter.")
    
    total = 0
    for row in rows:
        total += abs(row["projected"] - row["actual"])
    return total / len(rows)


# positive number means the projections are to high, negative means projects are too low
def bias(rows):
    if not rows:
        raise ValueError("bias() got no rows. Check the pool filter.")
    
    total = 0
    for row in rows:
        total += row["projected"] - row["actual"]
    return total / len(rows)
    



def backtest_pool(rows, position,top_n=24):
    by_week = {}
    result = []
   
    for row in rows:
        if row["on_bye"] or row["position"] != position:
            continue

        if row["week"] not in by_week:
            by_week[row["week"]] = []

        by_week[row["week"]].append(row)

    for week in by_week:    
        by_week[week].sort(key=lambda x: x["projected"], reverse=True)
        top = by_week[week][:top_n]
        result.extend(top)


    return result


def get_mae_and_bias(rows):
    positions = {
        "QB": 12, 
        "RB": 24,
        "WR": 30,
        "TE": 12
        }

    results = {}

    for position in positions:
        pool = backtest_pool(rows, position, top_n=positions[position])
        mae_results = mae(pool)
        bias_result = bias(pool)

        results[position] = {"mae": round(mae_results, 2), "bias": round(bias_result, 2)}

    return results



if __name__ == "__main__":
    config = load_config()
    league = get_league(config)
    rows = load_season_rows(league)
    print(get_mae_and_bias(rows))