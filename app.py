
import streamlit as st
import pickle
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# LOAD DATA
# =========================
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# =========================
# API KEY FUNCTION
# =========================
def get_api_key():
    return "182ce96e20dc330c300c9a62930daf4e"

# =========================
# FETCH POSTER FUNCTION
# =========================
def fetch_poster(movie_id):
    api_key = get_api_key()
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    backdrop_path = data.get('backdrop_path')
    overview = data.get('overview', 'No description available.')
    rating = data.get('vote_average', 0)
    release_date = data.get('release_date', 'N/A')
    genres = data.get('genres', [])
    genre_names = [g['name'] for g in genres[:3]]

    poster_url = ("https://image.tmdb.org/t/p/w500/" + poster_path) if poster_path else "https://via.placeholder.com/500x750?text=No+Poster"
    backdrop_url = ("https://image.tmdb.org/t/p/w1280/" + backdrop_path) if backdrop_path else None

    return {
        "poster": poster_url,
        "backdrop": backdrop_url,
        "overview": overview,
        "rating": rating,
        "release_date": release_date[:4] if release_date != 'N/A' else 'N/A',
        "genres": genre_names
    }

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_distances = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    results = []
    for i in movie_distances:
        movie_id = movies_list.iloc[i[0]].movie_id
        title = movies_list.iloc[i[0]].title
        info = fetch_poster(movie_id)
        info['title'] = title
        results.append(info)

    return results

