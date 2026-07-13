import pandas as pd
import streamlit as st
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "streaming"


@st.cache_resource
def get_db():
    return MongoClient(MONGO_URI)[DB_NAME]

# Key Performance Indicato
@st.cache_data
def kpis() -> dict:
    pipeline = [
        {"$group": {
            "_id": None,
            "ecoutes": {"$sum": 1},
            "ms_total": {"$sum": "$ms_played"},
            "artistes": {"$addToSet": "$morceau.artiste"},
            "morceaux": {"$addToSet": "$spotify_track_uri"},
        }},
        {"$project": {
            "_id": 0,
            "ecoutes": 1,
            "heures": {"$divide": ["$ms_total", 3600000]},
            "artistes": {"$size": "$artistes"},
            "morceaux": {"$size": "$morceaux"},
        }},
    ]
    return list(get_db().ecoutes.aggregate(pipeline))[0]

@st.cache_data
def monthly_evolution() -> pd.DataFrame:
    pipeline = [
        {"$group": {
            "_id": {"annee": {"$year": "$date_ecoute"}, "mois": {"$month": "$date_ecoute"}},
            "nb_ecoutes": {"$sum": 1},
        }},
        {"$sort": {"_id.annee": 1, "_id.mois": 1}},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    df = pd.DataFrame([
        {"year": r["_id"]["annee"], "month": r["_id"]["mois"], "nb_ecoutes": r["nb_ecoutes"]}
        for r in rows
    ])
    df["date"] = pd.to_datetime(df.assign(day=1)[["year", "month", "day"]])
    return df

@st.cache_data
def top_tracks(limit: int = 10) -> pd.DataFrame:
    pipeline = [
        {"$group": {
            "_id": {"titre": "$morceau.titre", "artiste": "$morceau.artiste"},
            "nb_ecoutes": {"$sum": 1},
        }},
        {"$sort": {"nb_ecoutes": -1}},
        {"$limit": limit},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame([
        {
            "titre": r["_id"]["titre"],
            "artiste": r["_id"]["artiste"],
            "nb_ecoutes": r["nb_ecoutes"],
        }
        for r in rows
    ])

@st.cache_data
def top_artists(limit: int = 10) -> pd.DataFrame:
    pipeline = [
        {"$group": {"_id": "$morceau.artiste", "nb_ecoutes": {"$sum": 1}}},
        {"$sort": {"nb_ecoutes": -1}},
        {"$limit": limit},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame(
        [{"artiste": r["_id"], "nb_ecoutes": r["nb_ecoutes"]} for r in rows]
    )


@st.cache_data
def listening_time_by_genre() -> pd.DataFrame:
    pipeline = [
        {"$group": {"_id": "$morceau.genre", "temps_total_ms": {"$sum": "$ms_played"}}},
        {"$sort": {"temps_total_ms": -1}},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame([
        {"genre": r["_id"], "heures": round(r["temps_total_ms"] / 3_600_000, 1)}
        for r in rows
    ])

@st.cache_data
def listens_by_hour() -> pd.DataFrame:
    pipeline = [
        {"$group": {"_id": {"$hour": "$date_ecoute"}, "nb_ecoutes": {"$sum": 1}}},
        {"$sort": {"_id": 1}},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return (
        pd.DataFrame([{"heure": r["_id"], "nb_ecoutes": r["nb_ecoutes"]} for r in rows])
        .set_index("heure")
        .reindex(range(24), fill_value=0)
        .reset_index()
    )

@st.cache_data
def platform_split() -> pd.DataFrame:
    pipeline = [
        {"$group": {"_id": "$plateforme", "nb_ecoutes": {"$sum": 1}}},
        {"$sort": {"nb_ecoutes": -1}},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame([
        {"plateforme": r["_id"], "nb_ecoutes": r["nb_ecoutes"]} for r in rows
    ])

@st.cache_data
def favorite_genre_per_user() -> pd.DataFrame:
    pipeline = [
        {"$group": {
            "_id": {"utilisateur": "$id_utilisateur", "genre": "$morceau.genre"},
            "nb": {"$sum": 1},
        }},
        {"$sort": {"_id.utilisateur": 1, "nb": -1}},
        {"$group": {
            "_id": "$_id.utilisateur",
            "genre_prefere": {"$first": "$_id.genre"},
            "nb_ecoutes": {"$first": "$nb"},
        }},
        {"$sort": {"_id": 1}},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame([
        {
            "utilisateur": r["_id"],
            "genre_prefere": r["genre_prefere"],
            "nb_ecoutes": r["nb_ecoutes"],
        }
        for r in rows
    ])

@st.cache_data
def replay_rate(limit: int = 10) -> pd.DataFrame:
    pipeline = [
        {"$group": {
            "_id": {"titre": "$morceau.titre", "artiste": "$morceau.artiste"},
            "nb_ecoutes": {"$sum": 1},
            "utilisateurs_distincts": {"$addToSet": "$id_utilisateur"},
        }},
        {"$project": {
            "nb_ecoutes": 1,
            "nb_utilisateurs": {"$size": "$utilisateurs_distincts"},
            "taux_reecoute": {
                "$divide": ["$nb_ecoutes", {"$size": "$utilisateurs_distincts"}]
            },
        }},
        {"$sort": {"nb_ecoutes": -1}},
        {"$limit": limit},
    ]
    rows = list(get_db().ecoutes.aggregate(pipeline))
    return pd.DataFrame([
        {
            "titre": r["_id"]["titre"],
            "artiste": r["_id"]["artiste"],
            "nb_ecoutes": r["nb_ecoutes"],
            "nb_utilisateurs": r["nb_utilisateurs"],
            "taux_reecoute": round(r["taux_reecoute"], 2),
        }
        for r in rows
    ])