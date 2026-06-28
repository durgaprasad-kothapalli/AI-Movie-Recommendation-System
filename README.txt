# ── Setup & Run Instructions ────────────────────────────────────────────────
# AI-Based Movie Recommendation System
# ──────────────────────────────────────────────────────────────────────────────

## FOLDER STRUCTURE
movie_recommendation/
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── .env.example          ← copy to .env and edit
│   ├── ml/
│   │   ├── __init__.py
│   │   ├── data_loader.py    ← sample data built-in (no download needed)
│   │   ├── content_based.py
│   │   ├── collaborative.py
│   │   ├── hybrid.py
│   │   └── recommender.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── movies.py
│   │   ├── recommend.py
│   │   ├── ratings.py
│   │   └── watchlist.py
│   └── data/
│       └── movielens/        ← (optional) place MovieLens CSVs here
└── frontend/
    ├── package.json
    ├── vite.config.js
    ├── index.html
    ├── .env.example          ← copy to .env and edit
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── context/AuthContext.jsx
        ├── services/api.js
        ├── components/
        │   ├── Navbar.jsx
        │   ├── MovieCard.jsx
        │   ├── LoadingSpinner.jsx
        │   └── ProtectedRoute.jsx
        └── pages/
            ├── Home.jsx
            ├── Login.jsx
            ├── Register.jsx
            ├── MovieDetail.jsx
            ├── Search.jsx
            ├── Recommendations.jsx
            ├── Watchlist.jsx
            └── Profile.jsx

## PREREQUISITES
- Python 3.10+
- Node.js 18+
- MongoDB (running on localhost:27017)

## STEP 1 — Start MongoDB
Make sure MongoDB is running:
  mongod

## STEP 2 — Backend Setup
  cd backend
  copy .env.example .env        # Windows
  # cp .env.example .env         # Mac/Linux
  pip install -r requirements.txt
  python app.py

Backend runs at: http://localhost:5000

## STEP 3 — Frontend Setup (new terminal)
  cd frontend
  copy .env.example .env        # Windows
  # cp .env.example .env         # Mac/Linux
  npm install
  npm run dev

Frontend runs at: http://localhost:5173

## STEP 4 — (Optional) Use Real MovieLens Dataset
1. Download from: https://grouplens.org/datasets/movielens/
2. Unzip and copy movies.csv + ratings.csv into:
   backend/data/movielens/
3. Restart backend — it auto-detects the CSVs.

## API ENDPOINTS REFERENCE
POST   /register                       Register new user
POST   /login                          Login → JWT token
GET    /movies?q=&genre=&page=&limit=  List/search movies
GET    /movie/<id>                     Movie detail
GET    /movies/search?q=               Live search suggestions
GET    /movies/genres                  All genre labels
GET    /recommend/<id>?method=hybrid   Get recommendations
POST   /rate                           Submit star rating  [JWT]
GET    /ratings/<movie_id>             Average rating
GET    /ratings/user                   Your ratings        [JWT]
POST   /watchlist                      Add to watchlist    [JWT]
GET    /watchlist                      Your watchlist      [JWT]
DELETE /watchlist/<movie_id>           Remove from list    [JWT]