# =========================
# NETFLIX-STYLE CSS
# =========================
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700&display=swap');

  /* ── Global Reset ── */
  html, body, [class*="css"] {
    background-color: #0a0a0a !important;
    color: #e5e5e5 !important;
    font-family: 'Inter', sans-serif;
  }

  .stApp {
    background: #0a0a0a !important;
  }

  /* ── Hide Streamlit chrome ── */
  #MainMenu, footer, header { visibility: hidden; }
  .block-container {
    padding: 0 !important;
    max-width: 100% !important;
  }

  /* ── Navbar ── */
  .navbar {
    position: sticky;
    top: 0;
    z-index: 999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 60px;
    background: linear-gradient(180deg, rgba(0,0,0,0.95) 0%, transparent 100%);
    backdrop-filter: blur(6px);
    border-bottom: 1px solid rgba(255,255,255,0.04);
  }

  .navbar-brand {
    font-family: 'Bebas Neue', cursive;
    font-size: 2.2rem;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #e50914 0%, #ff6b35 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-decoration: none;
    user-select: none;
  }

  .navbar-tagline {
    font-size: 0.75rem;
    color: #888;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 300;
  }

  /* ── Hero Section ── */
  .hero {
    position: relative;
    width: 100%;
    height: 82vh;
    min-height: 500px;
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    padding: 0 60px 60px;
    margin-bottom: 0;
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    background-size: cover;
    background-position: center top;
    filter: brightness(0.45);
    transform: scale(1.02);
    transition: opacity 0.8s ease;
  }

  .hero-gradient {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      to bottom,
      transparent 0%,
      transparent 30%,
      rgba(10,10,10,0.6) 65%,
      #0a0a0a 100%
    );
  }

  .hero-gradient-side {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      to right,
      rgba(10,10,10,0.85) 0%,
      transparent 55%
    );
  }

  .hero-content {
    position: relative;
    z-index: 2;
    max-width: 580px;
  }

  .hero-badge {
    display: inline-block;
    background: #e50914;
    color: white;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 5px 12px;
    border-radius: 3px;
    margin-bottom: 16px;
  }

  .hero-title {
    font-family: 'Bebas Neue', cursive;
    font-size: clamp(2.8rem, 5vw, 4.5rem);
    line-height: 1.0;
    letter-spacing: 1px;
    color: #fff;
    margin: 0 0 16px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.5);
  }

  .hero-meta {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
    flex-wrap: wrap;
  }

  .hero-rating {
    display: flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    color: #f5c518;
  }

  .hero-year {
    font-size: 0.8rem;
    color: #aaa;
    font-weight: 400;
  }

  .hero-genre-tag {
    font-size: 0.72rem;
    color: #ccc;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
  }

  .hero-overview {
    font-size: 0.95rem;
    line-height: 1.65;
    color: #c8c8c8;
    font-weight: 300;
    max-width: 460px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* ── Search Section ── */
  .search-section {
    padding: 48px 60px 20px;
    background: linear-gradient(180deg, transparent 0%, #0a0a0a 20%);
    position: relative;
    z-index: 10;
  }

  .section-label {
    font-size: 0.7rem;
    color: #e50914;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 600;
    margin-bottom: 10px;
  }

  .section-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 2rem;
    letter-spacing: 1px;
    color: #fff;
    margin-bottom: 28px;
    line-height: 1;
  }

  /* ── Streamlit Selectbox Override ── */
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: #e5e5e5 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 4px 0 !important;
    transition: border-color 0.2s !important;
  }

  .stSelectbox > div > div:hover {
    border-color: rgba(229,9,20,0.6) !important;
  }

  .stSelectbox > div > div:focus-within {
    border-color: #e50914 !important;
    box-shadow: 0 0 0 2px rgba(229,9,20,0.2) !important;
  }

  /* ── Recommend Button ── */
  .stButton > button {
    background: linear-gradient(135deg, #e50914, #c40812) !important;
    color: white !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(229, 9, 20, 0.35) !important;
    width: auto !important;
}

/* Center the button - ADD THIS */
.stButton {
    display: flex !important;
    justify-content: center !important;
}

  .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(229, 9, 20, 0.5) !important;
    background: linear-gradient(135deg, #ff1a27, #e50914) !important;
  }

  .stButton > button:active {
    transform: translateY(0px) !important;
  }

  /* ── Results Section ── */
  .results-section {
    padding: 20px 60px 60px;
  }

  .results-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 30px;
  }

  .results-divider {
    height: 3px;
    flex: 1;
    background: linear-gradient(to right, rgba(229,9,20,0.5), transparent);
    border-radius: 2px;
  }

  /* ── Movie Card ── */
  .movie-card {
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    background: #141414;
    border: 1px solid rgba(255,255,255,0.06);
    transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1),
                box-shadow 0.35s ease,
                border-color 0.2s ease;
    cursor: pointer;
    height: 100%;
  }

  .movie-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 20px 50px rgba(0,0,0,0.7), 0 0 0 1px rgba(229,9,20,0.3);
    border-color: rgba(229,9,20,0.3);
    z-index: 10;
  }

  .movie-card:hover .card-overlay {
    opacity: 1;
  }

  .movie-card:hover .card-info {
    transform: translateY(0);
    opacity: 1;
  }

  .card-poster {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
    transition: filter 0.3s ease;
  }

  .movie-card:hover .card-poster {
    filter: brightness(0.4);
  }

  .card-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(
      to top,
      rgba(10,10,10,0.98) 0%,
      rgba(10,10,10,0.5) 50%,
      transparent 100%
    );
    opacity: 0.5;
    transition: opacity 0.3s ease;
  }

  .card-rank {
    position: absolute;
    top: 12px;
    left: 12px;
    font-family: 'Bebas Neue', cursive;
    font-size: 1.5rem;
    color: rgba(255,255,255,0.9);
    background: rgba(229,9,20,0.85);
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 6px;
    letter-spacing: 0;
    z-index: 3;
  }

  .card-info {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 16px;
    transform: translateY(8px);
    opacity: 0.85;
    transition: transform 0.3s ease, opacity 0.3s ease;
    z-index: 4;
  }

  .card-title {
    font-family: 'Bebas Neue', cursive;
    font-size: 1.15rem;
    letter-spacing: 0.5px;
    color: #fff;
    margin: 0 0 6px;
    line-height: 1.2;
    text-shadow: 0 1px 8px rgba(0,0,0,0.8);
  }

  .card-meta-row {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }

  .card-rating-pill {
    display: flex;
    align-items: center;
    gap: 3px;
    background: rgba(245,197,24,0.15);
    border: 1px solid rgba(245,197,24,0.3);
    padding: 2px 7px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    color: #f5c518;
  }

  .card-year {
    font-size: 0.7rem;
    color: #999;
  }

  .card-genre {
    font-size: 0.65rem;
    color: #bbb;
    background: rgba(255,255,255,0.07);
    padding: 2px 7px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
  }

  /* ── Spinner override ── */
  .stSpinner > div {
    border-color: #e50914 transparent transparent !important;
  }

  /* ── Footer ── */
  .cinematch-footer {
    text-align: center;
    padding: 40px 60px;
    border-top: 1px solid rgba(255,255,255,0.06);
    color: #444;
    font-size: 0.75rem;
    letter-spacing: 1px;
  }

  .cinematch-footer span {
    color: #e50914;
  }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: #0a0a0a; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #e50914; }
