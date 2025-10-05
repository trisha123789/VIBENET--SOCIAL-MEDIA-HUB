import streamlit as st
from datetime import datetime
from typing import Dict, List, Optional

# === Services ===
from src.services.viber_service import ViberService
from src.services.thought_service import ThoughtService
from src.services.post_service import PostService
from src.services.badge_service import BadgeService
from src.services.tribe_service import TribeService
from src.services.echo_service import EchoService

# ====== Page config ======
st.set_page_config(page_title="VibeNet 🔮", page_icon="🔮", layout="wide", initial_sidebar_state="expanded")

# ====== CSS for neon + dark gamified UI ======
st.markdown("""
<style>
:root {
    --bg: #0b0c10;
    --card-bg: linear-gradient(145deg, #111217, #1c1e26);
    --accent: #ff6ec7;
    --accent2: #8a6cff;
    --muted: #8b95a1;
}






















.stApp { background: var(--bg); color: #e9f0f7; }
.sidebar .sidebar-content { background: #0d0e15; border-right:1px solid rgba(255,255,255,0.05); }
.card {
    background: var(--card-bg);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 20px rgba(138,108,255,0.3);
    transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover { transform: translateY(-4px); box-shadow: 0 8px 30px rgba(138,108,255,0.6); }
.author { font-weight:700; font-size:16px; color:#fff; }
.mini { font-size:12px; color: var(--muted); }
.badge-pill { padding:6px 12px; border-radius:999px; background: rgba(255,255,255,0.05); margin-right:6px; display:inline-block; transition: all 0.2s; }
.badge-pill:hover { background: var(--accent2); color:#fff; transform: scale(1.1); }
.vibe-btn { background: var(--accent); color: white; padding:6px 14px; border-radius:12px; border: none; cursor:pointer; transition: all 0.2s; }
.vibe-btn:hover { background: #ff3ec7; transform: scale(1.05); }
.emo-Joy { color:#FFD166; font-weight:700; }
.emo-Curiosity { color:#39A2DB; font-weight:700; }
.emo-Nostalgia { color:#FF7AB6; font-weight:700; }
.emo-Rage { color:#FF6B6B; font-weight:700; }
.searchbox { background: rgba(255,255,255,0.02); padding:8px 10px; border-radius:10px; }

.notif-item {
    padding:6px 10px;
    border-radius:8px;
    margin-bottom:6px;
    background: rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}
.notif-new {
    background: linear-gradient(90deg, #ff6ec7, #8a6cff);
    color: #fff;
    font-weight: 700;
    box-shadow: 0 0 10px rgba(255,110,199,0.8), 0 0 20px rgba(138,108,255,0.6);
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

# ====== Helpers ======
EMOTION_CLASS = {
    "Joy": "emo-Joy",
    "Curiosity": "emo-Curiosity",
    "Nostalgia": "emo-Nostalgia",
    "Rage": "emo-Rage",
    "Neutral": "mini",
}

def timeago(iso_ts: Optional[str]) -> str:
    if not iso_ts:
        return ""
    try:
        ts = datetime.fromisoformat(iso_ts.replace("Z","+00:00"))
        delta = datetime.utcnow() - ts.replace(tzinfo=None)
        if delta.days > 0:
            return f"{delta.days}d ago"
        if delta.seconds > 3600:
            return f"{delta.seconds//3600}h ago"
        if delta.seconds > 60:
            return f"{delta.seconds//60}m ago"
        return "just now"
    except:
        return iso_ts

def render_badges(badges: List[str]):
    if not badges:
        st.markdown("<span class='mini muted'>No badges yet</span>", unsafe_allow_html=True)
        return
    for b in badges:
        st.markdown(f"<span class='badge-pill mini'>{b}</span>", unsafe_allow_html=True)

def safe_get_user(viber_id: int) -> Dict:
    try:
        return ViberService.dao.get_by_id(viber_id) or {}
    except:
        return {}

def avatar_url(username: str):
    seed = username or "viber"
    return f"https://api.dicebear.com/6.x/bottts/svg?seed={seed}"

# ---------- Badge awarding helper ----------
def award_badge(viber_id: int, badge_name: str) -> bool:
    """
    Safely award a badge to a viber (updates vibers.badges JSONB).
    Returns True if awarded, False if already owned.
    Raises Exception if badge doesn't exist or update fails.
    """
    # 1) ensure badge exists in badges table
    badges_available = BadgeService.list() or []
    badge_names = [b.get("name") for b in badges_available]
    if badge_name not in badge_names:
        raise Exception(f"Badge '{badge_name}' does not exist in badges table.")

    # 2) fetch user
    user = ViberService.dao.get_by_id(viber_id)
    if not user:
        raise Exception("User not found.")

    current = user.get("badges", []) or []
    if badge_name in current:
        return False

    updated = current + [badge_name]
    # 3) update vibers table (assumes ViberService.dao.update(id, dict) exists)
    ViberService.dao.update(viber_id, {"badges": updated})
    return True

# ====== Session state ======
if "viber_username" not in st.session_state:
    st.session_state.viber_username = None
if "viber_id" not in st.session_state:
    st.session_state.viber_id = None
if "notif" not in st.session_state:
    st.session_state.notif = []
if "viber_badges" not in st.session_state:
    st.session_state.viber_badges = []

# ====== Auth page ======
if st.session_state.viber_id is None:
    st.markdown("<h1 style='color:#ff6ec7'>Welcome to VibeNet 🔮</h1>", unsafe_allow_html=True)
    tab = st.radio("Account", ["Sign In","Register"])
    if tab == "Sign In":
        username = st.text_input("Username", key="signin_user")
        password = st.text_input("Password", type="password", key="signin_pass")
        if st.button("Sign In"):
            user = ViberService.dao.get_by_username(username)
            if user and user.get("password") == password:
                st.session_state.viber_id = user["viber_id"]
                st.session_state.viber_username = user["username"]
                # keep session badges synced
                st.session_state.viber_badges = user.get("badges", []) or []
                st.success(f"Welcome back, {username}! 🎉")
                st.rerun()
            else:
                st.error("Invalid credentials")
    else:
        username = st.text_input("Choose username", key="reg_user")
        password = st.text_input("Choose password", type="password", key="reg_pass")
        if st.button("Register"):
            if not username or not password:
                st.warning("Fill both fields")
            else:
                try:
                    v = ViberService.dao.create(username, f"{username}@example.com", password, "Violet")
                    st.session_state.viber_id = v["viber_id"]
                    st.session_state.viber_username = v["username"]
                    st.session_state.viber_badges = v.get("badges", []) or []
                    st.success(f"Account created! Welcome {v['username']} ✨")
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not register: {str(e)}")

# ====== Main App ======
else:
    with st.sidebar:
        st.markdown(f"<div class='mini muted'>Signed in as <b>{st.session_state.viber_username}</b></div>", unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.viber_id = None
            st.session_state.viber_username = None
            st.session_state.viber_badges = []
            st.rerun()
        st.markdown("---")
        selected = st.radio("Navigation", ["Dashboard","Feed","Create Thought","Create Post","Profile","Tribes","Trending"])

    col_main, col_right = st.columns([3,1])

    # ---------- LEFT COLUMN ----------
    with col_main:
        # ---------- DASHBOARD ----------
        if selected == "Dashboard":
            st.title("Dashboard — VibeNet 🔮")
            st.markdown("<div class='card'><b>Welcome</b><div class='mini muted'>Your personal hub for vibes, tribes & trends</div></div>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            try:
                total_vibers = len(ViberService.dao.list_all() or [])
            except:
                total_vibers = "?"
            try:
                total_thoughts = len(ThoughtService.list_recent(100) or [])
            except:
                total_thoughts = "?"
            try:
                total_tribes = len(TribeService.list() or [])
            except:
                total_tribes = "?"
            c1.markdown(f"<div class='card'><div class='author'>{total_vibers}</div><div class='mini muted'>Vibers</div></div>", unsafe_allow_html=True)
            c2.markdown(f"<div class='card'><div class='author'>{total_thoughts}</div><div class='mini muted'>Thoughts</div></div>", unsafe_allow_html=True)
            c3.markdown(f"<div class='card'><div class='author'>{total_tribes}</div><div class='mini muted'>Tribes</div></div>", unsafe_allow_html=True)

            st.markdown("<div class='card'><b>Recent Thoughts</b></div>", unsafe_allow_html=True)
            try:
                rec = ThoughtService.list_recent(6)
                for t in rec:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    author = safe_get_user(t.get("viber_id"))
                    st.markdown(f"<div class='author'>{author.get('username','Viber')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='mini muted'>{timeago(t.get('created_at'))} • #{t.get('emotion_tag')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='margin-top:8px'>{t.get('content')[:220]}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
            except:
                st.info("No thoughts yet.")

        # ---------- FEED ----------
        elif selected == "Feed":
            st.title("Feed — Latest Vibes")
            search_q = st.text_input("Search thoughts", placeholder="Search content or username")
            st.markdown("<div class='card'><b>Thoughts</b> — click an emotion to echo</div>", unsafe_allow_html=True)
            try:
                thoughts = ThoughtService.list_recent(50)
                for t in thoughts:
                    author = safe_get_user(t.get("viber_id"))
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(
                        f"<div style='display:flex; align-items:center'>"
                        f"<img src='{avatar_url(author.get('username'))}' width='56' style='border-radius:12px; margin-right:12px'/>"
                        f"<div><div class='author'>{author.get('username')}</div>"
                        f"<div class='mini muted'>{timeago(t.get('created_at'))} • "
                        f"<span class='{EMOTION_CLASS.get(t.get('emotion_tag','Neutral'))}'>#{t.get('emotion_tag')}</span></div></div></div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(f"<div style='margin-top:8px'>{t.get('content')}</div>", unsafe_allow_html=True)

                    # Actions — Echo Buttons with Badge Unlocks
                    c1, c2, c3 = st.columns([1,1,1])
                    emotions = [("Joy","😊"), ("Curiosity","🤔"), ("Nostalgia","🌸")]
                    cols = [c1, c2, c3]

                    for i, (emotion, emoji) in enumerate(emotions):
                        with cols[i]:
                            key = f"{emotion}-{t['thought_id']}"
                            if st.button(f"{emoji} {emotion}", key=key):
                                if st.session_state.viber_id:
                                    try:
                                        EchoService.react(t["thought_id"], st.session_state.viber_id, emotion)
                                        st.success(f"Echoed {emotion}!")

                                        user = safe_get_user(st.session_state.viber_id)

                                        # Badge awarding (use helper that updates vibers.badges)
                                        badge_map = {
                                            "Joy": "Joyful Viber",
                                            "Curiosity": "Curious Mind",
                                            "Nostalgia": "Nostalgic Soul",
                                        }
                                        badge_to_award = badge_map.get(emotion)
                                        if badge_to_award and badge_to_award not in (user.get("badges") or []):
                                            try:
                                                awarded = award_badge(user["viber_id"], badge_to_award)
                                                if awarded:
                                                    # Refresh session badges and push notification to top
                                                    refreshed_user = ViberService.dao.get_by_id(user["viber_id"])
                                                    st.session_state.viber_badges = refreshed_user.get("badges", []) or []
                                                    st.session_state.notif.insert(0, f"🎉 You unlocked a badge: {badge_to_award}!")
                                                    st.success(f"🎉 Badge Unlocked: {badge_to_award}!")
                                            except Exception as e:
                                                st.error(f"Could not award badge: {str(e)}")

                                        # Add Echo notification
                                        st.session_state.notif.insert(0, f"{user.get('username','You')} echoed a thought with {emotion} {emoji}")

                                        # Refresh UI
                                        st.rerun()

                                    except Exception as e:
                                        msg = str(e)
                                        if "duplicate key" in msg:
                                            st.info(f"Already reacted with {emotion}")
                                        else:
                                            st.error("Echo failed: " + msg)
                                else:
                                    st.warning("Sign in first (sidebar).")
                    st.markdown("</div>", unsafe_allow_html=True)

                if not thoughts:
                    st.info("No thoughts found." if search_q else "No thoughts yet.")
            except Exception as e:
                st.error("Could not load Feed: " + str(e))

        # ---------- CREATE THOUGHT ----------
        elif selected == "Create Thought":
            st.title("Share a Thought")
            with st.form("thought_form"):
                username = st.text_input("Your username (existing)", value=st.session_state.viber_username or "")
                content = st.text_area("Your thought...", height=150)
                emotion = st.selectbox("Emotion", ["Joy","Curiosity","Nostalgia","Rage"], index=0)
                submitted = st.form_submit_button("Share")
                if submitted:
                    if not content.strip():
                        st.warning("Write something first.")
                    else:
                        try:
                            user = safe_get_user(st.session_state.viber_id)
                            ThoughtService.create(user["viber_id"], content, emotion)
                            st.success("Thought shared ✨")
                            st.rerun()
                        except Exception as e:
                            st.error("Could not create thought: " + str(e))

        # ---------- CREATE POST ----------
        elif selected == "Create Post":
            st.title("Create a Post")
            with st.form("post_form"):
                username = st.text_input(
                    "Your username (existing)",
                    value=st.session_state.viber_username or "",
                    key="post_user"
                )
                content = st.text_area("Post content...", height=150)
                submitted = st.form_submit_button("Publish")

                if submitted:
                    if not content.strip():
                        st.warning("Write something first.")
                    else:
                        try:
                            user = ViberService.dao.get_by_username(username)
                            if not user:
                                st.error("User not found.")
                            else:
                                # Create post
                                PostService.create(user["viber_id"], content)
                                st.success("Post published 🎉")
                                



                                # Award badge if not already owned (Social Viber)
                                user_badges = user.get("badges", []) or []
                                if "Explorer" not in user_badges:
                                    try:
                                        awarded = award_badge(user["viber_id"], "Explorer")
                                        if awarded:
                                            # Refresh user badges from DAO
                                            refreshed = ViberService.dao.get_by_id(user["viber_id"])
                                            st.session_state.viber_badges = refreshed.get("badges", []) or []
                                            # Add notification at the TOP
                                            st.session_state.notif.insert(0, "🎉 You unlocked a badge: Explorer!")
                                            st.success("🎉 Badge Unlocked: Explorer!")
                                    except Exception as e:
                                        st.error(f"Could not award badge: {str(e)}")
                                else:
                                    st.session_state.viber_badges = user_badges

                                st.rerun()
                        except Exception as e:
                            st.error(f"Error creating post: {str(e)}")

        # ---------- PROFILE ----------
        elif selected == "Profile":
            st.title("Profile")
            if not st.session_state.viber_id:
                st.info("Sign in to view profile.")
            else:
                user = safe_get_user(st.session_state.viber_id)
                if not user:
                    st.error("Profile not found.")
                else:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    col_a, col_b = st.columns([1,3])
                    with col_a:
                        st.image(avatar_url(user.get("username","viber")), width=140)
                    with col_b:
                        st.markdown(f"<div class='author'>{user.get('username')}</div>", unsafe_allow_html=True)
                        st.markdown(
                            f"<div class='mini muted'>Aura: <b>{user.get('aura_color')}</b> • Vibe: <b>{user.get('vibe_level','Novice')}</b></div>",
                            unsafe_allow_html=True
                        )

                        st.markdown("<div style='margin-top:8px'>Badges:</div>", unsafe_allow_html=True)
                        # prefer session badges if available so profile updates instantly
                        render_badges(st.session_state.get("viber_badges", user.get("badges", []) or []))

                        new_aura = st.selectbox(
                            "Change Aura Color",
                            ["Neutral","Violet","Blue","Gold","Rose","Crimson"],
                            index=["Neutral","Violet","Blue","Gold","Rose","Crimson"].index(user.get("aura_color","Neutral"))
                        )
                        if st.button("Save Aura"):
                            try:
                                ViberService.dao.update(user["viber_id"], {"aura_color": new_aura})
                                st.success("Aura updated ✨")
                                st.rerun()
                            except Exception as e:
                                st.error("Could not update aura: " + str(e))
                    st.markdown("</div>", unsafe_allow_html=True)

           
        elif selected == "Tribes":
            st.title("Tribes — Join your crew")
            left, right = st.columns([2,1])
            with left:
                tribes = TribeService.list() or []
                if not tribes: st.info("No tribes available yet. Start one soon!")
                for t in tribes:
                    st.markdown("<div class='card'>", unsafe_allow_html=True)
                    st.markdown(f"<div class='author'>{t.get('name')}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='mini muted'>{t.get('description')}</div>", unsafe_allow_html=True)
                    if st.button("Join Tribe", key=f"join-{t.get('tribe_id')}"):
                        if st.session_state.viber_id:
                            try:
                                TribeService.join(st.session_state.viber_id, t.get('tribe_id'))
                                st.success(f"🎉 You joined {t.get('name')}!")
                                st.session_state.notif.insert(0,f"🎉 Joined tribe {t.get('name')}")
                                try: award_badge(st.session_state.viber_id,"Tribe Member")
                                except: pass
                                st.rerun()
                            except Exception as e:
                                st.error("Could not join tribe: " + str(e))
                        else: st.warning("Sign in first.")
                    st.markdown("</div>", unsafe_allow_html=True)
            with right:
                st.markdown("<div class='card'><b>Create Tribe</b></div>", unsafe_allow_html=True)
                with st.form("new_tribe"):
                    name = st.text_input("Tribe name")
                    desc = st.text_area("Short description", height=120)
                    submitted = st.form_submit_button("Create")
                    if submitted:
                        if not name.strip(): st.warning("Provide a tribe name.")
                        else:
                            try:
                                TribeService.create(name, desc)
                                st.success("✨ Tribe created successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error("Failed to create tribe: " + str(e))
        
        
        # ---------- TRENDING ----------
        elif selected == "Trending":
            st.title("Trending — Hot Vibes 🔥")
            col_main, col_side = st.columns([3,1])

    # ----- LEFT: Top Thoughts -----
            with col_main:
                
            # Fetch recent thoughts
                    thoughts = ThoughtService.list_recent(3) or []
                    if not thoughts:
                        st.info("No trending thoughts yet. Start sharing vibes!")
                    else:
                # Sort by echo_count (most reactions first)
                        trending_thoughts = sorted(thoughts, key=lambda t: t.get("echo_count", 0), reverse=True)[:3]

                        for t in trending_thoughts:
                            author = safe_get_user(t.get("viber_id"))
                            st.markdown("<div class='card'>", unsafe_allow_html=True)
                            st.markdown(
                                f"<div style='display:flex; align-items:center'>"
                                f"<img src='{avatar_url(author.get('username'))}' width='48' style='border-radius:12px; margin-right:12px'/>"
                                f"<div><div class='author'>{author.get('username')}</div>"
                                f"<div class='mini muted'>{timeago(t.get('created_at'))} • "
                                f"<span class='{EMOTION_CLASS.get(t.get('emotion_tag','Neutral'))}'>#{t.get('emotion_tag')}</span> • "
                                f"{t.get('echo_count',0)} echoes</div></div></div>",
                                unsafe_allow_html=True
                            )
                            st.markdown(f"<div style='margin-top:6px'>{t.get('content')[:250]}</div>", unsafe_allow_html=True)

                    
    # ---------- RIGHT COLUMN ----------
  
    with col_right:
    # ----- Notifications Card -----
        st.markdown("<div class='card'><b>Notifications</b></div>", unsafe_allow_html=True)
        notifs = st.session_state.get("notif", [])

        if not notifs:
            st.markdown("<div class='mini muted'>No notifications</div>", unsafe_allow_html=True)
        else:
            for n in notifs:
                cls = "notif-item notif-new"  # Neon applied to ALL notifications
                st.markdown(f"<div class='{cls}'>{n}</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ----- Badges Card -----
        st.markdown("<div class='card'><b>Badges</b><div class='mini muted'>Create & view badges</div></div>", unsafe_allow_html=True)
        badges = BadgeService.list() or []

        if not badges:
            st.markdown("<div class='mini muted'>No badges yet</div>", unsafe_allow_html=True)
        else:
            for b in badges:
                st.markdown(
                    f"<div><b>{b.get('name')}</b>"
                    f"<div class='mini muted'>{b.get('description')}</div></div>",
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ----- Quick Tips Card -----
        st.markdown(
            "<div class='card'><b>Quick Tips</b>"
            "<div class='mini muted'>Use demo account; change aura; join tribes!</div></div>",
            unsafe_allow_html=True
        )


