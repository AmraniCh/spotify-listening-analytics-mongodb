// =====================================================
// ANALYSES — collection "ecoutes"
// Exécution : docker exec -i mongo mongosh streaming < queries/analyses.js
// =====================================================

// -----------------------------------------------------
// 1. Morceaux les plus écoutés
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: { titre: "$morceau.titre", artiste: "$morceau.artiste" },
      nb_ecoutes: { $sum: 1 }
  } },
  { $sort: { nb_ecoutes: -1 } },
  { $limit: 10 }
]);

// -----------------------------------------------------
// 2. Temps total d'écoute par genre
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: "$morceau.genre",
      temps_total_ms: { $sum: "$ms_played" }
  } },
  { $sort: { temps_total_ms: -1 } }
]);

// -----------------------------------------------------
// 3. Artistes les plus écoutés
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: "$morceau.artiste",
      nb_ecoutes: { $sum: 1 }
  } },
  { $sort: { nb_ecoutes: -1 } },
  { $limit: 10 }
]);

// -----------------------------------------------------
// 4. Répartition des écoutes par plateforme
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: "$plateforme",
      nb_ecoutes: { $sum: 1 }
  } },
  { $sort: { nb_ecoutes: -1 } }
]);

// -----------------------------------------------------
// 5. Évolution des écoutes dans le temps (par mois)
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: { annee: { $year: "$date_ecoute" }, mois: { $month: "$date_ecoute" } },
      nb_ecoutes: { $sum: 1 }
  } },
  { $sort: { "_id.annee": 1, "_id.mois": 1 } }
]);

// =====================================================
// ANALYSES COMPLÉMENTAIRES (au moins 3 exigées)
// =====================================================

// -----------------------------------------------------
// 6. Genre préféré de chaque utilisateur
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: { utilisateur: "$id_utilisateur", genre: "$morceau.genre" },
      nb: { $sum: 1 }
  } },
  { $sort: { "_id.utilisateur": 1, nb: -1 } },
  { $group: {
      _id: "$_id.utilisateur",
      genre_prefere: { $first: "$_id.genre" },
      nb_ecoutes: { $first: "$nb" }
  } },
  { $sort: { _id: 1 } }
]);

// -----------------------------------------------------
// 7. Heures de forte écoute
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: { $hour: "$date_ecoute" },
      nb_ecoutes: { $sum: 1 }
  } },
  { $sort: { nb_ecoutes: -1 } }
]);

// -----------------------------------------------------
// 8. Taux de réécoute des morceaux les plus populaires
// -----------------------------------------------------
db.ecoutes.aggregate([
  { $group: {
      _id: { titre: "$morceau.titre", artiste: "$morceau.artiste" },
      nb_ecoutes: { $sum: 1 },
      utilisateurs_distincts: { $addToSet: "$id_utilisateur" }
  } },
  { $project: {
      nb_ecoutes: 1,
      nb_utilisateurs: { $size: "$utilisateurs_distincts" },
      taux_reecoute: { $divide: ["$nb_ecoutes", { $size: "$utilisateurs_distincts" }] }
  } },
  { $sort: { nb_ecoutes: -1 } },
  { $limit: 10 }
]);
