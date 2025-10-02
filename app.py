# app.py
import streamlit as st
from datetime import datetime
from src.services.viber_service import ViberService
from src.services.thought_service import ThoughtService
from src.services.post_service import PostService
from src.services.reverberation_service import ReverberationService
from src.services.soul_link_service import SoulLinkService
from src.services.echo_service import EchoService
from src.services.badge_service import BadgeService
from src.services.tribe_service import TribeService

st.set_page_config(
    page_title="VibeNet",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Styles for Dark Mode ---
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #E0E0E0; }
        .card { 
            background-color: #1E1E1E; 
            border-radius: 10px; 
            padding: 15px; 
            margin-bottom: 15px; 
            box-shadow: 0 0 10px rgba(0,0,0,0.5);
        }
        .sidebar .sidebar-content {
            background-color: #1A1A1A;
        }
        .btn { color: white; background-color: #6200EE; border-radius: 5px; padding: 5px 10px; }
        .emotion-Joy { color: #FFD700; font-weight: bold; }
        .emotion-Curiosity { color: #00BFFF; font-weight: bold; }
        .emotion-Nostalgia { color: #FF69B4; font-weight: bold; }
        .emotion-Rage { color: #FF4500; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("VibeNet 🔮")
menu = st.sidebar.radio("Navigation", ["Home", "Feed", "Tribes", "Profile", "Trending"])

# --- Helper Functions ---
def display_badges(badges):
    for badge in badges:
        st.markdown(f"<span style='color:#FFD700'>{badge}</span>", unsafe_allow_html=True)

def display_thought_card(thought):
    emotion = thought.get("emotion_tag", "Neutral")
    author_id = thought.get("viber_id")
    author = ViberService.get(author_id)
    aura_color = author.get("aura_color", "Neutral")
    st.markdown(f"<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"**Author:** {author.get('username')}  | Aura: {aura_color}")
    st.markdown(f"**Emotion:** <span class='emotion-{emotion}'>{emotion}</span>", unsafe_allow_html=True)
    st.markdown(f"**Content:** {thought.get('content')}")
    st.markdown(f"**Echoes:** {thought.get('echoes',0)} | **Vibe Score:** {thought.get('vibe_score',0)}")
    
    cols = st.columns([1,1,1,2])
    with cols[0]:
        if st.button("😊 Joy", key=f"joy-{thought['thought_id']}"):
            EchoService.react(thought["thought_id"], 1, "Joy")
    with cols[1]:
        if st.button("🤔 Curiosity", key=f"curiosity-{thought['thought_id']}"):
            EchoService.react(thought["thought_id"], 1, "Curiosity")
    with cols[2]:
        if st.button("🌸 Nostalgia", key=f"nostalgia-{thought['thought_id']}"):
            EchoService.react(thought["thought_id"], 1, "Nostalgia")
    with cols[3]:
        if st.button("😡 Rage", key=f"rage-{thought['thought_id']}"):
            EchoService.react(thought["thought_id"], 1, "Rage")
    st.markdown("</div>", unsafe_allow_html=True)

# --- Pages ---
if menu == "Home":
    st.header("Welcome to VibeNet 🔮")
    st.markdown("Express your thoughts, join tribes, and vibe with the community!")

elif menu == "Feed":
    st.header("Feed")
    thoughts = ThoughtService.list_recent(10)
    for t in thoughts:
        display_thought_card(t)

elif menu == "Tribes":
    st.header("Tribes")
    tribes = TribeService.list()
    for tribe in tribes:
        st.markdown(f"<div class='card'><b>{tribe['name']}</b><br>{tribe['description']}</div>", unsafe_allow_html=True)
        if st.button(f"Join {tribe['name']}", key=f"join-{tribe['tribe_id']}"):
            TribeService.join(1, tribe['tribe_id'])
            st.success(f"Joined {tribe['name']}!")

elif menu == "Profile":
    st.header("Your Profile")
    # For simplicity, current viber_id = 1
    user = ViberService.get(1)
    st.markdown(f"**Username:** {user['username']}")
    st.markdown(f"**Aura Color:** {user['aura_color']}")
    st.markdown(f"**Vibe Level:** {user['vibe_level']}")
    st.markdown("**Badges:**")
    display_badges(user.get("badges", []))
    st.markdown("---")
    st.subheader("Your Thoughts")
    thoughts = ThoughtService.list_recent(10)
    for t in thoughts:
        if t["viber_id"] == 1:
            display_thought_card(t)

elif menu == "Trending":
    st.header("Trending Realms")
    # Placeholder for trending (latest thoughts)
    trending = ThoughtService.list_recent(5)
    for t in trending:
        display_thought_card(t)
