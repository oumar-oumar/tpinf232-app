from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
from flask_cors import CORS
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)
CORS(app)

# ----------------------------
# INITIALISATION BASE DE DONNÉES
# ----------------------------
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            age INTEGER,
            sexe TEXT,
            ville TEXT,
            temps INTEGER
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ----------------------------
# PAGE D'ACCUEIL (PUB)
# ----------------------------
@app.route("/")
def home_page():
    return render_template("home.html")

# ----------------------------
# PAGE COLLECTE
# ----------------------------
@app.route("/Collecte")
def collect_page():
    return render_template("index.html")

# ----------------------------
# DASHBOARD
# ----------------------------
@app.route("/dashboard")
def dashboard_page():
    return render_template("dashboard.html")

# ----------------------------
# AJOUT DONNÉES
# ----------------------------
@app.route("/add", methods=["POST"])
def add():
    data = request.json

    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("""
        INSERT INTO users (nom, age, sexe, ville, temps)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("nom"),
        int(data.get("age")),
        data.get("sexe"),
        data.get("ville"),
        int(data.get("temps"))
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "OK"})

# ----------------------------
# STATISTIQUES + ML
# ----------------------------
@app.route("/stats")
def stats():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    # ----- STATS -----
    c.execute("SELECT COUNT(*) FROM users")
    total = c.fetchone()[0]

    c.execute("SELECT AVG(age) FROM users")
    moyenneAge = c.fetchone()[0] or 0

    c.execute("SELECT AVG(temps) FROM users")
    moyenneTemps = c.fetchone()[0] or 0

    c.execute("SELECT COUNT(*) FROM users WHERE sexe='M'")
    hommes = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM users WHERE sexe='F'")
    femmes = c.fetchone()[0]

    # ----- DATA -----
    c.execute("SELECT age, temps FROM users")
    rows = c.fetchall()

    conn.close()

    # ----- REGRESSION -----
    n = len(rows)
    sum_x = sum_y = sum_xy = sum_x2 = 0

    for r in rows:
        x = float(r[0])
        y = float(r[1])

        sum_x += x
        sum_y += y
        sum_xy += x * y
        sum_x2 += x * x

    a = 0
    b = 0

    if n > 1:
        a = (n * sum_xy - sum_x * sum_y) / ((n * sum_x2) - (sum_x ** 2) + 0.0001)
        b = (sum_y - a * sum_x) / n

    # ----- INTERPRÉTATION -----
    if n > 1:
        if a > 0:
            trend = "📈 Relation positive"
        elif a < 0:
            trend = "📉 Relation négative"
        else:
            trend = "📊 Aucune relation"
    else:
        trend = "📊 Pas assez de données"

    # ----- CLASSIFICATION -----
    if moyenneTemps < 5:
        classe = "Utilisateur faible"
    elif moyenneTemps < 10:
        classe = "Utilisateur moyen"
    else:
        classe = "Utilisateur intensif"

    # ----- CLUSTERING -----
    clusters = []
    ages = []
    temps_list = []

    if len(rows) >= 3:
        X = np.array(rows)

        kmeans = KMeans(n_clusters=3, random_state=0, n_init=10)
        labels = kmeans.fit_predict(X)

        clusters = labels.tolist()

        for r in rows:
            ages.append(r[0])
            temps_list.append(r[1])

    return jsonify({
        "total": total,
        "moyenneAge": round(moyenneAge, 2),
        "moyenneTemps": round(moyenneTemps, 2),
        "hommes": hommes,
        "femmes": femmes,
        "regression": {
            "a": round(a, 2),
            "b": round(b, 2)
        },
        "trend": trend,
        "classe": classe,
        "clusters": clusters,
        "ages": ages,
        "temps_list": temps_list
    })

# ----------------------------
# DONNÉES BRUTES
# ----------------------------
@app.route("/data")
def get_data():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    rows = c.fetchall()

    conn.close()

    return jsonify(rows)

# ----------------------------
# DEBUG
# ----------------------------
@app.route("/debug")
def debug():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users")
    data = c.fetchall()

    conn.close()

    return jsonify(data)

@app.route("/search")
def search():
    q = request.args.get("q", "").lower().strip()

    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT nom, age, sexe, ville, temps FROM users")
    rows = c.fetchall()
    conn.close()

    if not q:
        return jsonify(rows)

    result = []

    for nom, age, sexe, ville, temps in rows:

        nom_l = str(nom).lower()
        ville_l = str(ville).lower()
        sexe_l = str(sexe).lower()
        age_l = str(age)
        temps_l = str(temps)

        # logique intelligente
        if (
            q in nom_l or
            q in ville_l or
            q == sexe_l or
            q == age_l or
            q == temps_l
        ):
            result.append([nom, age, sexe, ville, temps])

    return jsonify(result)
# ----------------------------
# LANCEMENT
# ----------------------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)