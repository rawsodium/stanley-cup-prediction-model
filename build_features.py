from src.processing.history import (
    get_head_to_head,
    get_playoff_matchup_games,
    summarize_series,
    summarize_head_to_head
)

def build_features(team1, team2, standings_df, games_df):

    # Head-to-head
    h2h_df = get_head_to_head(team1, team2)
    h2h_stats = summarize_head_to_head(h2h_df, team1)

    # Playoff history
    matchup_games = get_playoff_matchup_games(games_df, team1, team2)
    series_stats = summarize_series(matchup_games, team1, team2)

    return {
        "team1": team1,
        "team2": team2,

        # model features
        "team1_h2h_wins": h2h_stats["team1_h2h_wins"],
        "goal_diff": h2h_stats["goal_diff"],
        "team1_series_wins": series_stats["team1_series_wins"]
    }