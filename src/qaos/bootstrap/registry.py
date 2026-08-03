BOOT_STEPS = []


def register(step):
    BOOT_STEPS.append(step)


def steps():
    return BOOT_STEPS