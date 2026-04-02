import requests
import pandas as pd
from datetime import datetime

# gets the NHL standings for the current date
def get_standings(date):
    url = f"https://api-web.nhle.com/v1/standings/{date}"
    response = requests.get(url)
    data = response.json()

    teams = []

    for team in data["standings"]:
        teams.append({
            "team": team["teamAbbrev"]["default"],
            "conference": team["conferenceName"],
            "division": team["divisionName"],
            "points": team["points"],
            "wins": team["wins"],
            "losses": team["losses"],
            "ot_losses": team["otLosses"],
            "goal_diff": team["goalDifferential"]
        })

    return pd.DataFrame(teams)

# def get_team_schedule(team, season):
