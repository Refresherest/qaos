from qaos.council import EXECUTIVE_COUNCIL


def execute():
    print("=" * 50)
    print("QAOS Executive Council")
    print("=" * 50)
    print()

    for key, member in EXECUTIVE_COUNCIL.items():
        print(f"{key:<20} {member.title}")