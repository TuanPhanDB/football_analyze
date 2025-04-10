import pandas as pd
import json
import time

#--------------------------------------------------------------------------------------------------------#

#--------------------------------------------------------------------------------------------------------#
def get_league_info():

    #Top 5 leagues
    leagues = {'Premier-League' : 9, 'La-Liga' : 12, 'Serie-A' : 11, 'Ligue-1' : 13, 'Bundesliga' : 20}
    league_table = pd.DataFrame([])
    #Get all teams
    for league in leagues:
        url = f"https://fbref.com/en/comps/{leagues.get(league)}/{league}-Stats"

        table = pd.read_html(url, attrs={"id" : "results2024-202591_overall"})

        #Target columns
        target_cols = table[0][['Rk', 'Squad', 'MP', 'W', 'D', 'L', 'GF', 'GA', 'GD', 
                            'Pts', 'Pts/MP', 'xG', 'xGA', 'xGD', 'xGD/90', 'Last 5']]
        
        league_table = pd.concat([league_table, target_cols])

        time.sleep(3)

        #Get only Premier League first
        break

    return league_table

def get_squad_info():

    with open('Teams_ID.json', 'r') as file:
        team_squad = json.load(file)

    player_table = pd.DataFrame([])

    for team in team_squad:
        url = f"https://fbref.com/en/squads/{team_squad.get(team)}/2024-2025/all_comps/{team}-Stats-All-Competitions"

        table = pd.read_html(url, attrs={"id" : "stats_standard_combined"})

        #When use read_html, it will wrap all the table into a list, even there is only 1 table.
        #That is why using table = table[0] to extract the first Df from the list
        table = table[0]

        #Add squad name to df
        table['Squad'] = team

        #Drop multi header
        table.columns = table.columns.droplevel(0)

        #Filter only player who played
        table = table[table['MP'] > 0]

        player_table = pd.concat([player_table, table])

        time.sleep(3)

    return player_table


squad = get_squad_info()
file_name = 'full_data.xlsx'
squad.to_excel(file_name)


