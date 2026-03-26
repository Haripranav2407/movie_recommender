import streamlit as st
import pandas as pd

st.set_page_config(page_title="Movie Recommender", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("movies.csv")

movies = load_data()

st.title("🎬 Movie Recommendation System")
st.caption("Discover movies based on your preferences")

st.divider()

st.sidebar.title("🔍 Filter Movies")

with st.sidebar.expander("Search & Filter", expanded=True):
    search = st.text_input("Search Movie")

    genre = st.selectbox(
        "Genre",
        ["All"] + sorted(movies["genre"].unique())
    )

    platform = st.multiselect(
        "Streaming Platform",
        sorted(movies["platform"].unique())
    )

    year = st.slider(
        "Minimum Year",
        int(movies["year"].min()),
        int(movies["year"].max()),
        int(movies["year"].min())
    )

    rating = st.slider(
        "Minimum Rating",
        float(movies["rating"].min()),
        float(movies["rating"].max()),
        5.0
    )

sort_option = st.sidebar.radio(
    "Sort By",
    ["Rating (High to Low)", "Year (Latest)"]
)

top_n = st.sidebar.slider(
    "Number of movies to display",
    4, 150, 20
)

filtered = movies.copy()

if search:
    filtered = filtered[
        filtered["title"].str.contains(search, case=False)
    ]

if genre != "All":
    filtered = filtered[filtered["genre"] == genre]

if platform:
    filtered = filtered[filtered["platform"].isin(platform)]

filtered = filtered[
    (filtered["year"] >= year) &
    (filtered["rating"] >= rating)
]

if sort_option == "Rating (High to Low)":
    filtered = filtered.sort_values(by="rating", ascending=False)
else:
    filtered = filtered.sort_values(by="year", ascending=False)

st.subheader(f"🎥 Showing {len(filtered)} Movies")
st.divider()

cols = st.columns(4)

for i, row in filtered.head(top_n).iterrows():
    with cols[i % 4]:
        with st.container(border=True):
            st.subheader(row['title'])

            col1, col2 = st.columns(2)
            col1.metric("⭐ Rating", row['rating'])
            col2.metric("📅 Year", row['year'])

            st.caption(f"🎭 Genre: {row['genre']}")
            st.caption(f"📺 Platform: {row['platform']}")

if len(filtered) == 0:
    st.warning("No movies found. Try adjusting filters.")
