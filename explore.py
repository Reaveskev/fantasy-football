import os
from dotenv import load_dotenv
from espn_api.football import League


load_dotenv()

league_id = os.getenv("LEAGUE_ID")
espn_s2 = os.getenv("ESPN_S2")
swid = os.getenv("SWID")
year = os.getenv("SEASON")
my_team_id = os.getenv("TEAM_ID")



if league_id is None:
    print("League Id is coming back as None")
    quit()
    
     
if espn_s2 is None:
    print("Espn_2 is coming back as None")
    quit()

if swid is None:
    print("swid is coming back as None")
    quit()

if year is None:
    print("Year is coming back as None")
    quit()
year = int(year)

if my_team_id is None:
    print("Team_id is coming back as None")
    quit()
my_team_id = int(my_team_id)



league = League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)




teams = league.teams

my_team = None


for team in teams:
    if team.team_id == my_team_id:
        my_team = team
        break

if my_team is None:
    print("Did not recieve team information")
    quit()




roster = my_team.roster
nfl_week = league.nfl_week
good_player_status_list = ["ACTIVE", "NORMAL"]


roster_projections = []

for player in roster:

    name = player.name
    position = player.position
    projection = player.stats.get(nfl_week,{}).get("projected_points",0)
    flag = False
    reason = ""
    injury_status = player.injuryStatus
    player_schedule = player.schedule

   

   
    if str(nfl_week) not in player_schedule:
        projection = 0
        reason = "Player on BYE"
    elif injury_status in good_player_status_list:
        pass
    elif injury_status == "OUT" or injury_status == "INJURY_RESERVE":
        projection = 0
        reason = injury_status
    else:
        flag = True
        reason = injury_status


   
    

    player_info = {
    "name": name,
    "position": position, 
    "projection": projection, 
    "flag": flag, 
    "reason": reason
    }

    roster_projections.append(player_info)




def optimize_lineup(roster_projections):

    slot_order = ["QB", "RB", "RB", "WR", "WR", "TE", "FLEX"]
    allowed_pos ={"QB": ["QB"], "RB": ["RB"], "WR":["WR"], "TE":["TE"], "FLEX": ["RB", "WR", "TE"] }
    inactive = []
    roster_pool = []




    for p in roster_projections:
    
        if p["position"] == "K" or p["position"] == "D/ST":
            pass
        elif p["projection"] == 0:
            inactive.append(p)
        else:
            roster_pool.append(p)




    roster_pool.sort(key=lambda x: x["projection"], reverse=True)



    lineup = []
    warnings = []


    for slot in slot_order:
        for player in roster_pool:
            if player["position"] in allowed_pos[slot]:
                lineup.append({"slot": slot, "player": player})
                roster_pool.remove(player)
                break
            
        else:
            lineup.append({"slot": slot, "player": None})
            warning = "No eligible player for " + slot
            warnings.append(warning)




    return lineup, roster_pool, inactive, warnings


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