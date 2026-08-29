"""
QAOS Objective Registry
"""

class ObjectiveRegistry:
    """Registry state owned by one objective-manager lifecycle."""

    def __init__(self):
        self._by_id = {}
        self._by_goal = {}
        self._records = []

    def register(self, objective):
        objective_id = getattr(objective, "objective_id", None)

        if objective_id is not None:
            existing = self._by_id.get(objective_id)
            if existing is not None and existing is not objective:
                raise ValueError(f"duplicate objective_id: {objective_id}")
            self._by_id[objective_id] = objective

        if objective not in self._records:
            self._records.append(objective)

        self._by_goal[objective.goal] = objective

    def unregister(self, objective):
        registered = self.get(objective)
        if registered is None:
            return

        self._records.remove(registered)

        objective_id = getattr(registered, "objective_id", None)
        if objective_id is not None:
            self._by_id.pop(objective_id, None)

        if self._by_goal.get(registered.goal) is registered:
            self._by_goal.pop(registered.goal, None)
            for candidate in reversed(self._records):
                if candidate.goal == registered.goal:
                    self._by_goal[registered.goal] = candidate
                    break

    def get(self, objective):
        if hasattr(objective, "goal"):
            objective_id = getattr(objective, "objective_id", None)
            if objective_id is not None:
                return self._by_id.get(objective_id)
            objective = objective.goal

        return self._by_goal.get(objective)

    def get_by_id(self, objective_id):
        return self._by_id.get(objective_id)

    def records(self):
        return tuple(self._records)

    def all(self):
        return self._by_goal


objective_registry = ObjectiveRegistry()


def register(objective):
    objective_registry.register(objective)


def unregister(objective):
    objective_registry.unregister(objective)


def get(objective):
    return objective_registry.get(objective)


def get_by_id(objective_id):
    return objective_registry.get_by_id(objective_id)


def records():
    return objective_registry.records()


def all():
    return objective_registry.all()
