import pandas as pd
import json
import time
import os

#--------------------------------------------------------------------------------------------------------#
#------------------------------- Squad and Players information ------------------------------------------#
#--------------------------------------------------------------------------------------------------------#
def get_info(target = "squad"):

    with open('Teams_ID.json', 'r') as file:
        team_squad = json.load(file)

    info_table = pd.DataFrame([])
    
    request_count = 0
    start_time = time.time()

    for league in team_squad:
        league_teams = team_squad[league][0]

        for team, team_id in league_teams.items():
            try:
                if request_count >= 5:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 60:
                        time.sleep(60 - elapsed_time)  # Wait until the next minute
                    request_count = 0
                    start_time = time.time()

                if league == "Premier-League":
                    league_id = 9
                if league == "La-Liga":
                    league_id = 12
                if league == "Serie-A":
                    league_id = 11
                if league == "Ligue-1":
                    league_id = 13
                if league == "Bundesliga":
                    league_id = 20

                url = f"https://fbref.com/en/squads/{team_id}/2024-2025/c{league_id}/{team}-Stats-{league}"

                #When use read_html, it will wrap all the table into a list, even there is only 1 table.
                #That is why using table = table[0] to extract the first Df from the list
                if target == "squad":
                    info_data = pd.read_html(url, attrs={"id": f"stats_standard_{league_id}"})[0]
                
                if target == "gk":
                    info_data = pd.read_html(url, attrs={"id": f"stats_keeper_{league_id}"})[0]

                if target == "shooting":
                    info_data = pd.read_html(url, attrs={"id": f"stats_shooting_{league_id}"})[0]
                
                if target == "passing":
                    info_data = pd.read_html(url, attrs={"id": f"stats_passing_{league_id}"})[0]

                if target == "gca":
                    info_data = pd.read_html(url, attrs={"id": f"stats_gca_{league_id}"})[0]

                if target == "defense":
                    info_data = pd.read_html(url, attrs={"id": f"stats_defense_{league_id}"})[0]
                
                if target == "possession": 
                    info_data = pd.read_html(url, attrs={"id": f"stats_possession_{league_id}"})[0]

                if target == "miscellaneous": 
                    info_data = pd.read_html(url, attrs={"id": f"stats_misc_{league_id}"})[0]

                #Drop multi header
                info_data.columns = info_data.columns.droplevel(0)

                #Add squad name to df
                info_data['Squad'] = team           

                #Add league name
                info_data['League'] = league

                #Filter only player who played in squad and gk df
                if (target == "squad" | target == "gk"):
                    info_data = info_data[info_data['MP'] > 0]

                #Drop last 2 rows of data "Squad Total" and "Opponent Total"
                info_data = info_data.iloc[:-2]

                info_table = pd.concat([info_table, info_data])
                info_table.reset_index()

                request_count += 1

            except Exception as e:
                print(f"Error retrieving data for {team}: {str(e)}")
                continue

    return info_table

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

#--------------------------------------------------------------------------------------------------------#
# Generate all stats files
output_dir_info = "stats_info"
os.makedirs(output_dir, exist_ok=True)

target_list = ["squad", "gk", "shooting", "passing", "gca", "defense", "possession", "miscellaneous"]

for target in target_list:
    df = get_info(target)
    file_name = f'{target}_stats.csv'
    file_path = os.path.join(output_dir, file_name)
    df.to_csv(file_name)



