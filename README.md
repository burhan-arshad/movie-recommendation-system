# CineMatch

## Content-Based Movie Recommendation System

CineMatch is an end-to-end movie recommendation system that combines a locally trained TF-IDF content-based recommendation engine with the TMDB API to provide movie search, movie details, and movie recommendations.

The system uses TF-IDF vectorization and cosine similarity to identify movies with similar content based on movie metadata.

Built with Python, FastAPI, Streamlit, Scikit-learn, and the TMDB API.

---

## Live Demo

Frontend: https://movie-recommendation-system-burhan.streamlit.app/

Backend API: YOUR_FASTAPI_URL

---

## Features

* Movie search using TMDB
* Movie posters and release information
* Detailed movie information
* Content-based movie recommendations
* TF-IDF similarity recommendations
* Genre-based recommendations
* TMDB ratings
* FastAPI REST API
* Streamlit frontend
* Interactive FastAPI documentation
* Precomputed recommendation artifacts
* Separate frontend and backend architecture

---

## How It Works

CineMatch uses a two-part architecture.

The Streamlit frontend provides the user interface and sends requests to the FastAPI backend.

The FastAPI backend handles the recommendation engine and communicates with the TMDB API.

Architecture:

User → Streamlit Frontend → FastAPI Backend → TF-IDF Recommendation Engine

The FastAPI backend also communicates with the TMDB API to retrieve movie information, posters, ratings, genres, and search results.

---

## Recommendation Pipeline

Movie Metadata
→ Text Feature Preparation
→ TF-IDF Vectorization
→ TF-IDF Matrix
→ Cosine Similarity
→ Similar Movies

For a selected movie, its TF-IDF vector is compared with the vectors of other movies.

Movies with higher cosine similarity scores are considered more similar.

---

## Technologies Used

### Programming Language

* Python

### Machine Learning

* TF-IDF Vectorization
* Cosine Similarity
* Content-Based Recommendation

### Backend

* FastAPI
* Uvicorn
* HTTPX
* Pandas
* NumPy
* Scikit-learn

### Frontend

* Streamlit
* Requests

### External API

* TMDB API

---

## Project Structure

CineMatch/
├── app.py
├── main.py
├── Movie.ipynb
├── df.pkl
├── indices.pkl
├── tfidf.pkl
├── tfidf_matrix.pkl
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md

The following files are intentionally excluded from the repository:

* .env
* movies_metadata.csv
* **pycache**/

The .env file contains secrets, while the raw dataset is not required at runtime because the processed recommendation artifacts have already been generated.

---

## Important Files

### app.py

Streamlit frontend responsible for:

* Movie search
* Movie selection
* Movie posters
* Movie details
* TF-IDF recommendations
* Genre recommendations

### main.py

FastAPI backend responsible for:

* TMDB movie search
* Movie details
* Popular movies
* Genre recommendations
* TF-IDF recommendations
* Combined movie recommendation results

### df.pkl

Processed movie dataframe used by the recommendation engine.

### indices.pkl

Mapping between movie titles and their corresponding positions in the TF-IDF matrix.

### tfidf.pkl

Saved TF-IDF vectorizer used during model development.

### tfidf_matrix.pkl

Precomputed TF-IDF matrix containing vector representations of the movies.

### Movie.ipynb

Development notebook containing the data preparation, TF-IDF vectorization, cosine similarity, and recommendation pipeline used to generate the saved artifacts.

---

## API Endpoints

### Health Check

GET /health

Returns the current backend status.

### Home Movies

GET /home

Supported categories:

* popular
* top_rated
* upcoming
* now_playing
* trending

Example:

/home?category=popular&limit=18

### TMDB Movie Search

GET /tmdb/search

Example:

/tmdb/search?query=Inception

### Movie Details

GET /movie/id/{tmdb_id}

Example:

/movie/id/27205

### TF-IDF Recommendations

GET /recommend/tfidf

Example:

/recommend/tfidf?title=Inception&top_n=10

### Genre Recommendations

GET /recommend/genre

