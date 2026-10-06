# Spotify Music & Song Popularity Analysis — Dashboard 🎵📊

## What is included?
This version converts the EDA mini project into an interactive **Streamlit dashboard**.

### Dashboard features
- KPI cards for number of songs, average popularity, artists and duration
- Genre filter
- Release-year filter
- Popularity-range filter
- Popularity distribution
- Average popularity by release year
- Genre-wise popularity comparison
- Genre song-count comparison
- Audio feature vs popularity scatter plot
- Correlation with popularity
- Top-N popular songs table and chart

## How to run

### 1. Install Python
Use Python 3.10+ if possible.

### 2. Open Command Prompt in this project folder

### 3. Install the libraries
```bash
pip install -r requirements.txt
```

### 4. Start the dashboard
```bash
streamlit run app.py
```

### 5. Open the address shown by Streamlit
Usually it opens automatically in your browser.

## Project flow

Dataset
  ↓
Pandas Data Loading
  ↓
Data Cleaning
  ↓
Sidebar Filters
  ↓
EDA Calculations
  ↓
Interactive Charts
  ↓
Dashboard Insights

## Viva explanation

“My project is an interactive Exploratory Data Analysis dashboard for Spotify music data. The dashboard allows users to filter songs by genre, release year and popularity. It displays KPIs, genre-wise analysis, popularity distributions, feature-versus-popularity relationships, correlation values and the most popular songs. Streamlit is used to convert the Python EDA analysis into an interactive web dashboard.”

## Important note
The included CSV is a reproducible Spotify-style educational dataset. If your department specifically requires a real Spotify/Kaggle dataset, the CSV can be replaced with a permitted dataset using the same column structure.

Correlation shows association and does not prove that a particular audio feature causes popularity.
