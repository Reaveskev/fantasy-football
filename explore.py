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
        print(team)
        my_team = team
        break

if my_team is None:
    print("Did not recieve team infomation")
    quit()




roster = my_team.roster
nfl_week = league.nfl_week


for player in roster:
    name = player.name
    position = player.position
    projection = player.stats[nfl_week]["projected_points"]
    print(name, position, projection)

