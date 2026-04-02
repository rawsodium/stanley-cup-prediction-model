import pandas as pd

def build_playoff_bracket(df):
    """
    Returns a DataFrame of the 16 playoff teams (8 per conference)
    based on NHL playoff rules (top 3 per division + 2 wildcards)
    """

    playoff_teams = []

    for conference in df['conference'].unique():
        conf_df = df[df['conference'] == conference].copy()

        conf_df = conf_df.sort_values(
            ['points', 'wins', 'goal_diff'],
            ascending=False
        )

        divisions = conf_df['division'].unique()

        division_top_three = []

        for div in divisions:
            div_df = conf_df[conf_df['division'] == div]
            division_top_three.append(div_df.head(3))

        division_top_three_df = pd.concat(division_top_three)

        # wildcard teams
        remaining = conf_df.drop(division_top_three_df.index)
        wildcards = remaining.head(2)

        playoff_teams.append(pd.concat([division_top_three_df, wildcards]))

    playoff_df = pd.concat(playoff_teams).reset_index(drop=True)

    return playoff_df
