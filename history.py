import requests
import pandas as pd

import requests

# set to 2024-25 season for default for right now..
def get_head_to_head(team1, team2, season="20242025"):
    url = f"https://api-web.nhle.com/v1/club-schedule-season/{team1}/{season}"
    data = requests.get(url).json()

    games = []

    for game in data.get('games', []):
        home = game['homeTeam']['abbrev']
        away = game['awayTeam']['abbrev']

        if team2 not in (home, away):
            continue

        home_score = game.get('homeScore')
        away_score = game.get('awayScore')

        if home_score is None or away_score is None:
            continue  # skip future games

        games.append({
            "home": home,
            "away": away,
            "home_score": home_score,
            "away_score": away_score,
            "winner": home if home_score > away_score else away
        })

    return pd.DataFrame(games)

def get_playoff_matchup_games(df, team1, team2):
    """
    Returns all playoff games between two teams.
    """

    mask = (
        ((df['homeAbbrev'] == team1) & (df['awayAbbrev'] == team2)) |
        ((df['homeAbbrev'] == team2) & (df['awayAbbrev'] == team1))
    )

    return df.loc[mask].copy()

def add_series_id(df):
    """
    Adds a series_id column by trimming gameId.
    """
    df = df.copy()
    df['series_id'] = df['gameId'].astype(str).str[:-1]
    return df

def add_winner(df):
    df = df.copy()

    df['winner'] = df.apply(
        lambda row: row['homeAbbrev']
        if row['homeGoals'] > row['awayGoals']
        else row['awayAbbrev'],
        axis=1
    )

    return df

def summarize_series(df, team1, team2):
    """
    Returns series-level stats between two teams.
    """

    if df.empty:
        return {
            "series_played": 0,
            "team1_series_wins": 0,
            "team2_series_wins": 0,
            "avg_games_per_series": 0
        }

    df = add_series_id(df)
    df = add_winner(df)

    series_stats = []

    for series_id, group in df.groupby('series_id'):
        wins = group['winner'].value_counts()

        team1_wins = wins.get(team1, 0)
        team2_wins = wins.get(team2, 0)

        winner = team1 if team1_wins > team2_wins else team2

        series_stats.append({
            "series_id": series_id,
            "winner": winner,
            "games_played": len(group)
        })

    series_df = pd.DataFrame(series_stats)

    return {
        "series_played": len(series_df),
        "team1_series_wins": (series_df['winner'] == team1).sum(),
        "team2_series_wins": (series_df['winner'] == team2).sum(),
        "avg_games_per_series": series_df['games_played'].mean()
    }

def summarize_head_to_head(df, team1):
    """
    Converts raw head-to-head games into model features.
    """

    if df.empty:
        return {
            "h2h_games": 0,
            "team1_h2h_wins": 0,
            "goal_diff": 0
        }

    team1_wins = (df['winner'] == team1).sum()

    # goal differential from team1 perspective
    goal_diff = 0

    for _, row in df.iterrows():
        if row['home'] == team1:
            goal_diff += row['home_score'] - row['away_score']
        else:
            goal_diff += row['away_score'] - row['home_score']

    return {
        "h2h_games": len(df),
        "team1_h2h_wins": team1_wins,
        "goal_diff": goal_diff
    }
