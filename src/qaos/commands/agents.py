from qaos.agents import AGENTS


def execute():
    print("=" * 50)
    print("QAOS Registered Agents")
    print("=" * 50)
    print()

    for name, agent in AGENTS.items():
        print(f"{name:<20} {agent.title}")