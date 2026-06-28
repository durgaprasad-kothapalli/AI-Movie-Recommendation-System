import pandas as pd
import os

# ── Sample movie catalogue (fallback when MovieLens CSVs are absent) ─────────
SAMPLE_MOVIES = [
    {"movieId": 1,  "title": "The Shawshank Redemption", "genres": "Drama"},
    {"movieId": 2,  "title": "The Godfather",             "genres": "Crime|Drama"},
    {"movieId": 3,  "title": "The Dark Knight",            "genres": "Action|Crime|Drama"},
    {"movieId": 4,  "title": "Pulp Fiction",               "genres": "Crime|Drama"},
    {"movieId": 5,  "title": "Schindler's List",           "genres": "Biography|Drama|History"},
    {"movieId": 6,  "title": "The Lord of the Rings",      "genres": "Adventure|Drama|Fantasy"},
    {"movieId": 7,  "title": "Fight Club",                 "genres": "Drama|Mystery|Thriller"},
    {"movieId": 8,  "title": "Forrest Gump",               "genres": "Drama|Romance"},
    {"movieId": 9,  "title": "Inception",                  "genres": "Action|Adventure|Sci-Fi|Thriller"},
    {"movieId": 10, "title": "The Matrix",                 "genres": "Action|Sci-Fi"},
    {"movieId": 11, "title": "Goodfellas",                 "genres": "Biography|Crime|Drama"},
    {"movieId": 12, "title": "Interstellar",               "genres": "Adventure|Drama|Sci-Fi"},
    {"movieId": 13, "title": "The Silence of the Lambs",   "genres": "Crime|Drama|Thriller"},
    {"movieId": 14, "title": "Parasite",                   "genres": "Drama|Thriller"},
    {"movieId": 15, "title": "Avengers: Endgame",          "genres": "Action|Adventure|Sci-Fi"},
    {"movieId": 16, "title": "The Lion King",              "genres": "Animation|Adventure|Drama"},
    {"movieId": 17, "title": "Toy Story",                  "genres": "Animation|Adventure|Comedy"},
    {"movieId": 18, "title": "The Prestige",               "genres": "Drama|Mystery|Sci-Fi|Thriller"},
    {"movieId": 19, "title": "Whiplash",                   "genres": "Drama|Music"},
    {"movieId": 20, "title": "La La Land",                 "genres": "Drama|Music|Romance"},
    {"movieId": 21, "title": "Mad Max: Fury Road",         "genres": "Action|Adventure|Sci-Fi"},
    {"movieId": 22, "title": "Blade Runner 2049",          "genres": "Drama|Mystery|Sci-Fi|Thriller"},
    {"movieId": 23, "title": "Get Out",                    "genres": "Horror|Mystery|Thriller"},
    {"movieId": 24, "title": "Black Panther",              "genres": "Action|Adventure|Sci-Fi"},
    {"movieId": 25, "title": "Spider-Man: Into the Spider-Verse", "genres": "Animation|Action|Adventure"},
    {"movieId": 26, "title": "Joker",                     "genres": "Crime|Drama|Thriller"},
    {"movieId": 27, "title": "1917",                       "genres": "Drama|War"},
    {"movieId": 28, "title": "Knives Out",                 "genres": "Comedy|Crime|Drama|Mystery"},
    {"movieId": 29, "title": "The Grand Budapest Hotel",   "genres": "Adventure|Comedy|Crime|Drama"},
    {"movieId": 30, "title": "Dune",                       "genres": "Adventure|Drama|Sci-Fi"},
]

