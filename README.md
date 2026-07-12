# Setup

De zéro jusqu'au shell MongoDB.

## 1. Dépendances Python

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 2. Lancer MongoDB

```bash
docker run -d --name mongo -p 27017:27017 mongo:7
```

Une seule fois. Ensuite, `docker start mongo` suffit.

Vérifier qu'il tourne :

```bash
docker ps
```

## 3. Le pipeline

```bash
python scripts/build_documents.py
python scripts/import_mongodb.py
```

Sortie attendue :

```
ecoutes: 12000
utilisateurs: 16
```

## 4. Le shell MongoDB

```bash
docker exec -it mongo mongosh
```

```javascript
use streaming
db.ecoutes.countDocuments() // 12000
db.utilisateurs.countDocuments() // 16
db.ecoutes.findOne()
```

`exit` ou `Ctrl+D` pour sortir.

---

## En cas de problème

**`Connection refused`** — MongoDB ne tourne pas : `docker start mongo`

**`container name already in use`** — le conteneur existe déjà. Ne pas refaire
`docker run`, faire `docker start mongo`.

**`countDocuments()` renvoie 0** — relancer `python scripts/import_mongodb.py`.
Le script vide les collections avant d'insérer, il est rejouable sans risque.

**Repartir de zéro :**

```bash
docker exec -it mongo mongosh streaming --eval "db.dropDatabase()"
python scripts/import_mongodb.py
```