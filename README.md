# 🍽️ Restaurant Reservation App

Une application de réservation en ligne pour un restaurant à forte capacité (200–250 couverts par service), développée avec Django.

---

## 📚 Objectif

Créer une solution complète pour gérer les réservations clients dans un restaurant à grande superficie, avec forte affluence. Le projet servira à la fois de support d'apprentissage (Python, Django, API REST, frontend JS) et de vitrine professionnelle.

---

## 🚀 Stack technique

### Backend
- 🐍 Python 3
- 🌐 Django 5.x
- 🧩 Django REST Framework (API)
- 🗃️ PostgreSQL (ou SQLite en dev)
- 🔐 Authentification JWT (à venir)

### Frontend
- 🖼️ HTML/CSS (base)
- ⚙️ JavaScript Vanilla (puis React plus tard)
- 🎨 TailwindCSS ou Bootstrap (au choix)

### DevOps & Productivité
- 🐙 Git / GitHub
- 🧪 Tests unitaires Django
- 📦 Docker (à envisager plus tard)
- 🧠 Projet pédagogique Holberton-aligned

---

## 🧱 Fonctionnalités prévues

### Côté client
- Réservation d’une table à une date et une heure
- Nombre de couverts
- Visualisation des créneaux disponibles
- Email de confirmation (plus tard)

### Côté staff/admin
- Vue d’ensemble des réservations par service
- Gestion manuelle (ajout/suppression)
- Interface admin Django (personnalisée plus tard)

---

## 📁 Arborescence projet (prévisionnelle)

```bash
restaurant-reservation/
├── backend/
│   ├── manage.py
│   ├── reservation_project/
│   ├── reservations/  ← app principale
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── js/
│   └── css/
└── README.md
