from qaos.services import status_service


def execute():
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