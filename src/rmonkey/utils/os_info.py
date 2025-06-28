import platform


def system(xml=True) -> str:
    name = f"system/OS name: {platform.system()}".strip()
    arch = f"arch: {platform.machine()}".strip()
    info = f"{name}\n{arch}"
    if xml:
        return f"<platform>\n{info}\n</platform>"
    return info
