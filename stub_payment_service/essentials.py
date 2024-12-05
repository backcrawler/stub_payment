import re
from pathlib import Path

from .exceptions import PotentialInjectionError

_pattern = re.compile("[A-Za-z0-9_]+")


def is_docker() -> bool:
    """Check whether this is inside docker container or not."""
    path = Path("/proc/self/cgroup")
    return (
        Path.exists(Path(path, "/.dockerenv"))
        or path.is_file()
        and any("docker" in line for line in path.open())
    )


def check_for_injections(values: str) -> None:
    if not re.match(_pattern, values):
        raise PotentialInjectionError
