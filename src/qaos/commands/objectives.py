"""Read-only complete Objective listing for one explicit workspace."""

import json
from pathlib import Path

from qaos.objectives import ObjectiveManager
from qaos.storage import create_stores


def execute(workspace):
    if not Path(workspace).is_dir():
        raise ValueError("Listing requires an existing workspace directory")

    records = ObjectiveManager(stores=create_stores(workspace)).objective_records()
    lines = [json.dumps({
        "objective_id": objective.objective_id,
        "status": objective.status,
        "goal": objective.goal,
    }, ensure_ascii=True, sort_keys=True) for objective in records]

    if not lines:
        print("Objectives: []")
    else:
        print("Objectives:")
        for line in lines:
            print(line)
    return records