Example:

/recommend/genre?tmdb_id=27205&limit=10

### Combined Movie Search

GET /movie/search

Example:

/movie/search?query=Inception

This endpoint combines:

* TMDB movie details
* TF-IDF recommendations
* Genre recommendations

---

## Local Setup

### 1. Clone the Repository

git clone https://github.com/burhan-arshad24/CineMatch.git

cd CineMatch

### 2. Create a Virtual Environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate

Linux/macOS:

python3 -m venv .venv

source .venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure the TMDB API Key

Create a .env file in the project root.

Add:

TMDB_API_KEY=your_tmdb_api_key

Never commit the real .env file to GitHub.

---

## Running the Backend

Start FastAPI:

uvicorn main:app --reload

The backend will be available at:

http://127.0.0.1:8000

Interactive API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

---

## Running the Frontend

Open another terminal and activate the virtual environment.

Run:

streamlit run app.py

The frontend will normally be available at:

http://localhost:8501

---

## Environment Variables

### FastAPI Backend

The backend requires:

TMDB_API_KEY=your_tmdb_api_key

### Streamlit Frontend

For deployment, configure:

API_BASE_URL=https://your-fastapi-backend-url.com

The TMDB API key remains on the FastAPI backend and is not exposed to the frontend.

---

## Deployment Architecture

CineMatch is designed to run as two separate services.

User
→ Streamlit Frontend
→ FastAPI Backend
→ TF-IDF Recommendation Engine

The FastAPI backend also communicates with the TMDB API.

The Streamlit frontend communicates with the deployed FastAPI backend through API_BASE_URL.

The FastAPI backend communicates with TMDB using the private TMDB_API_KEY.

---

## Model Artifacts

The recommendation engine uses four precomputed artifacts:

* df.pkl
* indices.pkl
* tfidf.pkl
* tfidf_matrix.pkl

These files are included in the repository because they are required by the FastAPI backend at runtime.

The original movies_metadata.csv dataset is not required by the deployed application because the required processed data and recommendation artifacts have already been generated.

---

## Recommendation Method

CineMatch uses content-based filtering.

Movie metadata is converted into numerical representations using TF-IDF.

The system then calculates cosine similarity between movie vectors.

The process is:

Movie A
→ TF-IDF Vector
→ Cosine Similarity
→ Compare With Other Movies
→ Rank Similarity Scores
→ Recommended Movies

A higher cosine similarity score indicates that two movie representations are more similar.

---

## Why Content-Based Filtering?

Content-based filtering recommends items based on their characteristics.

For CineMatch, recommendations are generated from movie metadata rather than relying on user ratings or interaction history.

This makes the system suitable for demonstrating a standalone recommendation engine using machine learning and natural language processing techniques.

---

## Limitations

CineMatch currently has several limitations:

* Recommendations depend on available movie metadata.
* The system does not learn individual user preferences over time.
* TF-IDF does not capture semantic meaning as deeply as transformer-based embeddings.
* TMDB API availability and rate limits can affect external movie information.
* Some locally stored movies may not have an exact TMDB match.
* Genre recommendations currently use the primary genre returned by TMDB.

---

## Future Improvements

Potential improvements include:

* Transformer-based semantic embeddings
* Sentence Transformers
* Hybrid recommendation systems
* Collaborative filtering
* Personalized user profiles
* Recommendation history
* User authentication
* Redis caching
* Semantic movie search
* Recommendation explanations
* Movie similarity visualization
* User feedback-based recommendations

---

## Disclaimer

CineMatch is an educational and portfolio project.

Movie information, posters, ratings, and related metadata are provided through TMDB.

This project is not affiliated with or endorsed by TMDB.

---

## Author

Burhan Arshad

Field: BS Computer Science

Specialization: Machine Learning & Deep Learning

Areas of Focus:

* Machine Learning
* Deep Learning
* Natural Language Processing
* Generative AI
* AI Engineering

GitHub: https://github.com/burhan-arshad

---

## License

This project is available for educational and portfolio purposes.
