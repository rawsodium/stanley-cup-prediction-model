from datetime import datetime
import pandas as pd

from src.api.nhl_api import get_standings
from src.processing.standings import build_playoff_bracket
from src.processing.matchups import generate_playoff_matchups
from src.features.build_features import build_features
from src.models.baseline_prediction_model import simulate_playoffs

# Load playoff history data
playoff_games_df = pd.read_csv(
    "cleaned_data/cleaned_game_boxscores_playoffs.csv"
)

today = datetime.today().strftime("%Y-%m-%d")

# 1. standings
standings_df = get_standings(today)
standings_df.to_csv(f"outputs/current_standings_{today}.csv", index=False)

# 2. playoff teams
playoff_df = build_playoff_bracket(standings_df)
playoff_df.to_csv(f"outputs/playoff_teams_{today}.csv", index=False)

# 3. matchups
matchups = generate_playoff_matchups(playoff_df)

# 4. build features
features = []

for team1, team2 in matchups:
    row = build_features(team1, team2, standings_df, playoff_games_df)
    features.append(row)

features_df = pd.DataFrame(features)
features_df.to_csv(f"outputs/model_input_{today}.csv", index=False)

# 5. simulate playoffs
simulate_playoffs(matchups, features_df)

results, champion = simulate_playoffs(matchups, features_df)

# Save results and champion to CSV
import pandas as pd

results_df = pd.DataFrame(results)
results_df.to_csv("playoff_predictions.csv", index=False)
print(f"Playoff results saved. Champion: {champion}")

print(f"Stanley Cup Winner: {champion}")


