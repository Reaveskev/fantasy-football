
def score_projection(players):
    player_projections = []

    for player in players:
        flag = False
        reason = ""
        projection = player["espn_projection"]



        good_player_status_list = ["ACTIVE", "NORMAL"]

        if player["bye"]:
            projection = 0
            reason = "Player is on a BYE week"

        elif player["status"] in good_player_status_list:
            pass
        elif player["status"] == "OUT" or player["status"] == "INJURY_RESERVE":
            projection = 0
            reason = player["status"]
        else:
            flag = True
            reason = player["status"]


        player_info = {
    "name": player["name"],
    "position": player["position"], 
    "projection": projection, 
    "flag": flag, 
    "reason": reason
    }

        player_projections.append(player_info)

    return player_projections



