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
    
    [data-testid="stMetric"] {
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.4rem;
        font-weight: 600;
    }

    [data-testid="stMetricLabel"] p {
        font-size: 0.95rem;
        opacity: 0.65;
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
c1.metric(":material/play_circle: Écoutes", f"{k['ecoutes']:,}".replace(",", " "), border=True)
c2.metric(":material/mic: Artistes", f"{k['artistes']:,}".replace(",", " "), border=True)
c3.metric(":material/music_note: Morceaux", f"{k['morceaux']:,}".replace(",", " "), border=True)
c4.metric(":material/schedule: Heures écoutées", f"{k['heures']:,.0f}".replace(",", " "), border=True)

st.divider()

st.subheader("Top 10 artistes")

df = top_artists()

base = alt.Chart(df).encode(
    x=alt.X("nb_ecoutes:Q", title=None),
    y=alt.Y("artiste:N", sort="-x", title=None),
    tooltip=["artiste", "nb_ecoutes"],
)

bars = base.mark_bar(color="#89F2AE79")
labels = base.mark_text(align="left", dx=6).encode(text="nb_ecoutes:Q")

chart = (
    (bars + labels)
    .properties(height=320)
    .configure_axis(grid=False, domain=False, ticks=False)
    .configure_view(stroke=None)
)

st.altair_chart(chart, use_container_width=True)