</style>
""", unsafe_allow_html=True)

# =========================
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
  <span class="navbar-brand">🎬 CineMatch</span>
  <span class="navbar-tagline">AI-Powered Recommendations</span>
</div>
""", unsafe_allow_html=True)

# =========================
# STATE
# =========================
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'selected_movie' not in st.session_state:
    st.session_state.selected_movie = None
if 'hero_info' not in st.session_state:
    st.session_state.hero_info = None

movie_list_values = movies_list['title'].values

# =========================
# SEARCH SECTION
# =========================
st.markdown('<div class="search-section">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Discover</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Find Your Next Obsession</div>', unsafe_allow_html=True)

col_select, col_btn = st.columns([4, 1])
with col_select:
    selected_movie = st.selectbox(
        "",
        movie_list_values,
        label_visibility="collapsed"
    )
with col_btn:
    recommend_clicked = st.button("▶ Recommend", use_container_width=False)

st.markdown('</div>', unsafe_allow_html=True)

# =========================
# ON RECOMMEND CLICK
# =========================
if recommend_clicked:
    with st.spinner("Fetching recommendations..."):
        results = recommend(selected_movie)
        st.session_state.recommendations = results
        st.session_state.selected_movie = selected_movie

        # Fetch hero info for selected movie
        sel_row = movies_list[movies_list['title'] == selected_movie].iloc[0]
        hero_data = fetch_poster(sel_row['movie_id'])
        hero_data['title'] = selected_movie
        st.session_state.hero_info = hero_data

# =========================
# HERO BANNER
# =========================
hero = st.session_state.hero_info
if hero:
    bg_url = hero.get('backdrop') or hero.get('poster')
    genres_html = "".join([f'<span class="hero-genre-tag">{g}</span>' for g in hero.get('genres', [])])
    rating_val = hero.get('rating', 0)
    stars = "★" * round(rating_val / 2) if rating_val else ""

    st.markdown(f"""
    <div class="hero">
      <div class="hero-bg" style="background-image: url('{bg_url}');"></div>
      <div class="hero-gradient"></div>
      <div class="hero-gradient-side"></div>
      <div class="hero-content">
        <div class="hero-badge">Now Viewing</div>
        <h1 class="hero-title">{hero['title']}</h1>
        <div class="hero-meta">
          <div class="hero-rating">⭐ {rating_val:.1f} / 10</div>
          <span class="hero-year">{hero.get('release_date','N/A')}</span>
          {genres_html}
        </div>
        <p class="hero-overview">{hero.get('overview','')}</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# RESULTS GRID
# =========================
if st.session_state.recommendations:
    results = st.session_state.recommendations

    st.markdown('<div class="results-section">', unsafe_allow_html=True)
    st.markdown("""
    <div class="results-header">
      <div class="section-label" style="margin:0; white-space:nowrap;">Because You Chose</div>
      <div class="results-divider"></div>
    </div>
    <div class="section-title" style="margin-bottom:24px;">Top 5 Picks For You</div>
    """, unsafe_allow_html=True)

    cols = st.columns(5, gap="medium")

    for idx, (col, movie) in enumerate(zip(cols, results)):
        with col:
            genres_html = " · ".join(movie.get('genres', [])[:2])
            rating = movie.get('rating', 0)

            st.markdown(f"""
            <div class="movie-card">
              <img class="card-poster" src="{movie['poster']}" alt="{movie['title']}"/>
              <div class="card-overlay"></div>
              <div class="card-rank">{idx + 1}</div>
              <div class="card-info">
                <div class="card-title">{movie['title']}</div>
                <div class="card-meta-row">
                  <span class="card-rating-pill">⭐ {rating:.1f}</span>
                  <span class="card-year">{movie.get('release_date','')}</span>
                  {'<span class="card-genre">' + genres_html + '</span>' if genres_html else ''}
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# EMPTY STATE
# =========================
if not st.session_state.recommendations:
    st.markdown("""
    <div style="text-align:center; padding: 80px 60px; color: #333;">
      <div style="font-family:'Bebas Neue',cursive; font-size:4rem; letter-spacing:2px; color:#1a1a1a; margin-bottom:12px;">
        LIGHTS. CAMERA. ACTION.
      </div>
      <div style="font-size:0.9rem; color:#444; letter-spacing:1px;">
        Select a movie above and hit Recommend to discover your next watch.
      </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class="cinematch-footer">
  Built with <span>♥</span> using Streamlit · Powered by TMDB API · CineMatch © 2025
</div>
""", unsafe_allow_html=True)