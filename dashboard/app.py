import altair as alt
import streamlit as st
from mongo_queries import kpis, monthly_evolution, top_tracks, top_artists, listening_time_by_genre

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

tab1, tab2, tab3 = st.tabs(["Vue d'ensemble", "Genres & temps", "Utilisateurs"])

with tab1:
    k = kpis()

    c1, c2, c3, c4 = st.columns(4, gap="medium")
    c1.metric(":material/play_circle: Écoutes", f"{k['ecoutes']:,}".replace(",", " "), border=True)
    c2.metric(":material/mic: Artistes", f"{k['artistes']:,}".replace(",", " "), border=True)
    c3.metric(":material/music_note: Morceaux", f"{k['morceaux']:,}".replace(",", " "), border=True)
    c4.metric(":material/schedule: Heures écoutées", f"{k['heures']:,.0f}".replace(",", " "), border=True)

    st.divider()

    st.subheader("Évolution des écoutes")

    df_monthly = monthly_evolution()

    chart_monthly = (
        alt.Chart(df_monthly)
        .mark_area(
            line={"color": "#c7f9d9", "strokeWidth": 2},
            color=alt.Gradient(
                gradient="linear",
                stops=[
                    alt.GradientStop(color="#FFFFFF", offset=0),
                    alt.GradientStop(color="#c7f9d9", offset=1),
                ],
                x1=1, x2=1, y1=1, y2=0,
            ),
            opacity=0.35,
        )
        .encode(
            x=alt.X("date:T", title=None, axis=alt.Axis(format="%b %Y")),
            y=alt.Y("nb_ecoutes:Q", title=None),
            tooltip=[
                alt.Tooltip("date:T", title="Mois", format="%B %Y"),
                alt.Tooltip("nb_ecoutes:Q", title="Écoutes"),
            ],
        )
        .properties(height=280)
        .configure_axis(grid=False, domain=False, ticks=False)
        .configure_view(stroke=None)
    )

    st.altair_chart(chart_monthly, use_container_width=True)
 
    left, right = st.columns(2, gap="large")

    with left:
        st.subheader("Top 10 morceaux")
        df_tracks = top_tracks()

        base = alt.Chart(df_tracks).encode(
            x=alt.X("nb_ecoutes:Q", title=None),
            y=alt.Y("titre:N", sort="-x", title=None),
            tooltip=["titre", "artiste", "nb_ecoutes"],
        )

        bars = base.mark_bar(color="#c7f9d9")
        labels = base.mark_text(align="left", dx=6).encode(text="nb_ecoutes:Q")

        chart_tracks = (
            (bars + labels)
            .properties(height=320)
            .configure_axis(grid=False, domain=False, ticks=False)
            .configure_view(stroke=None)
        )

        st.altair_chart(chart_tracks, use_container_width=True)


    with right:
        st.subheader("Top 10 artistes")
        
        df = top_artists()

        base = alt.Chart(df).encode(
            x=alt.X("nb_ecoutes:Q", title=None),
            y=alt.Y("artiste:N", sort="-x", title=None),
            tooltip=["artiste", "nb_ecoutes"],
        )

        bars = base.mark_bar(color="#c7f9d9")
        labels = base.mark_text(align="left", dx=6).encode(text="nb_ecoutes:Q")

        chart = (
            (bars + labels)
            .properties(height=320)
            .configure_axis(grid=False, domain=False, ticks=False)
            .configure_view(stroke=None)
        )

        st.altair_chart(chart, use_container_width=True)


with tab2:
    st.subheader("Temps d'écoute par genre")

    df_genre = listening_time_by_genre()

    base_genre = alt.Chart(df_genre).encode(
        x=alt.X("heures:Q", title=None, axis=None),
        y=alt.Y("genre:N", sort="-x", title=None),
        tooltip=[
            alt.Tooltip("genre", title="Genre"),
            alt.Tooltip("heures", title="Heures"),
        ],
    )

    bars_genre = base_genre.mark_bar(color="#c7f9d9", cornerRadiusEnd=4)
    labels_genre = base_genre.mark_text(align="left", dx=6, fontSize=12).encode(
        text=alt.Text("heures:Q", format=".0f")
    )

    chart_genre = (
        (bars_genre + labels_genre)
        .properties(height=520)
        .configure_axis(grid=False, domain=False, ticks=False)
        .configure_view(stroke=None)
    )

    st.altair_chart(chart_genre, use_container_width=True)

# with tab3:
#     # genre préféré par user + taux de réécoute
