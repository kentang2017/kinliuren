# Vendored copy of kinqimen + its internal config
# This avoids the "import config" top-level module error from the pip version.
# The original package used bare "import config" which only works with path hacks.

from . import kinqimen
from . import config

__all__ = ["kinqimen", "config", "Qimen"]
Qimen = kinqimen.Qimen
