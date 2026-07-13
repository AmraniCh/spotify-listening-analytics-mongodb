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