SAMPLE_RATINGS = [
    # user 1 — likes drama and crime
    {"userId": 1, "movieId": 1, "rating": 5.0},
    {"userId": 1, "movieId": 2, "rating": 4.5},
    {"userId": 1, "movieId": 4, "rating": 4.0},
    {"userId": 1, "movieId": 11,"rating": 4.5},
    {"userId": 1, "movieId": 13,"rating": 3.5},
    # user 2 — likes sci-fi/action
    {"userId": 2, "movieId": 9, "rating": 5.0},
    {"userId": 2, "movieId": 10,"rating": 5.0},
    {"userId": 2, "movieId": 12,"rating": 4.5},
    {"userId": 2, "movieId": 15,"rating": 4.0},
    {"userId": 2, "movieId": 21,"rating": 3.5},
    # user 3 — mixed
    {"userId": 3, "movieId": 1, "rating": 4.0},
    {"userId": 3, "movieId": 8, "rating": 5.0},
    {"userId": 3, "movieId": 17,"rating": 4.5},
    {"userId": 3, "movieId": 20,"rating": 4.0},
    {"userId": 3, "movieId": 19,"rating": 4.5},
    # user 4 — animation + adventure
    {"userId": 4, "movieId": 16,"rating": 5.0},
    {"userId": 4, "movieId": 17,"rating": 5.0},
    {"userId": 4, "movieId": 25,"rating": 4.5},
    {"userId": 4, "movieId": 6, "rating": 4.0},
    # user 5 — thriller / mystery
    {"userId": 5, "movieId": 7, "rating": 5.0},
    {"userId": 5, "movieId": 13,"rating": 4.5},
    {"userId": 5, "movieId": 18,"rating": 4.5},
    {"userId": 5, "movieId": 23,"rating": 4.0},
    {"userId": 5, "movieId": 28,"rating": 4.0},
]

POSTERS = {
    1:  "https://image.tmdb.org/t/p/w500/q6y0Go1tsGEsmtFryDOJo3dEmqu.jpg",
    2:  "https://image.tmdb.org/t/p/w500/3bhkrj58Vtu7enYsLLeHjnhFNNB.jpg",
    3:  "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    4:  "https://image.tmdb.org/t/p/w500/dM2w364MScsjFf8pfMbaWUcWrR.jpg",
    5:  "https://image.tmdb.org/t/p/w500/sF1U4EUQS8YHUYjNl3pMGNIQyr0.jpg",
    6:  "https://image.tmdb.org/t/p/w500/6oom5QYQ2yQTMJIbnvbkBL9cHo6.jpg",
    7:  "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
    8:  "https://image.tmdb.org/t/p/w500/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
    9:  "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
    10: "https://image.tmdb.org/t/p/w500/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
    11: "https://image.tmdb.org/t/p/w500/aKuFiU82s5ISJpGZp7YkIr3kCUd.jpg",
    12: "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
    13: "https://image.tmdb.org/t/p/w500/uS9m8OBk1A8eM9I042bx8XXpqAq.jpg",
    14: "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
    15: "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
    16: "https://image.tmdb.org/t/p/w500/sIyd6XjbCSaHlSKWkHoQlHSFcHB.jpg",
    17: "https://image.tmdb.org/t/p/w500/uXDfjJbdP4ijW5hWSBrPrlKpxab.jpg",
    18: "https://image.tmdb.org/t/p/w500/bdN3gXuIZYaJP6PTHrMHMEo0BXp.jpg",
    19: "https://image.tmdb.org/t/p/w500/7fn624j5lj3xTme2SgiLCeuedmO.jpg",
    20: "https://image.tmdb.org/t/p/w500/uDO8zWDhfWwoFdKS4fzkUJt0Rf0.jpg",
    21: "https://image.tmdb.org/t/p/w500/8tZYtuWezp8JbcsvHYO0O46tFbo.jpg",
    22: "https://image.tmdb.org/t/p/w500/gajva2L0rPYkEWjzgFlBXCAVBE5.jpg",
    23: "https://image.tmdb.org/t/p/w500/tFXcEccSQMf3lfhfXKSU9iRBpa3.jpg",
    24: "https://image.tmdb.org/t/p/w500/uxzzxijgPIY7slzFvMotPv8wjKA.jpg",
    25: "https://image.tmdb.org/t/p/w500/iiZZdoQBEYBv6id8su7ImL0oCbD.jpg",
    26: "https://image.tmdb.org/t/p/w500/udDclJoHjfjb8Ekgsd4FDteOkCU.jpg",
    27: "https://image.tmdb.org/t/p/w500/iZf0KyrE25z1sage4SYQLUcDTeE.jpg",
    28: "https://image.tmdb.org/t/p/w500/pThyQovXQrqVedERGrBqXDFOrqa.jpg",
    29: "https://image.tmdb.org/t/p/w500/eWdyYQreja6JGCzqHWXpWHDrrPo.jpg",
    30: "https://image.tmdb.org/t/p/w500/d5NXSklpcKDlFOFmtQPmOs3Udhd.jpg",
}

