from pathlib import Path


STANDARD_DIRECTORIES = [
    "docs",
    "docs/architecture",
    "docs/roadmap",
    "docs/specifications",
    "src",
    "tests",
]


def execute():
    print("=" * 50)
    print("QAOS Bootstrap")
    print("=" * 50)

    project = Path.cwd()

    for directory in STANDARD_DIRECTORIES:
        path = project / directory

        if path.exists():
            print(f"✓ {directory}")
        else:
            print(f"+ Create {directory}")