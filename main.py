from optimizer import optimize_lineup
from espn_client import get_roster
from config import league_id, year, espn_s2, swid, my_team_id
from projections import score_projection



def main():

    roster = get_roster(league_id, year, espn_s2, swid, my_team_id)

    roster_projections = score_projection(roster)



    best_starters, bench, out, warnings = optimize_lineup(roster_projections)

    for slot in best_starters:
        if slot["player"] is None:
            print(slot["slot"]+":", "No eligible player")
        elif slot["player"]["flag"]:
            print(slot["slot"]+":", slot["player"]["name"], slot["player"]["projection"], slot["player"]["reason"])
        else:
            print(slot["slot"]+":", slot["player"]["name"], slot["player"]["projection"])

    for player in bench:
        print("Bench:",player["name"], player["projection"])

    for player in out:
        print("Inactive:", player["name"], player["reason"])

    for issue in warnings:
        print(issue)



if __name__ == "__main__":
    main()