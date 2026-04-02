import pandas as pd

def build_series_dataset(games_df):
    df = games_df.copy()

    # create series ID
    df['series_id'] = df['gameId'].astype(str).str[:-1]

    series_rows = []

    for series_id, group in df.groupby('series_id'):
        group = group.sort_values('gameDate')

        team1 = group.iloc[0]['homeAbbrev']
        team2 = group.iloc[0]['awayAbbrev']

        # count wins
        team1_wins = 0
        team2_wins = 0

        for _, row in group.iterrows():
            if row['homeGoals'] > row['awayGoals']:
                winner = row['homeAbbrev']
            else:
                winner = row['awayAbbrev']

            if winner == team1:
                team1_wins += 1
            else:
                team2_wins += 1

        # determine series winner
        team1_won = 1 if team1_wins > team2_wins else 0

        series_rows.append({
            "series_id": series_id,
            "team1": team1,
            "team2": team2,
            "team1_won": team1_won,
            "games_played": len(group)
        })

    return pd.DataFrame(series_rows)

from history import (
    get_playoff_matchup_games,
    summarize_series,
    get_head_to_head,
    summarize_head_to_head
)

def build_training_data(series_df, games_df):
    rows = []

    for _, row in series_df.iterrows():
        team1 = row['team1']
        team2 = row['team2']

        # Historical playoff matchup stats
        matchup_games = get_playoff_matchup_games(games_df, team1, team2)
        series_stats = summarize_series(matchup_games, team1, team2)

        # Regular season head-to-head (use same season as series)
        season = row['series_id'][:4] + row['series_id'][:4]  # crude but works
        h2h_df = get_head_to_head(team1, team2, season)
        h2h_stats = summarize_head_to_head(h2h_df, team1)

        rows.append({
            **row.to_dict(),
            **series_stats,
            **h2h_stats
        })

    return pd.DataFrame(rows)
