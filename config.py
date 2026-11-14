import os
from dotenv import load_dotenv


def load_config():


    load_dotenv()
    configs = {}

    for name in ["LEAGUE_ID","ESPN_S2", "SWID", "SEASON", "TEAM_ID"]:
        value = os.getenv(name)
        if value is None:
            raise ValueError(f'Missing {name} in .env.')
    

        configs[name] = value
    
    configs["SEASON"] = int(configs["SEASON"])
    configs["LEAGUE_ID"] = int(configs["LEAGUE_ID"])
    configs["TEAM_ID"] = int(configs["TEAM_ID"])


    return configs


