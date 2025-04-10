import pandas as pd
from sqlalchemy import create_engine


# github_url = ""

# #Parameters for database connection
# user="postgres"
# password="tuanp123"
# host ="localhost"
# database="football_data"
# port=5432

# # Create connection string
# connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# # Connect to the PostgreSQL database
# engine = create_engine(connection_string)

# df = pd.read_excel(github_url, engine='openpyx1')

# df.to_sql()

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