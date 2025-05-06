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

    league_ids = {
        "Premier-League": 9,
        "La-Liga": 12,
        "Serie-A": 11,
        "Ligue-1": 13,
        "Bundesliga": 20
    }

    for league in team_squad:
        league_teams = team_squad[league][0]
        league_id = league_ids.get(league)

        for team, team_id in league_teams.items():
            try:
                if request_count >= 5:
                    elapsed_time = time.time() - start_time
                    if elapsed_time < 60:
                        time.sleep(60 - elapsed_time)  # Wait until the next minute
                    request_count = 0
                    start_time = time.time()

                # if league == "Premier-League":
                #     league_id = 9
                # if league == "La-Liga":
                #     league_id = 12
                # if league == "Serie-A":
                #     league_id = 11
                # if league == "Ligue-1":
                #     league_id = 13
                # if league == "Bundesliga":
                #     league_id = 20

                url = f"https://fbref.com/en/squads/{team_id}/2024-2025/c{league_id}/{team}-Stats-{league}"

                #When use read_html, it will wrap all the table into a list, even there is only 1 table.
                #That is why using table = table[0] to extract the first Df from the list
                table_ids = {
                    "squad"         : f"stats_standard_{league_id}",
                    "gk"            : f"stats_keeper_{league_id}",
                    "shooting"      : f"stats_shooting_{league_id}",
                    "passing"       : f"stats_passing_{league_id}",
                    "gca"           : f"stats_gca_{league_id}",
                    "defense"       : f"stats_defense_{league_id}",
                    "possession"    : f"stats_possession_{league_id}",
                    "miscellaneous" : f"stats_misc_{league_id}"
                }
                # if target == "squad":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_standard_{league_id}"})[0]
                
                # if target == "gk":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_keeper_{league_id}"})[0]
                
                # if target == "shooting":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_shooting_{league_id}"})[0]
                
                # if target == "passing":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_passing_{league_id}"})[0]

                # if target == "gca":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_gca_{league_id}"})[0]

                # if target == "defense":
                #     info_data = pd.read_html(url, attrs={"id": f"stats_defense_{league_id}"})[0]
                
                # if target == "possession": 
                #     info_data = pd.read_html(url, attrs={"id": f"stats_possession_{league_id}"})[0]

                # if target == "miscellaneous": 
                #     info_data = pd.read_html(url, attrs={"id": f"stats_misc_{league_id}"})[0]

                info_data = pd.read_html(url, attrs={"id": table_ids.get(target)})[0]
                #Drop multi header
                info_data.columns = info_data.columns.droplevel(0)

                #Add squad name to df
                info_data['Squad'] = team           

                #Add league name
                info_data['League'] = league

                #Filter only player who played
                if target in ["squad", "gk"]:
                    info_data = info_data[info_data['MP'] > 0]

                #Drop last 2 rows of data "Squad Total" and "Opponent Total"
                info_data = info_data.iloc[:-2]

                info_table = pd.concat([info_table, info_data])
                info_table.reset_index(drop=True, inplace=True)

                request_count += 1

            except pd.errors.EmptyDataError:
                print(f"No data found for {team}")
            except Exception as e:
                print(f"Error retrieving data for {target}, {team}: {str(e)}")
                continue

    return info_table

#--------------------------------------------------------------------------------------------------------#
#-------------------------------- Leagues Standing ------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------#
#-------------------------------- Call Functions --------------------------------------------------------#
#--------------------------------------------------------------------------------------------------------#

# Create folder and path for leagues standing
# Generate squad info
output_dir_info = "stats_info"
os.makedirs(output_dir_info, exist_ok=True)

target_list = ["squad", "gk", "shooting", "passing", "gca", "defense", "possession", "miscellaneous"]

for target in target_list:
    df = get_info(target)
    file_name = f'{target}_stats.csv'
    file_path = os.path.join(output_dir_info, file_name)
    df.to_csv(file_name)

# There are some errors, squad and gk work fine. Test the other first
