# Movie Recommender System

A machine learning–based movie recommendation system built using user–movie embeddings and efficient similarity search. This project uses real movie data to generate recommendations and includes a Streamlit web application that provides interactive movie recommendations.

---

## Objective

The goal of this project is to build a movie recommendation engine that suggests movies similar to a given movie or user preferences. It combines embedding techniques with efficient similarity search to provide relevant movie suggestions.

---

## Dataset Overview

The project uses a dataset of movies containing essential movie metadata (e.g., titles, genres) stored in `movies.csv`. Movie embeddings and index files (`embeddings.pkl`, `faiss_index.bin`) are generated to support fast similarity search for recommending related movies.

Key elements:
- **movies.csv** — Movie dataset.
- **embeddings.pkl** — Precomputed feature embeddings representing movies in vector space.
- **faiss_index.bin** — FAISS index for efficient nearest-neighbor search.

---

## How It Works

1. **Embedding Generation**  
   Movie data is converted into vector representations encoding important movie features for effective similarity search.

2. **Similarity Search**  
   A FAISS index is used to perform fast nearest-neighbor search on movie vectors.

3. **Recommendation Logic**  
   Given a movie query, the system retrieves the most similar movies based on vector distances.

4. **Application Interface**  
   An application file (`app.py`) uses the precomputed index and embeddings to serve recommendations for a selected movie.

---

## Usage

Ensure all required dependencies are installed and all necessary files are available in the project directory.

Launch the Streamlit application by running:
```bash
streamlit run app.py
```
<br>
### Streamlit App Demo:
<br><br/>

![Streamlit App Demo](assets/streamlit-app.gif)

---

## Technologies Used

- **Programming Language**: `Python`
- **Data Analysis**: `Pandas`, `NumPy`
- **Machine Learning**: `Embedding Techniques`, `Similarity Search(FAISS)`
- **Web Interface**: `Streamlit`
- **Deployment Platform**: `Streamlit Web Community`

---

## Deployment

The application is deployed as a **Streamlit web app** on the **Streamlit Web Community** platform. It offers an interactive interface where users can view movie recommendations and click on suggested movies to receive updated recommendations in real time.

[Movie Recommender System Live App](https://movie-recommender-system-bcx5ns6pxvmn8gazkykg42.streamlit.app/)

---

## Key Takeaways

- Built a **content-based movie recommender system** using **embedding representations** and **similarity search**.
- Implemented **efficient nearest-neighbor retrieval** to generate fast and relevant recommendations.
- Designed an **interactive Streamlit app** for seamless user interaction.
- Gained hands-on experience deploying a recommendation system as a web application.
