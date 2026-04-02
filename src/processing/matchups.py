def generate_playoff_matchups(playoff_df):
    """
    Returns a list of tuples [(team1, team2), ...] that represents first-round playoff matchups
    """

    matchups = []

    for conference in playoff_df['conference'].unique():
        conf_df = playoff_df[playoff_df['conference'] == conference].copy()

        # denote division winners
        division_winners = (
            conf_df.sort_values(['points', 'wins'], ascending=False)
            .groupby('division')
            .head(1)
            .sort_values('points', ascending=False)
        )

        # remaining teams
        non_winners = conf_df.drop(division_winners.index)

        # wildcards = top 2 remaining
        wildcards = non_winners.sort_values(
            ['points', 'wins'], ascending=False
        ).head(2)

        # best division winner plays lower wildcard
        matchups.append((
            division_winners.iloc[0]['team'],
            wildcards.iloc[1]['team']
        ))

        matchups.append((
            division_winners.iloc[1]['team'],
            wildcards.iloc[0]['team']
        ))

        # handle 2nd and 3rd in divisions playing each other
        for division in conf_df['division'].unique():
            div_df = conf_df[conf_df['division'] == division] \
                .sort_values(['points', 'wins'], ascending=False)

            matchups.append((
                div_df.iloc[1]['team'],
                div_df.iloc[2]['team']
            ))

    return matchups
