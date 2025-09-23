
import argparse
from src.services.viber_service import ViberService
from src.services.thought_service import ThoughtService
from src.services.post_service import PostService
from src.services.reverberation_service import ReverberationService
from src.services.soul_link_service import SoulLinkService
from src.services.echo_service import EchoService
from src.services.badge_service import BadgeService
from src.services.tribe_service import TribeService


def handle_viber(args):
    if args.action == "register":
        viber = ViberService.register(args.username, args.email, args.password, args.aura_color)
        print("✅ Viber Registered:", viber)
    elif args.action == "list":
        vibers = ViberService.list()
        for v in vibers:
            print(v)
    elif args.action == "get":
        viber = ViberService.get(args.viber_id)
        print(viber or "❌ Not found")

def handle_thought(args):
    if args.action == "create":
        thought = ThoughtService.create(args.viber_id, args.content, args.emotion_tag)
        print("✅ Thought Created:", thought)
    elif args.action == "list":
        thoughts = ThoughtService.list_recent()
        for t in thoughts:
            print(t)

def handle_post(args):
    if args.action == "create":
        post = PostService.create(args.user_id, args.content)
        print("✅ Post Created:", post)
    elif args.action == "list":
        posts = PostService.list_recent()
        for p in posts:
            print(p)
    elif args.action == "like":
        post = PostService.like(args.post_id)
        print("👍 Post Liked:", post)


def handle_reverberation(args):
    if args.action == "create":
        r = ReverberationService.create(args.thought_id, args.viber_id, args.content)
        print(r)
    elif args.action == "list":
        r = ReverberationService.list(args.thought_id)
        print(r)

def handle_soul_link(args):
    if args.action == "create":
        s = SoulLinkService.create(args.viber_id, args.friend_id)
        print(s)
    elif args.action == "update":
        s = SoulLinkService.update_status(args.link_id, args.status)
        print(s)

def handle_echo(args):
    if args.action == "react":
        e = EchoService.react(args.thought_id, args.viber_id, args.emotion)
        print(e)

def handle_badge(args):
    if args.action == "create":
        b = BadgeService.create(args.name, args.description, args.aura_color, args.vibe_level)
        print(b)
    elif args.action == "list":
        b = BadgeService.list()
        print(b)
def handle_tribe(args):
    if args.action == "create":
        tribe = TribeService.create(args.name, args.description)
        print("🏕 Tribe Created:", tribe)
    elif args.action == "list":
        tribes = TribeService.list()
        for t in tribes:
            print(t)
    elif args.action == "join":
        membership = TribeService.join(args.viber_id, args.tribe_id)
        print("🤝 Joined Tribe:", membership)
    elif args.action == "mytribes":
        tribes = TribeService.list_viber_tribes(args.viber_id)
        print("📜 Tribes Joined:", tribes)

def main():
    parser = argparse.ArgumentParser(prog="vibenet-cli")
    subparsers = parser.add_subparsers(dest="entity")

    # Viber
    viber_parser = subparsers.add_parser("viber")
    viber_sub = viber_parser.add_subparsers(dest="action")

    reg = viber_sub.add_parser("register")
    reg.add_argument("--username", required=True)
    reg.add_argument("--email", required=True)
    reg.add_argument("--password", required=True)
    reg.add_argument("--aura_color", default="Neutral")

    viber_sub.add_parser("list")
    get_cmd = viber_sub.add_parser("get")
    get_cmd.add_argument("--viber_id", type=int, required=True)

    # Thought
    thought_parser = subparsers.add_parser("thought")
    thought_sub = thought_parser.add_subparsers(dest="action")

    create_t = thought_sub.add_parser("create")
    create_t.add_argument("--viber_id", type=int, required=True)
    create_t.add_argument("--content", required=True)
    create_t.add_argument("--emotion_tag", choices=["Joy", "Curiosity", "Nostalgia", "Rage"], required=True)

    thought_sub.add_parser("list")

    # Post
    post_parser = subparsers.add_parser("post")
    post_sub = post_parser.add_subparsers(dest="action")

    create_p = post_sub.add_parser("create")
    create_p.add_argument("--user_id", type=int, required=True)
    create_p.add_argument("--content", required=True)

    post_sub.add_parser("list")

    like_p = post_sub.add_parser("like")
    like_p.add_argument("--post_id", type=int, required=True)
    
    
     
    rev_parser = subparsers.add_parser("reverberation")
    rev_parser.add_argument("action", choices=["create", "list"])
    rev_parser.add_argument("--thought_id", type=int)
    rev_parser.add_argument("--viber_id", type=int)
    rev_parser.add_argument("--content")

    # Soul links
    soul_parser = subparsers.add_parser("soul")
    soul_parser.add_argument("action", choices=["create", "update"])
    soul_parser.add_argument("--viber_id", type=int)
    soul_parser.add_argument("--friend_id", type=int)
    soul_parser.add_argument("--link_id", type=int)
    soul_parser.add_argument("--status", choices=["PENDING", "ACCEPTED", "REJECTED"])

    # Echo
    echo_parser = subparsers.add_parser("echo")
    echo_parser.add_argument("action", choices=["react"])
    echo_parser.add_argument("--thought_id", type=int)
    echo_parser.add_argument("--viber_id", type=int)
    echo_parser.add_argument("--emotion", choices=["Joy", "Curiosity", "Nostalgia", "Rage"])

    # Badges
    badge_parser = subparsers.add_parser("badge")
    badge_parser.add_argument("action", choices=["create", "list"])
    badge_parser.add_argument("--name")
    badge_parser.add_argument("--description")
    badge_parser.add_argument("--aura_color")
    badge_parser.add_argument("--vibe_level", type=int)
    
    
        # Tribes
    tribe_parser = subparsers.add_parser("tribe")
    tribe_sub = tribe_parser.add_subparsers(dest="action")

    create_tr = tribe_sub.add_parser("create")
    create_tr.add_argument("--name", required=True)
    create_tr.add_argument("--description", required=True)

    tribe_sub.add_parser("list")

    join_tr = tribe_sub.add_parser("join")
    join_tr.add_argument("--viber_id", type=int, required=True)
    join_tr.add_argument("--tribe_id", type=int, required=True)

    mytribes = tribe_sub.add_parser("mytribes")
    mytribes.add_argument("--viber_id", type=int, required=True)

    
    
    args = parser.parse_args()

    if args.entity == "viber":
        handle_viber(args)
    elif args.entity == "thought":
        handle_thought(args)
    elif args.entity == "post":
        handle_post(args)
    
    elif args.entity == "reverberation":
        handle_reverberation(args)
    elif args.entity == "soul":
        handle_soul_link(args)
    elif args.entity == "echo":
        handle_echo(args)
    elif args.entity == "badge":
        handle_badge(args)
    elif args.entity == "tribe":
        handle_tribe(args)

    else:
        parser.print_help()
        
       

    

if __name__ == "__main__":
    main()

