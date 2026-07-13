import altair as alt
import streamlit as st
from mongo_queries import kpis, top_artists

st.set_page_config(page_title="Spotify Analytics", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Figtree', sans-serif;
    }

    .block-container { padding-top: 2.5rem; }

    h1 {
        color: #1DB954;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='color:#1DB954; margin-bottom:1.5rem;'>Spotify Listening Analytics</h1>",
    unsafe_allow_html=True,
)

k = kpis()

c1, c2, c3, c4 = st.columns(4, gap="medium")
c1.metric("Écoutes", f"{k['ecoutes']:,}".replace(",", " "), border=True)
c2.metric("Artistes", f"{k['artistes']:,}".replace(",", " "), border=True)
c3.metric("Morceaux", f"{k['morceaux']:,}".replace(",", " "), border=True)
c4.metric("Heures écoutées", f"{k['heures']:,.0f}".replace(",", " "), border=True)

st.divider()

# st.subheader("Top 10 artistes")

# df = top_artists()

# chart = (
#     alt.Chart(df)
#     .mark_bar(color="#1DB954")
#     .encode(
#         x=alt.X("nb_ecoutes:Q", title=None),
#         y=alt.Y("artiste:N", sort="-x", title=None),
#         tooltip=["artiste", "nb_ecoutes"],
#     )
#     .properties(height=320)
# )

# st.altair_chart(chart, use_container_width=True)