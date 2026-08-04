_ACTIONS = {}


def register(action):
    _ACTIONS[action.name] = action


def get(name):
    return _ACTIONS.get(name)


def all():
    return dict(_ACTIONS)