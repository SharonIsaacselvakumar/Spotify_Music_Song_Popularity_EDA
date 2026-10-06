import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Spotify Music & Popularity Dashboard",
    page_icon="🎵",
    layout="wide"
)

# ---------- Load data ----------
@st.cache_data
def load_data():
    df = pd.read_csv("spotify_music_data.csv")
    numeric_cols = [
        "duration_ms", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "instrumentalness",
        "valence", "tempo", "popularity"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df["duration_min"] = df["duration_ms"] / 60000
    return df

df = load_data()

# ---------- Sidebar ----------
st.sidebar.title("🎛️ Dashboard Filters")

genres = st.sidebar.multiselect(
    "Select Genre",
    sorted(df["genre"].unique()),
    default=sorted(df["genre"].unique())
)

min_year, max_year = int(df["release_year"].min()), int(df["release_year"].max())
year_range = st.sidebar.slider(
    "Release Year",
    min_year, max_year,
    (min_year, max_year)
)

pop_range = st.sidebar.slider(
    "Popularity Range",
    0, 100, (0, 100)
)

filtered = df[
    df["genre"].isin(genres)
    & df["release_year"].between(year_range[0], year_range[1])
    & df["popularity"].between(pop_range[0], pop_range[1])
].copy()

# ---------- Header ----------
st.title("🎵 Spotify Music & Song Popularity Analysis")
st.markdown(
    "### Exploratory Data Analysis Dashboard\n"
    "Explore song popularity, genres, audio characteristics and their relationships."
)

st.divider()

# ---------- KPI cards ----------
c1, c2, c3, c4 = st.columns(4)
c1.metric("🎵 Songs", f"{len(filtered):,}")
c2.metric("⭐ Avg. Popularity", f"{filtered['popularity'].mean():.1f}" if len(filtered) else "N/A")
c3.metric("🎤 Artists", f"{filtered['artist_name'].nunique():,}")
c4.metric("⏱️ Avg. Duration", f"{filtered['duration_min'].mean():.2f} min" if len(filtered) else "N/A")

if filtered.empty:
    st.warning("No songs match the selected filters. Please adjust the filters.")
    st.stop()

# ---------- Tabs ----------
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Overview", "🎶 Genre Analysis", "🔎 Feature Analysis", "🏆 Top Songs"
])

with tab1:
    st.subheader("Popularity Distribution")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.hist(filtered["popularity"], bins=15, edgecolor="black")
        ax.set_xlabel("Popularity Score")
        ax.set_ylabel("Number of Songs")
        ax.set_title("Distribution of Song Popularity")
        st.pyplot(fig)

    with col2:
        yearly = filtered.groupby("release_year")["popularity"].mean()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(yearly.index, yearly.values, marker="o")
        ax.set_xlabel("Release Year")
        ax.set_ylabel("Average Popularity")
        ax.set_title("Average Popularity by Release Year")
        ax.grid(alpha=0.25)
        st.pyplot(fig)

    st.subheader("Dataset Preview")
    st.dataframe(
        filtered[
            ["track_name", "artist_name", "genre", "release_year",
             "danceability", "energy", "tempo", "popularity"]
        ].head(20),
        use_container_width=True
    )

with tab2:
    st.subheader("Genre-wise Analysis")

    genre_summary = (
        filtered.groupby("genre")
        .agg(
            Songs=("track_name", "count"),
            Avg_Popularity=("popularity", "mean"),
            Avg_Danceability=("danceability", "mean"),
            Avg_Energy=("energy", "mean")
        )
        .sort_values("Avg_Popularity", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(genre_summary.index, genre_summary["Avg_Popularity"])
        ax.set_title("Average Popularity by Genre")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Average Popularity")
        ax.tick_params(axis="x", rotation=35)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(genre_summary.index, genre_summary["Songs"])
        ax.set_title("Number of Songs by Genre")
        ax.set_xlabel("Genre")
        ax.set_ylabel("Number of Songs")
        ax.tick_params(axis="x", rotation=35)
        st.pyplot(fig)

    st.subheader("Genre Summary Table")
    st.dataframe(genre_summary.round(2), use_container_width=True)

with tab3:
    st.subheader("Audio Features vs Popularity")

    feature = st.selectbox(
        "Choose an audio feature",
        ["danceability", "energy", "valence", "acousticness",
         "instrumentalness", "speechiness", "tempo", "loudness"]
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.scatter(filtered[feature], filtered["popularity"], alpha=0.6)
    ax.set_xlabel(feature.title())
    ax.set_ylabel("Popularity")
    ax.set_title(f"{feature.title()} vs Popularity")
    ax.grid(alpha=0.2)
    st.pyplot(fig)

    correlation = filtered[feature].corr(filtered["popularity"])
    st.info(
        f"Correlation between **{feature}** and **popularity**: "
        f"**{correlation:.3f}**"
    )

    st.subheader("Correlation with Popularity")
    numeric = [
        "duration_ms", "danceability", "energy", "loudness",
        "speechiness", "acousticness", "instrumentalness",
        "valence", "tempo", "popularity"
    ]
    correlations = (
        filtered[numeric].corr()["popularity"]
        .sort_values(ascending=False)
        .to_frame("Correlation")
    )
    st.dataframe(correlations.round(3), use_container_width=True)

with tab4:
    st.subheader("🏆 Most Popular Songs")

    n = st.slider("Number of songs to display", 5, 20, 10)

    top = filtered.nlargest(n, "popularity")[
        ["track_name", "artist_name", "genre", "release_year", "popularity"]
    ]

    st.dataframe(top, use_container_width=True, hide_index=True)

    st.subheader("Popularity Comparison")
    fig, ax = plt.subplots(figsize=(10, 5))
    labels = top["track_name"].str[:22]
    ax.barh(labels[::-1], top["popularity"].iloc[::-1])
    ax.set_xlabel("Popularity")
    ax.set_title(f"Top {n} Songs by Popularity")
    fig.tight_layout()
    st.pyplot(fig)

st.divider()
st.caption(
    "EDA note: Correlation indicates association and does not establish causation. "
    "This project is designed for educational/miniproject use."
)
