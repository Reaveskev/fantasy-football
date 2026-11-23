from optimizer import optimize_lineup



# Run test .venv/Scripts/python.exe -m pytest


def make_player(name, position, projection):
    player_info = {
            "name": name,
            "position": position, 
            "projection": projection, 
            "flag": False, 
            "reason": ""
            }
    
    return player_info



def get_slot(lineup, slot_name):
    for starter in lineup:
        if starter["slot"] == slot_name:
            return starter

  




def test_full_roster():
    # Makes sure that the lineup is set, and that every spot is filled

    roster = [
    make_player("QB1", "QB", 22),
    make_player("RB1", "RB", 11),
    make_player("RB2", "RB", 20),
    make_player("WR1", "WR", 18),
    make_player("WR2", "WR", 17),
    make_player("TE", "TE", 15),
    make_player("RB3", "RB", 22),
    ]

    lineup, roster_pool, inactive, warnings = optimize_lineup(roster)
  
    assert all(slot["player"] is not None for slot in lineup)
    assert roster_pool == []
    assert inactive == []
    assert warnings == []



 


def test_missing_position():
    # Make sure it sets an empty slot as none
    roster = [
        make_player("QB1", "QB", 22),
        make_player("RB1", "RB", 11),
        make_player("RB2", "RB", 20),
        make_player("WR1", "WR", 18),
        make_player("WR2", "WR", 17),
        make_player("RB4", "RB", 15),
        make_player("RB3", "RB", 22),
        ]
    
    lineup, roster_pool, inactive, warnings = optimize_lineup(roster)
   
    te_slot = get_slot(lineup, "TE")
  

    assert te_slot is not None      # the slot exists
    assert te_slot["player"] is None  # and nobody's in it



    te_warning = warnings[0]
    
    assert te_warning == 'No eligible player for TE'
   
    
    
def test_best_player_starts():
    # Make sure the higher projected player starts
    roster = [
        make_player("QB1", "QB", 22),
        make_player("RB1", "RB", 11),
        make_player("RB2", "RB", 20),
        make_player("WR1", "WR", 18),
        make_player("WR2", "WR", 17),
        make_player("RB4", "RB", 15),
        make_player("TE1", "TE", 22),
        make_player("QB2", "QB", 30),
        ]
    
    lineup, roster_pool, inactive, warnings = optimize_lineup(roster)
   
    qb_slot = get_slot(lineup, "QB")
 

    assert qb_slot is not None      # the slot exists
    assert qb_slot["player"]["name"] == "QB2"  # QB2 is starting




   
    