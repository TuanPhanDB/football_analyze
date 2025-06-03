# ⚽ Football Analyze

**Football Analyze** is a data-driven project designed to scrape, process, and visualize football statistics from [FBref](https://fbref.com). The project serves as a hands-on exercise in **data manipulation**, **automation**, and **Power BI dashboarding**.

---

## 📁 Project Structure

![data_structure](https://github.com/user-attachments/assets/832ca5eb-c5df-4ba3-968f-f9e957bf9ab6)

## 📝 Project Workflow

### 1. Data Retrieval

- Data is scraped from [https://fbref.com](https://fbref.com)
- Focused on **top 5 European leagues** for the 2024–2025 season:
  - 🇬🇧 Premier League (England)
  - 🇪🇸 La Liga (Spain)
  - 🇩🇪 Bundesliga (Germany)
  - 🇫🇷 Ligue 1 (France)
  - 🇮🇹 Serie A (Italy)

- Player statistics include:
  - Squad
  - Shooting
  - Passing
  - Possession
  - Miscellaneous
  - Goal-Creation Actions (GCA)
  - Defense
  - Goalkeeping (GK)

---

### 2. Automated Updates

- GitHub Actions is used to automate the data scraping process.
- The `fbref_scrap.py` script is scheduled to run **every Monday** to ensure up-to-date data.

---

### 3. Local Database Integration

- A **PostgreSQL database** is run via Docker for local storage.
- To set up the PostgreSQL environment, follow this guide:  
  👉 [Create PostgreSQL Database in Docker](https://www.commandprompt.com/education/how-to-create-a-postgresql-database-in-docker/)

- Once your database is up and running:
  1. Execute `connect_data.py` to load the scraped data into the local DB.
  2. Ensure your PostgreSQL Docker container is running during the process.
  3. Open **Power BI** and use the **"Get data"** feature to connect to your local database:

  ![Connect_database](https://github.com/user-attachments/assets/57ea479b-1ae7-4f45-8175-f96cbb8f100c)

---

### 4. Power BI Dashboard

- Data is transformed and visualized using **Power BI**.
- The `Visualization/` folder contains:
  - Power BI `.pbix` file
  - Custom themes
  - Relevant images for dashboards

- Here are some dashboard demos:
  <p align="center"><b>League Overview</b></p>

![PL_dashboard](https://github.com/user-attachments/assets/5110dd02-9557-4f36-8a90-95a08e286acb)

  <p align="center"><b>Team Statistics</b></p>

![Team_Stats](https://github.com/user-attachments/assets/575f8dc3-3806-4156-a944-3d718e70aa51)

  <p align="center"><b>Player Performance</b></p>

![Player_sstats](https://github.com/user-attachments/assets/15802bbd-b092-4ed8-9f6a-5c5d52272e4b)

  <p align="center"><b>Goalkeeper Performance</b></p>

![gk_stats](https://github.com/user-attachments/assets/b3368782-047c-4cf9-9375-6533648c78c9)
---

## 🚀 Technologies Used

- Python
- Pandas, Requests
- GitHub Actions
- PostgreSQL (via Docker)
- Power BI

---

## ✅ To-Do

Here are some features and improvements planned for the future:

- [ ] Allow selection of target seasons
- [ ] Add support for more leagues (e.g., Eredivisie, Primeira Liga)
- [ ] Optimize data model


---

## 📌 Notes

- All football data used in this project is sourced from [FBref](https://fbref.com), a publicly accessible football statistics website.
- This project is intended for **educational and personal learning purposes**.


