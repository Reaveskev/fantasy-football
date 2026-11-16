from espn_api.football import League





def get_league(config):
    league = League(league_id=config["LEAGUE_ID"],year=config["SEASON"], espn_s2=config["ESPN_S2"], swid=config["SWID"])

    return league



# Connect to espn and grab roster
def get_roster(league, team_id):
    teams = league.teams
    my_team = None

    for team in teams:
        if team.team_id == team_id:
            my_team = team
            break

    if my_team is None:
        raise ValueError(f"No team with ID {team_id} in league {league.league_id}.")

    roster = my_team.roster
    nfl_week = league.nfl_week


    players = []

    for player in roster:

        name = player.name
        position = player.position
        projection = player.stats.get(nfl_week,{}).get("projected_points",0)
        injury_status = player.injuryStatus
        player_schedule = player.schedule
        on_bye = False

    
        if str(nfl_week) not in player_schedule:
            on_bye = True
        
        player_info = {
               "name": name,
               "position": position, 
               "espn_projection": projection, 
               "status": injury_status, 
               "bye": on_bye
               }


        players.append(player_info)


    return players