# Movie Recommender System

A **content-based movie recommendation system** built using **movie embeddings** and **efficient similarity search**. This project uses real movie data to generate recommendations and includes a **Streamlit web application** that provides **interactive movie recommendations**.

---

## Objective

The goal of this project is to build a **movie recommendation engine** that suggests movies similar to a given movie or user preferences. It combines **embedding techniques** with **efficient similarity search** to provide **relevant movie recommendations**.

---

## Dataset Overview

The project uses a dataset of movies containing essential **movie metadata** (e.g., titles, genres), collected via **The Movie Database (TMDb) API** and compiled into `movies.csv`. **Movie embeddings** and **index files** (`embeddings.pkl`, `faiss_index.bin`) are generated using **Sentence-Transformers** to support **fast similarity search** for recommending related movies.

**Key elements:**
- **movies.csv** — Movie dataset collected via the TMDb API.
- **embeddings.pkl** — Precomputed Sentence-Transformer embeddings representing movies in vector space.
- **faiss_index.bin** — FAISS index for efficient nearest-neighbor search.

---

## How It Works

1. **Embedding Generation**  
   1. **Embedding Generation**  
   Movie data is converted into dense vector embeddings using **Sentence-Transformers**, capturing semantic similarity between movies based on their metadata.

2. **Similarity Search**  
   A **FAISS index** is used to perform **fast nearest-neighbor search** on movie vectors.

3. **Recommendation Logic**  
   Given a movie query, the system retrieves the **most similar movies** based on **vector distances**.

4. **Application Interface**  
   An application file (`app.py`) uses the **precomputed index and embeddings** to serve **recommendations** for a selected movie.

---

## Usage

Ensure all **required dependencies** are installed and all **necessary files** are available in the project directory.

Launch the Streamlit application by running:
```bash
streamlit run app.py
```

<br>

**Below is a short demo of the Streamlit application in action:**

![Streamlit App Demo](assets/streamlit-app.gif)

---

## Technologies Used

- **Programming Language**: `Python`
- **Data Analysis**: `Pandas`, `NumPy`
- **Vector Representations & Search**: `Sentence-Transformers`, `FAISS`
- **Web Interface**: `Streamlit`
- **Deployment Platform**: `Streamlit Community Cloud`

---

## Deployment

The application is deployed as a **Streamlit web app** on the **Streamlit Community Cloud** platform. It offers an **interactive interface** where users can view **movie recommendations** and click on suggested movies to receive **updated recommendations in real time**.

[Movie Recommender System Live App](https://movie-recommender-system-bcx5ns6pxvmn8gazkykg42.streamlit.app/)

---

## Key Takeaways

- Built a **content-based movie recommender system** using **Sentence-Transformer embeddings** and **FAISS similarity search**.
- Implemented **efficient nearest-neighbor retrieval** to generate fast and relevant recommendations.
- Designed an **interactive Streamlit app** for seamless user interaction.
- Gained hands-on experience sourcing data via the **TMDb API** and deploying a recommendation system as a **web application**.
