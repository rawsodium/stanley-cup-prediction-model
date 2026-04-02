import numpy as np

# not used yet
def predict_series_with_prob(team1, team2, features_df):
    """
    Predicts winner between team1 and team2 using features_df.
    Returns (winner, probability_team1_wins)
    """

    # try to find the row matching team1/team2
    row = features_df[
        ((features_df['team1'] == team1) & (features_df['team2'] == team2)) |
        ((features_df['team1'] == team2) & (features_df['team2'] == team1))
    ]

    if row.empty:
        # fallback: no features available
        print(f"No features found for matchup {team1} vs {team2}. Using 50/50.")
        return team1, 0.5

    row = row.iloc[0]

    # Check if the row is swapped
    swapped = (row['team1'] != team1)

    # extract relevant features
    team1_h2h_wins = row['team1_h2h_wins'] if not swapped else row['team2_h2h_wins']
    goal_diff = row['goal_diff'] if not swapped else -row['goal_diff']
    team1_series_wins = row['team1_series_wins'] if not swapped else row['team2_series_wins']

    # compute score
    score = 0.3 * team1_h2h_wins + 0.1 * goal_diff + 0.5 * team1_series_wins

    # convert score to probability via logistic function
    import math
    prob = 1 / (1 + math.exp(-score))  # sigmoid

    winner = team1 if prob >= 0.5 else team2

    return winner, prob

def predict_series(team1, team2, features_df):
    row = features_df[
        (features_df['team1'] == team1) &
        (features_df['team2'] == team2)
    ]

    if row.empty:
        return team1  # fallback

    row = row.iloc[0]

    score = 0

    # Head-to-head weight
    score += row['team1_h2h_wins'] * 0.3

    # Goal differential
    score += row['goal_diff'] * 0.1

    # Playoff experience
    score += row['team1_series_wins'] * 0.5

    return team1 if score >= 0 else team2

def simulate_round(matchups, features_df):
    winners = []

    for team1, team2 in matchups:
        winner = predict_series(team1, team2, features_df)
        winners.append(winner)

    return winners

def simulate_playoffs(initial_matchups, features_df):
    """
    Simulate the playoffs and return detailed results.

    Returns:
        results: list of dicts with round, team1, team2, winner, prob
        champion: name of the Stanley Cup winner
    """
    round_num = 1
    current_matchups = initial_matchups
    results = []

    while len(current_matchups) > 1:
        print(f"\n--- ROUND {round_num} ---")
        winners = []

        for team1, team2 in current_matchups:
            winner, prob = predict_series_with_prob(team1, team2, features_df)
            print(f"{team1} vs {team2} → {winner} (P(team1 wins)={prob:.2f})")

            results.append({
                "round": round_num,
                "team1": team1,
                "team2": team2,
                "winner": winner,
                "team1_win_prob": prob
            })

            winners.append(winner)

        # prepare next round matchups
        current_matchups = [
            (winners[i], winners[i+1])
            for i in range(0, len(winners), 2)
        ]

        round_num += 1

    champion = current_matchups[0][0]
    print(f"\nStanley Cup Winner: {champion}")

    return results, champion