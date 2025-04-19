import pandas as pd
import json
import time
import os

#--------------------------------------------------------------------------------------------------------#
#------------------------------- Squad and Players information ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
def get_squad_info():

    with open('Teams_ID.json', 'r') as file:
        team_squad = json.load(file)

    player_table = pd.DataFrame([])

    for league in team_squad:
        league_teams = team_squad[league][0]

        for team, team_id in league_teams.items():
            try:
                url = f"https://fbref.com/en/squads/{team_id}/2024-2025/all_comps/{team}-Stats-All-Competitions"

                table = pd.read_html(url, attrs={"id" : "stats_standard_combined"})

                #When use read_html, it will wrap all the table into a list, even there is only 1 table.
                #That is why using table = table[0] to extract the first Df from the list
                table = table[0]

                #Drop multi header
                table.columns = table.columns.droplevel(0)

                #Add squad name to df
                table['Squad'] = team           

                #Add league name
                table['League'] = league

                #Filter only player who played
                table = table[table['MP'] > 0]

                player_table = pd.concat([player_table, table])
                player_table.reset_index()

                time.sleep(3)
            
            except Exception as e:
                print(f"Error retrieving data for {team}: {str(e)}")
                continue

    return player_table

#--------------------------------------------------------------------------------------------------------#
#-------------------------------- Leagues Standing ------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
def get_league_info():

    #Top 5 leagues
    leagues = {'Premier-League' : 9, 'La-Liga' : 12, 'Serie-A' : 11, 'Ligue-1' : 13, 'Bundesliga' : 20}
    Premier_League = pd.DataFrame()
    La_Liga = pd.DataFrame()
    Serie_A = pd.DataFrame()
    Ligue_1 = pd.DataFrame()
    Bundesliga = pd.DataFrame()
    #Get all teams

    for league in leagues:
        url = f"https://fbref.com/en/comps/{leagues.get(league)}/{league}-Stats"

        try:
            table = pd.read_html(url, attrs={"id" : f"results2024-2025{leagues.get(league)}1_overall"})

            #Target columns
            target_cols = table[0][['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 
                                'Pts', 'Pts/MP', 'xG', 'xGA', 'xGD', 'xGD/90', 'Last 5']]
            
            # Assign to the appropriate DataFrame
            if league == 'Premier-League':
                Premier_League = target_cols.copy()
            elif league == 'La-Liga':
                La_Liga = target_cols.copy()
            elif league == 'Serie-A':
                Serie_A = target_cols.copy()
            elif league == 'Ligue-1':
                Ligue_1 = target_cols.copy()
            elif league == 'Bundesliga':
                Bundesliga = target_cols.copy()

            time.sleep(5)

        except Exception as e: 
            print(f"Error retrieving data for {league.replace('_', ' ')}: {str(e)}")

    return [Premier_League, La_Liga, Serie_A, Ligue_1, Bundesliga]

#--------------------------------------------------------------------------------------------------------#
#-------------------------------- Call Functions --------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# Create folder and path for leagues standing
output_dir = "league_standings"
os.makedirs(output_dir, exist_ok=True)

league_names = ["Premier_League", "La_Liga", "Serie_A", "Ligue_1", "Bundesliga"]
league_list = get_league_info()

# Generate leagues standing
for league, name in zip(league_list, league_names):
    file_name = f'{name}_standing.csv'
    file_path = os.path.join(output_dir, file_name)
    league.to_csv(file_path)

# Generate squad info
squad = get_squad_info()
file_name = 'squad_info.csv'
squad.to_csv(file_name)


