# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""The module is used to import/export from/to the CampusOnline System."""

from .ext import InvenioCampusonline
from .proxies import current_campusonline
from .services import CampusOnlineRESTService
from .types import CampusOnlineID, ThesesFilter

__version__ = "0.7.4"

__all__ = (
    "CampusOnlineID",
    "CampusOnlineRESTService",
    "InvenioCampusonline",
    "ThesesFilter",
    "__version__",
    "current_campusonline",
)
