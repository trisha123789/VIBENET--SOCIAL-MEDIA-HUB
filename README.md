# VIBENET--SOCIAL-MEDIA-HUB

**🌐 Vibenet - Social Media Hub**

-------Where every Vibe finds its Tribe

Vibenet is a Python-based, command-line social media hub that allows users ("Vibers") to post thoughts, react, comment, earn badges, join tribes, and explore trending content. This project demonstrates a fully functional social platform backend with a menu-driven CLI interface, ideal for learning, experimentation, and gamified social networking.
<img width="1242" height="695" alt="tavles created" src="https://github.com/user-attachments/assets/a6d99a08-e67b-44a1-8f2b-974c162c1800" />


🚀 Features

Vibers (Users)

Register with username, email, and password.

List all Vibers or view specific Viber details.

Aura color and vibe level system to personalize users.

Thoughts

Create, view, and track thoughts with emotion tags: Joy, Curiosity, Nostalgia, Rage.

Thoughts can receive echoes, reactions, and comments.

Posts

Create posts with content.

Like posts, track echoes, and view awarded batches.

Reverberations (Comments)

Comment on thoughts and list all comments for a thought.

Soul Links (Friendships)

Create friendship requests.

Update friendship status: PENDING, ACCEPTED, REJECTED.

Echoes (Reactions)

React to thoughts with specific emotion tags.

Badges

Create badges with aura colors and vibe level requirements.

List all badges and track which Vibers earned them.

Tribes

Create tribes with a name and description.

Join existing tribes.

List tribes a Viber has joined.

Menu-driven CLI

Fully interactive and user-friendly.

Step-by-step prompts for all operations.

Optional arguments mode for automated actions.


🔧 Modules & Methods
1️⃣ Viber

DAO: viber_dao.py

insert(username, email, password, aura_color) – add a new Viber

get(viber_id) – fetch Viber by ID

list_all() – fetch all Vibers

Service: viber_service.py

register(username, email, password, aura_color) – handles registration

get(viber_id) – retrieves Viber info

list() – returns all Vibers

2️⃣ Thought

DAO: thought_dao.py

insert(viber_id, content, emotion_tag) – create thought

list_recent() – fetch recent thoughts

Service: thought_service.py

create(viber_id, content, emotion_tag) – adds new thought

list_recent() – returns recent thoughts

3️⃣ Post

DAO: post_dao.py

insert(user_id, content) – create a post

list_recent() – fetch recent posts

increment_likes(post_id) – increase like count

Service: post_service.py

create(user_id, content) – create post

list_recent() – return recent posts

like(post_id) – like a post

4️⃣ Reverberation (Comment)

DAO: reverberation_dao.py

insert(thought_id, viber_id, content) – add comment

list_by_thought(thought_id) – fetch comments

Service: reverberation_service.py

create(thought_id, viber_id, content) – add comment

list(thought_id) – list comments

5️⃣ Soul Links (Friendships)

DAO: soul_link_dao.py

insert(viber_id, friend_id) – create friendship request

update_status(link_id, status) – update request status

Service: soul_link_service.py

create(viber_id, friend_id) – request friendship

update_status(link_id, status) – update friendship status

6️⃣ Echo (Reaction)

DAO: echo_dao.py

insert(thought_id, viber_id, emotion_tag) – add reaction

Service: echo_service.py

react(thought_id, viber_id, emotion) – react to a thought

7️⃣ Badge

DAO: badge_dao.py

insert(name, description, aura_color, vibe_level_required) – create badge

list_all() – list all badges

Service: badge_service.py

create(name, description, aura_color, vibe_level) – create badge

list() – return all badges

8️⃣ Tribe

DAO: tribe_dao.py

insert(name, description) – create tribe

list_all() – list all tribes

join(viber_id, tribe_id) – join a tribe

list_viber_tribes(viber_id) – list tribes a Viber joined

Service: tribe_service.py

create(name, description) – add tribe

list() – list all tribes

join(viber_id, tribe_id) – join a tribe

list_viber_tribes(viber_id) – list a Viber’s tribes

Setup PostgreSQL / Supabase:

Run db/schema.sql to create tables.

Configure Supabase credentials in src/config.py.

Run the CLI:

python -m src.cli.main

🎮 Usage Examples

Register a Viber:

python -m src.cli.main viber register --username "Trisha" --email "trisha@example.com" --password "1234"


Create a Thought:

python -m src.cli.main thought create --viber_id 1 --content "Exploring vibes!" --emotion_tag Joy


Like a Post:

python -m src.cli.main post like --post_id 1


Join a Tribe:

python -m src.cli.main tribe join --viber_id 1 --tribe_id 2


List Joined Tribes:

python -m src.cli.main tribe mytribes --viber_id 1

📌 Future Enhancements

Real-time notifications and feed.

Trending thoughts algorithm.

Gamification and leaderboard.

Media uploads for posts and thoughts.

REST API backend integration.

👩‍💻 Author

Trisha – Passionate developer building AI/ML-powered and social network projects.

📜 License

Open-source – use, modify, and contribute freely.
