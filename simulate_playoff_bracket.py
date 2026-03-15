# this is a toy exercise essentially, but predicts based on standings right now, and nothing else
import numpy as np
import pandas as pd
import random
from datetime import datetime

today = datetime.today().strftime("%Y-%m-%d")
csv_filename = f"nhl_standings_{today}.csv"

def win_probability(teamA, teamB):
    pA = teamA["points_pct"]
    pB = teamB["points_pct"]

    return pA / (pA + pB)

def simulate_series(teamA, teamB):

    p = win_probability(teamA, teamB)

    winsA = 0
    winsB = 0

    while winsA < 4 and winsB < 4:
        if random.random() < p:
            winsA += 1
        else:
            winsB += 1

    return teamA if winsA == 4 else teamB


def play_round(teams):

    winners = []

    for i in range(0, len(teams), 2):
        teamA = teams.iloc[i]
        teamB = teams.iloc[i+1]

        winner = simulate_series(teamA, teamB)
        winners.append(winner)

    return winners

def simulate_playoffs(playoff_df=pd.read_csv(csv_filename)):
    east = playoff_df[playoff_df["conference"] == "Eastern"]
    west = playoff_df[playoff_df["conference"] == "Western"]

    east = east.sort_values("points", ascending=False)
    west = west.sort_values("points", ascending=False)

    east_teams = list(east.to_dict("records"))
    west_teams = list(west.to_dict("records"))

    # Round 1
    east_r1 = play_round(pd.DataFrame(east_teams))
    west_r1 = play_round(pd.DataFrame(west_teams))

    # Round 2
    east_r2 = play_round(pd.DataFrame(east_r1))
    west_r2 = play_round(pd.DataFrame(west_r1))

    # Conference Finals
    east_champ = simulate_series(east_r2[0], east_r2[1])
    west_champ = simulate_series(west_r2[0], west_r2[1])

    # Stanley Cup Final
    cup_winner = simulate_series(east_champ, west_champ)

    return cup_winner

results = {}

for i in range(10000):
    playoff_df = pd.read_csv(csv_filename)
    # playoff_df["points_pct"] = playoff_df["points"] / (playoff_df["games_played"] * 2)
    winner = simulate_playoffs(playoff_df)

    team = winner["team"]

    results[team] = results.get(team, 0) + 1

for team, wins in sorted(results.items(), key=lambda x: x[1], reverse=True):
    print(team, wins/10000)

date = datetime.today().strftime("%Y-%m-%d")

sim_df = pd.DataFrame(
    [(k, v/10000) for k, v in results.items()],
    columns=["team","cup_probability"]
)

sim_df.to_csv(f"cup_probabilities_{date}.csv", index=False)