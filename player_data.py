# Started size at 200, then increased to 250 

def collect_rb_ids(league, fa_size = 250):
    rb_ids = set()

    for team in league.teams:
        for player in team.roster:
            if player.position == "RB":
                rb_ids.add(player.playerId)

    free_agents = league.free_agents(position="RB", size=fa_size)
    if len(free_agents) == fa_size:
        print(f"Warning: free_agents hit the cap ({fa_size}), results may be truncated")

    for player in free_agents:
        rb_ids.add(player.playerId)
        
    return rb_ids



def fetch_players(league, ids, batch_size=50):
    ids_list = list(ids)
    players = []

    for start in range(0, len(ids_list),batch_size):
        batch = league.player_info(playerId=ids_list[start:start + batch_size])


        if not isinstance(batch,list):
            batch = [batch]
        
        players.extend(batch)


    if len(ids_list) != len(players):
        print(f"Warning: sent {len(ids_list)} IDs, got {len(players)} players")

    return players
    
