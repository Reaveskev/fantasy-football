
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
