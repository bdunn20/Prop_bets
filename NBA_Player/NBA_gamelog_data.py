import pandas as pd
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

# fetch list of players
player_dict = players.get_players()
player_df = pd.DataFrame(player_dict)

# filter to only active players
active_player_df = player_df[player_df['is_active'] == True]
# drop all but player_id and name
active_player_df = active_player_df.drop(columns=['first_name', 'last_name', 'is_active'])
# rename to prep for merge
active_player_df = active_player_df.rename(columns={"id": "Player_ID", "full_name": "Name"})
# convert to list for use in for loop
active_player_id_list = active_player_df['Player_ID'].tolist()

# empty df for game logs
df = pd.DataFrame()

# List of seasons
seasons = ['2022-23', '2023-24']

# fetch game logs and add "Season" column
for season in seasons:
    for id in active_player_id_list:
        player_log = playergamelog.PlayerGameLog(player_id=id, season=season).player_game_log.get_data_frame()
        # merge w/ full log
        df = pd.concat([df, player_log])

# merge in player name
df = df.merge(active_player_df, how='left', on='Player_ID')

# export csv
df.to_csv('NBA_gamelogs.csv', index=False)