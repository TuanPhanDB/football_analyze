# football_analyze

This project scrapes the data from football data websites https://fbref.com

The project aims to practice data manipulation, automation, and Power BI.

# Steps:

1. Retrieve data

- All the data in this project belong to https://fbref.com

- The data in this project from the top 5 European Leagues (season 2024 - 2025):

  - Premier League - England
  - La Liga - Spain
  - Bundesliga - Germany
  - Ligue 1 - France
  - Serie A - Italy

- Necessary data was retrieved to support the Power BI visualizations. 

- The league table was stored in the folder league_standings which shows the ranking in domestic leagues. All stats were stored in stats_info which contains info that supports player in-depth visualization.

2. Automate update

- Using workflows from GitHub to refresh the data every week.

3. Local database

- Using connect_data.py from folder src to establish the connection to the local database. 

- After the local database is ready, use Power BI to connect to the database.

- This is for practicing Power BI which uses the data from the database.
  
4. Power BI

- After connecting to the database, transform and clean the data. 