DESCRIPTIONS = {
    1: "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
    2: "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
    3: "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests.",
    4: "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption.",
    5: "In German-occupied Poland, industrialist Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution.",
    6: "A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth.",
    7: "An insomniac office worker and a devil-may-care soapmaker form an underground fight club that evolves into something much more.",
    8: "The presidencies of Kennedy and Johnson, the Vietnam War, and other historical events unfold from the perspective of an Alabama man with an IQ of 75.",
    9: "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
    10: "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.",
    11: "The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen Hill and his mob partners Jimmy Conway and Tommy DeVito.",
    12: "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
    13: "A young F.B.I. cadet must receive the help of an incarcerated and manipulative cannibal killer to help catch another serial killer.",
    14: "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.",
    15: "After the devastating events of Avengers: Infinity War, the universe is in ruins. The Avengers assemble once more to reverse Thanos's actions.",
    16: "Lion prince Simba and his father are targeted by his bitter uncle, who wants to ascend the throne himself.",
    17: "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.",
    18: "After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion while sacrificing everything they have to outwit each other.",
    19: "A promising young drummer enrolls at a cut-throat music conservatory where his dreams of greatness are mentored by an instructor who will stop at nothing to realize a student's potential.",
    20: "While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.",
    21: "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search for her homeland with the aid of a group of female prisoners, a psychotic worshiper, and a drifter named Max.",
    22: "A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard, who's been missing for thirty years.",
    23: "A young African-American visits his white girlfriend's parents for the weekend, where his simmering uneasiness about their reception of him eventually reaches a boiling point.",
    24: "T'Challa, heir to the hidden but advanced kingdom of Wakanda, must step forward to lead his people into a new future and must confront a challenger from his country's past.",
    25: "Teen Miles Morales becomes the Spider-Man of his universe, and must join with five spider-powered individuals from other dimensions to stop a threat for all realities.",
    26: "A mentally troubled musician and wannabe comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime.",
    27: "April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap.",
    28: "A detective investigates the death of a patriarch of an eccentric, combative family.",
    29: "A writer encounters the owner of an aging high-class hotel, who tells him of his early years serving as a lobby boy in the hotel's glorious years under an exceptional concierge.",
    30: "Feature adaptation of Frank Herbert's science fiction novel about the son of a noble family entrusted with the protection of the most valuable asset and most vital element in the galaxy.",
}


def load_movies() -> pd.DataFrame:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "movielens", "movies.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
    else:
        df = pd.DataFrame(SAMPLE_MOVIES)
    # Add poster + description
    df["poster_url"]   = df["movieId"].map(POSTERS).fillna(
        "https://via.placeholder.com/300x450?text=No+Poster")
    df["description"]  = df["movieId"].map(DESCRIPTIONS).fillna("No description available.")
    df["release_year"] = df["title"].str.extract(r"\((\d{4})\)$").fillna("N/A")
    df["title"]        = df["title"].str.replace(r"\s*\(\d{4}\)$", "", regex=True)
    return df.reset_index(drop=True)


def load_ratings() -> pd.DataFrame:
    path = os.path.join(os.path.dirname(__file__), "..", "data", "movielens", "ratings.csv")
    if os.path.exists(path):
        df = pd.read_csv(path)
        return df[["userId", "movieId", "rating"]]
    return pd.DataFrame(SAMPLE_RATINGS)
