import pandas as pd
from sqlalchemy import create_engine
import requests
import os
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

def data_loader(path , name):
    token = os.environ["token"]
    owner = 'TuanPhanDB'
    repo = 'football_analyze'
    path = f'{path}/{name}.csv'

    try:
        # send a request
        r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
        owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
                }
        )

        # convert string to StringIO object
        string_io_obj = StringIO(r.text)

        # Load data to df
        df = pd.read_csv(string_io_obj)

        return df
     
    except Exception as e:
        print("Error", e)


# Connection parameters
user="postgres"
password="tuanp123"
host ="localhost"
database="football_data"
port=5432

# Create connection string
connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(connection_string)

# Load leagues standing to database
league_names = ["Premier_League", "La_Liga", "Serie_A", "Ligue_1", "Bundesliga"]
for league in league_names:
    # Retrieve data from GitHub
    df = data_loader('league_standings', f'{league}_standing')

    # Custom name for each table
    table_name = f"{league}_standing"

    # Write to database
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)

# Load stats info to database
stats_list = ["squad", "gk", "shooting", "passing", "gca", "defense", "possession", "miscellaneous"]
for stats in stats_list:
    df = data_loader('', f'{stats}_stats')

    # Custom name for each table
    table_name = f"{stats}_stats"

    # Write to database
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)




