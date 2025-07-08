# first
import streamlit as st
import pickle
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommendation System ",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling with background and title box
st.markdown("""
<style>
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        background-attachment: fixed;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        margin-top: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Title box styling */
    .title-box {
        background: linear-gradient(135deg, #E50914 0%, #B20710 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem auto;
        max-width: 800px;
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header {
        font-size: 3.5rem;
        color: white;
        font-weight: bold;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
        letter-spacing: 2px;
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 1rem 0 0 0;
        font-weight: 300;
    }
    
    /* Movie selection section */
    .selection-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .selection-header {
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    /* Movie recommendation cards */
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .recommendation-header {
        color: #FFD700;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {
        background-color: rgba(255, 255, 255, 0.9);
        border: 2px solid #E50914;
        border-radius: 10px;
        color: #333;
        font-size: 1.1rem;
        padding: 0.5rem;
    }
    
    .stSelectbox > div > div > select:focus {
        border-color: #FFD700;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
        color: #333;
        border: none;
        border-radius: 25px;
        padding: 1rem 3rem;
        font-weight: bold;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 5px 15px rgba(255, 215, 0, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #FFA500 0%, #FF8C00 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(255, 215, 0, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(30, 60, 114, 0.9);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .sidebar-content strong {
        color: #FFD700;
    }
    
    /* Footer styling */
    .footer {
        color: rgba(255, 255, 255, 0.7);
        text-align: center;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding: 1rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #FFD700 !important;
    }
    
    /* Text color adjustments */
    .stMarkdown, .stText {
        color: white;
    }
    
    /* Hide Streamlit menu and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Load data
@st.cache_data
def load_data():
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    return movies, similarity

movies, similarity = load_data()

# Header section with title box
st.markdown('''
<div class="title-box">
    <h1 class="main-header">🎬 MOVIE RECOMMENDER SYSTEM </h1>
    <p class="sub-header">Discover your next favorite movie based on your preferences!</p>
</div>
''', unsafe_allow_html=True)

# Create columns for better layout
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Movie selection in a container
    st.markdown('''
    <div class="selection-container">
        <div class="selection-header">🎭 Select a Movie You Like</div>
    </div>
    ''', unsafe_allow_html=True)
    
    selected_movie_name = st.selectbox(
        "",
        movies['title'].values,
        help="Choose a movie you enjoyed, and we'll recommend similar ones!"
    )
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recommendation button
    if st.button("🔍 Get Recommendations"):
        with st.spinner('Finding amazing movies for you...'):
            recommendations = recommend(selected_movie_name)
            
            st.markdown('<div class="recommendation-header">🌟 Movies You Might Love</div>', unsafe_allow_html=True)
            
            # Display recommendations in attractive cards
            for i, movie in enumerate(recommendations, 1):
                st.markdown(f'''
                <div class="movie-card">
                    {i}. {movie}
                </div>
                ''', unsafe_allow_html=True)

# Sidebar with additional information
with st.sidebar:
    st.markdown("### 📊 About This System")
    st.markdown("""
    <div class="sidebar-content">
    This recommendation system uses:
    <br><br>
    🎯 <strong>Content-Based Filtering</strong><br>
    📊 <strong>Machine Learning</strong><br>
    🔍 <strong>Similarity Analysis</strong><br>
    📚 <strong>5000+ Movies Database</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🎬 How It Works")
    st.markdown("""
    <div class="sidebar-content">
    1. Select a movie you enjoyed<br>
    2. Our AI analyzes movie features<br>
    3. Finds similar movies<br>
    4. Presents top 5 recommendations
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🌟 Features")
    st.markdown("""
    <div class="sidebar-content">
    ✅ Instant recommendations<br>
    ✅ Based on genres, cast & plot<br>
    ✅ 5000+ movie database<br>
    ✅ Smart similarity matching
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('''
<div class="footer">
    Made with ❤️ using Streamlit | Movie data from TMDb
</div>
''', unsafe_allow_html=True)
