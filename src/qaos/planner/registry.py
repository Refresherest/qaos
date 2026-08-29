"""
QAOS Plan Registry
"""

class PlanRegistry:
    """Registry state owned by one planner-manager lifecycle."""

    def __init__(self):
        self._by_objective_id = {}
        self._by_goal = {}
        self._records = []

    def register(self, plan):
        objective_id = getattr(plan, "objective_id", None)

        if objective_id is not None:
            existing = self._by_objective_id.get(objective_id)
            if existing is not None and existing is not plan:
                raise ValueError(f"duplicate plan objective_id: {objective_id}")
            self._by_objective_id[objective_id] = plan

        if plan not in self._records:
            self._records.append(plan)

        self._by_goal[plan.objective] = plan

    def unregister(self, objective):
        plan = self.get(objective)
        if plan is None:
            return

        self._records.remove(plan)

        if plan.objective_id is not None:
            self._by_objective_id.pop(plan.objective_id, None)

        if self._by_goal.get(plan.objective) is plan:
            self._by_goal.pop(plan.objective, None)
            for candidate in reversed(self._records):
                if candidate.objective == plan.objective:
                    self._by_goal[plan.objective] = candidate
                    break

    def get(self, objective):
        if hasattr(objective, "goal"):
            objective_id = getattr(objective, "objective_id", None)
            if objective_id is not None:
                return self._by_objective_id.get(objective_id)
            objective = objective.goal

        return self._by_goal.get(objective)

    def get_by_objective_id(self, objective_id):
        return self._by_objective_id.get(objective_id)

    def records(self):
        return tuple(self._records)

    def all(self):
        return self._by_goal


plan_registry = PlanRegistry()


def register(plan):
    plan_registry.register(plan)


def unregister(objective):
    plan_registry.unregister(objective)


def get(objective):
    return plan_registry.get(objective)


def get_by_objective_id(objective_id):
    return plan_registry.get_by_objective_id(objective_id)


def records():
    return plan_registry.records()


def all():
    return plan_registry.all()
