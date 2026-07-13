db.ecoutes.find({ "morceau.artiste": "The Killers" }).explain("executionStats");

db.ecoutes.createIndex({ "morceau.artiste": 1 });
db.ecoutes.createIndex({ "date_ecoute": 1 });
db.ecoutes.createIndex({ "id_utilisateur": 1 });
db.ecoutes.createIndex({ "morceau.genre": 1 });

db.ecoutes.getIndexes();

db.ecoutes.find({ "morceau.artiste": "The Killers" }).explain("executionStats");
