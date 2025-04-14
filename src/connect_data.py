import pandas as pd
from sqlalchemy import create_engine

league_names = ["Premier_League", "La_Liga", "Serie_A", "Ligue_1", "Bundesliga"]
for league in league_names:
    league_url = f"https://github.com/TuanPhanDB/football_analyze/blob/main/league_standings/{league}_standing.xlsx"


squad_url = "https://github.com/TuanPhanDB/football_analyze/blob/main/squad_info.xlsx"


def test_sqlalchemy_connection():
    try:
        user=""
        password=""
        host =""
        database=""
        port=

        # Create connection string
        connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

        engine = create_engine(connection_string)
        conn = engine.connect()
        print("✅ PostgreSQL connection successful (SQLAlchemy)!")
        conn.close()
    except Exception as e:
        print("❌ Connection failed:", e)

test_sqlalchemy_connection()