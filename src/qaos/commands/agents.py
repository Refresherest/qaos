from qaos.agents import agent_manager


def execute():
    print("=" * 50)
    print("QAOS Agents")
    print("=" * 50)
    print()

    agents = agent_manager.agents()

    if not agents:
        print("No agents registered.")
        return

    for key, agent in agents.items():
        print(f"{key:<25} {agent.title}")