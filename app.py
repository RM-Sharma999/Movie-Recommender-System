from streamlit_clickable_images import clickable_images
import streamlit as st
import pandas as pd
import pickle
import requests
import base64
import faiss
import time

# Get movie metadata function
@st.cache_data(show_spinner = False)
def get_movie_metadata(movie_id, retries = 3):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=b8cd668a03ee6296f94919995b52d187&language=en-US"

    for attempt in range(retries):
        try:
            response = requests.get(url, timeout = 8)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            print(f"Retrying {movie_id}... ({attempt+1}/{retries})")
            time.sleep(0.3)
    return None

# Load poster function
@st.cache_data(show_spinner = False)
def load_poster_from_tmdb(poster_path):
    url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    try:
        response = requests.get(url, timeout = 10)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return None

# Serve poster function
def serve_poster(poster_path):
    data = load_poster_from_tmdb(poster_path)

    if data is None:
        placeholder_url = "https://i.ibb.co/KxZrXkRY/8b6bd5f4-f5dc-4899-baab-85446491e3f8.png"
        try:
            response = requests.get(placeholder_url, timeout = 5)
            response.raise_for_status()
            data = response.content
        except requests.exceptions.RequestException:
            data = b""
    b64 = base64.b64encode(data).decode()
    # Assuming it's PNG because your URL is a PNG
    return f"data:image/png;base64,{b64}"

# Fetch poster function
def fetch_poster(movie_id):
    data = get_movie_metadata(movie_id)

    poster_path = data.get("poster_path") if data else None
    if not poster_path:
        return serve_poster(None)
    return serve_poster(poster_path)

# Load faiss index function
@st.cache_resource
def load_faiss():
    index = faiss.read_index("faiss_index.bin")
    return index

# Load embeddings function
@st.cache_resource
def load_embeddings():
    embeddings = pickle.load(open("embeddings.pkl", "rb"))
    return embeddings

# Recommend movies function
def recommend_movies(movie, k = 5):
    # Get the index of the selected movie
    movie_index = movies[movies["title"] == movie].index[0]

    # Get its embeddings
    query_vec = embeddings[movie_index].reshape(1, -1)

    # Search using faiss(k + 1 to skip the movie itself)
    distances, indices = index.search(query_vec, k + 1)

    # Skip the first result (the movie itself)
    recommended_indices = indices[0][1:]

    recommended_movies, recommended_posters = [], []

    for i in recommended_indices:
        movie_id = movies.iloc[i]["id"]
        recommended_movies.append(movies.iloc[i]["title"])
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters



# Load faiss index
index = load_faiss()

# Load embeddings
embeddings = load_embeddings()
faiss.normalize_L2(embeddings)

# Load the data
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))

movies = pd.DataFrame(movies_dict)
movie_titles = movies["title"].values

# Set configuration and title
st.set_page_config(page_title = "Movie Recommender System", layout = "wide")
st.title("Movie Recommender System")

# Initialize session variables
if "history" not in st.session_state:
    st.session_state.history = []
if "recommended" not in st.session_state:
    st.session_state.recommended = []
if "last_selected" not in st.session_state:
    st.session_state.last_selected = None
if "clicked_index" not in st.session_state:
    st.session_state.clicked_index = -1
if "click_lock" not in st.session_state:
    st.session_state.click_lock = False

# Movie dropdown
selected_movie = st.selectbox(
    "",
    options = [""] + list(movie_titles),
    format_func = lambda x: "Select a Movie to Recommend" if x == "" else x
)

# Handle recommend button
if st.button("Recommend"):
    # Warn if no movie is selected
    if selected_movie == "":
        st.warning("Please select a movie first!")
        st.stop()
    # Check if movie exists in the dataset
    if selected_movie not in movies["title"].values:
        st.warning("Movie not found in dataset. Please choose another movie.")
        st.stop()
    st.session_state.recommended = []
    names, posters = recommend_movies(selected_movie)
    st.session_state.history.append(selected_movie)
    st.session_state.recommended = list(zip(names, posters))
    st.session_state.last_selected = selected_movie
    st.session_state.clicked_index = -1
    st.session_state.click_lock = False
    st.rerun()

# Display clickable posters (with visible titles)
if st.session_state.recommended:
    st.subheader(f'Movies similar to "**{st.session_state.last_selected}**"')

    # Back button
    if st.button("←"):
        if len(st.session_state.history) > 1:
            # Pop current movie and show previous
            st.session_state.history.pop()
            prev_movie = st.session_state.history[-1]
            names, posters = recommend_movies(prev_movie)
            st.session_state.recommended = list(zip(names, posters))
            st.session_state.last_selected = prev_movie
        else:
            # No previous history, then return to home
            st.session_state.recommended = []
            st.session_state.last_selected = None
        # Reset click_index, click_lock for both cases
        st.session_state.clicked_index = -1
        st.session_state.click_lock = False
        st.rerun()

    posters = [poster for _, poster in st.session_state.recommended]
    titles = [title for title, _ in st.session_state.recommended]

    # Clickable posters
    component_key = "poster_" + st.session_state.last_selected.replace(" ", "_")

    clicked_index = clickable_images(
        posters,
        titles = titles,
        div_style = {
            "display": "flex",
            "justify-content": "center",
            "flex-wrap": "wrap",
            "gap": "18px",
        },
        img_style = {
            "border-radius": "12px",
            "width": "180px",
            "height": "270px",
            "object-fit": "cover",
            "transition": "transform 0.2s ease, box-shadow 0.2s ease",
        },
        key = component_key,
    )

    # Display movie titles under posters manually
    cols = st.columns(len(titles))
    for col, title in zip(cols, titles):
        with col:
            st.markdown(
                f"<p class = 'movie-title'>{title}</p>",
                unsafe_allow_html = True
            )

    # Handle clicks safely

    # Normalize clicked_index to -1
    if clicked_index is None:
        clicked_index = -1

    if clicked_index != -1 and not st.session_state.click_lock:
        # Bounds safety
        if 0 <= clicked_index < len(titles):
            clicked_title = titles[clicked_index]

            # Prevents processing on same click repeatedly
            if st.session_state.get("last_clicked_title") != clicked_title:
                st.session_state.last_clicked_title = clicked_title
                st.session_state.click_lock = True

                # Update recommendations once
                st.session_state.recommended = []
                names, posters = recommend_movies(clicked_title)
                st.session_state.recommended = list(zip(names, posters))
                st.session_state.last_selected = clicked_title

                # Add clicked movie to history
                st.session_state.history.append(clicked_title)

                # small delay then rerun so UI updates cleanly
                time.sleep(0.06)
                st.rerun()

    # unlock after stable state
    elif clicked_index == -1 and st.session_state.click_lock:
        # Do not unlock instantly
        time.sleep(0.04)
        st.session_state.click_lock = False

# Styling for hover + title
st.markdown(
    """
<style>
img:hover {
    transform: scale(1.05);
    box-shadow: 0 0 12px rgba(255,255,255,0.6);
}
.movie-title {
    text-align: center;
    margin-top: 6px;
    font-weight: 500;
    font-size: 0.9rem;
    color: black;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
""",
    unsafe_allow_html = True,
)