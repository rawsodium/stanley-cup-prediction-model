# get the current standings so we know what data we can actually throw into the model 
# we only want the top 16 teams, and we need to know who they're playing
import requests
import pandas as pd
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")
url = f"https://api-web.nhle.com/v1/standings/{today}"

response = requests.get(url)

csv_filename = f"nhl_standings_{today}.csv"

response = requests.get(url)

data = response.json()

teams = []

for team in data["standings"]:
    teams.append({
        "team": team["teamName"]["default"],
        "conference": team["conferenceName"],
        "division": team["divisionName"],
        "points": team["points"],
        "wins": team["wins"],
        "losses": team["losses"],
        "ot_losses": team["otLosses"],
        "goal_diff": team["goalDifferential"]
    })

standings_df = pd.DataFrame(teams)
print(standings_df)

standings_df.to_csv(csv_filename, index=False)


def build_playoff_bracket(df):
    playoff_teams = []

    for conference in df['conference'].unique():
        conf_df = df[df['conference'] == conference]

        divisions = conf_df['division'].unique()

        division_top_three = []

        for div in divisions:
            div_df = conf_df[conf_df['division'] == div]
            div_df = div_df.sort_values('points', ascending=False)

            division_top_three.append(div_df.head(3))

        division_top_three_df = pd.concat(division_top_three)

        remaining = conf_df.drop(division_top_three_df.index)
        wildcards = remaining.sort_values("points", ascending=False).head(2)

        playoff_teams.append(pd.concat([division_top_three_df, wildcards]))

    return pd.concat(playoff_teams)

playoff_df = build_playoff_bracket(standings_df)
print(playoff_df)

date = datetime.today().strftime("%Y-%m-%d")

standings_df.to_csv(f"standings_{date}.csv", index=False)
playoff_df.to_csv(f"playoff_teams_{date}.csv", index=False)

