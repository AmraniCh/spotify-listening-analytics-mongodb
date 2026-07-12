// =====================================================
// CRUD — collection "ecoutes"
// Exécution : docker exec -i mongo mongosh streaming < queries/crud.js
// =====================================================

// -----------------------------------------------------
// CREATE — ajouter une nouvelle écoute
// -----------------------------------------------------
db.ecoutes.insertOne({
  _id: "eco_99998",
  id_utilisateur: "user_01",
  spotify_track_uri: "0eGsygTp906u18L0Oimnem",
  morceau: {
    titre: "Mr. Brightside",
    artiste: "The Killers",
    album: "Hot Fuss",
    genre: "indie"
  },
  plateforme: "android",
  ms_played: 222000,
  reason_start: "clickrow",
  reason_end: "trackdone",
  shuffle: false,
  skipped: false,
  date_ecoute: ISODate("2024-12-16T10:30:00Z")
});

// -----------------------------------------------------
// READ — rechercher les écoutes
// -----------------------------------------------------
// ... par artisteid_
db.ecoutes.find({ "morceau.artiste": "The Killers" }).limit(5);
db.ecoutes.countDocuments({ "morceau.artiste": "The Killers" });

// ... par genre
db.ecoutes.find({ "morceau.genre": "rock" }).limit(5);
db.ecoutes.countDocuments({ "morceau.genre": "rock" });

// ... par période (année 2024)
db.ecoutes.countDocuments({
  date_ecoute: {
    $gte: ISODate("2024-01-01"),
    $lt: ISODate("2025-01-01")
  }
});

// -----------------------------------------------------
// UPDATE — modifier les métadonnées d'un morceau
//
// Le morceau étant imbriqué, ses métadonnées sont dupliquées
// dans chaque écoute : la correction touche donc N documents.
// C'est le coût assumé du choix d'imbrication.
// -----------------------------------------------------
db.ecoutes.updateMany(
  { spotify_track_uri: "0eGsygTp906u18L0Oimnem" },
  { $set: { "morceau.genre": "alternative" } }
);

// -----------------------------------------------------
// DELETE — supprimer les écoutes d'un utilisateur
//
// MongoDB ne fait aucune cascade : le document de la collection
// "utilisateurs" reste intact et doit être supprimé séparément.
// -----------------------------------------------------
db.ecoutes.deleteMany({ id_utilisateur: "user_16" });
db.utilisateurs.deleteOne({ _id: "user_16" });