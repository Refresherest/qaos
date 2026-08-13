from qaos.agents import agent_manager
from qaos.config import create_configuration
from qaos.council import council_manager
from qaos.plugins import plugin_manager
from qaos.services import StatusService


def execute():
    status_service = StatusService(
        create_configuration(),
        agent_manager,
        council_manager,
        plugin_manager,
    )
    data = status_service.get_status()

    print("=" * 50)
    print("QAOS Runtime Status")
    print("=" * 50)
    print()

    print(f"Kernel              {data['kernel']}")
    print(f"Runtime             {data['runtime']}")
    print(f"Configuration       {data['configuration']}")
    print(f"Environment         {data['environment']}")
    print(f"Version             {data['version']}")
    print()

    print(f"Executive Council   {data['council']}")
    print(f"Agents              {data['agents']}")
    print(f"Plugins             {data['plugins']}")
    print()

    print(f"Status              {data['status']}")
