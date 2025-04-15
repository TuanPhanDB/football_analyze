import pandas as pd
from sqlalchemy import create_engine
import requests
import os
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

def authenticate(league):
    # define parameters for a request
    token = os.environ["token"]
    owner = 'TuanPhanDB'
    repo = 'football_analyze'
    path = f'{league}_standing.xlsx'

    # Use raw content URL
    url = f'https://raw.githubusercontent.com/{owner}/{repo}/main/{path}'
    
    headers = {'Authorization': f'token {token}'} if token else {}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        # Check if we got the actual file
        if response.headers.get('Content-Type') != 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            try:
                error_data = response.json()
                raise ValueError(f"GitHub API error: {error_data.get('message')}")
            except ValueError:
                raise ValueError("Received unexpected response from GitHub")
        
        # Read Excel file
        excel_data = BytesIO(response.content)
        
        try:
            return pd.read_excel(excel_data, engine='openpyxl')
        except:
            excel_data.seek(0)
            return pd.read_excel(excel_data, engine='xlrd')
            
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Failed to fetch file: {str(e)}")



# def database_loader(url, name):
#     try:
#         df = pd.read_excel(url, engine='openpyxl')

#         # Write to database
#         df.to_sql(name, engine, if_exists='replace', index=False, chunksize=1000)
    
#     except Exception as e:
#         print("❌ Error:", e)

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
    df = authenticate(league)

    # Custom name for each table
    table_name = f"{league}_standing"

    # Write to database
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=1000)

# Load squad to database
# squad_url = "https://github.com/TuanPhanDB/football_analyze/blob/main/squad_info.xlsx"
# database_loader(squad_url, "squad_info")


