# 📊 Data Analysis Web App

## 🚀 Description

Cette application web permet de :

* Collecter des données utilisateurs
* Stocker les informations dans une base SQLite
* Analyser les données automatiquement
* Visualiser les résultats avec des graphiques interactifs
* Générer un rapport PDF

L'application utilise des techniques simples de **statistiques et de Machine Learning** (régression, clustering).

---

## 🧰 Technologies utilisées

### 🔹 Backend

* Python
* Flask
* SQLite
* NumPy

### 🔹 Frontend

* HTML / CSS / JavaScript
* Chart.js

### 🔹 Autres outils

* jsPDF (export PDF)
* html2canvas (capture graphique)

---

## 📂 Structure du projet

```
tpinf232-app/
│
├── app.py
├── requirements.txt
├── data.db
│
├── templates/
│   ├── home.html
│   ├── index.html
│   ├── dashboard.html
│
└── static/
```

---

## ⚙️ Installation locale

### 1. Cloner le projet

```
git clone https://github.com/ton-username/tpinf232-app.git
cd tpinf232-app
```

---

### 2. Installer les dépendances

```
pip install -r requirements.txt
```

---

### 3. Lancer l'application

```
python app.py
```

---

### 4. Accéder à l'application

```
http://127.0.0.1:5000
```

---

## 🌐 Déploiement

L'application est déployée en ligne via Render.

---

## 📊 Fonctionnalités principales

* 📝 Formulaire de collecte de données
* 📈 Dashboard avec statistiques
* 🔎 Recherche dynamique (nom, ville, âge, sexe)
* 📉 Régression linéaire
* 📊 Clustering des utilisateurs
* 📄 Export PDF automatique

---

## 🧠 Machine Learning utilisé

* Régression linéaire (relation âge / temps téléphone)
* Classification utilisateur (faible, moyen, intensif)
* Clustering (K-Means)

---

## 📸 Aperçu

* Page d'accueil
* Formulaire de collecte
* Dashboard interactif

---

## 👨‍💻 Auteur

**Oumarou MVONGO Caleb Israel**
Université de Yaoundé I
Département Informatique

---

## 📌 Remarques

* Le Machine Learning peut être limité en production selon l’environnement
* SQLite est utilisé pour la simplicité (non adapté à grande échelle)

---

## ⭐ Améliorations futures

* Authentification utilisateur
* Base de données distante (PostgreSQL)
* API REST complète
* Amélioration des modèles ML
* Interface UI/UX avancée

---
