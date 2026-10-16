# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Records."""

from .api import CampusOnlineAPI
from .config import CampusOnlineRESTConfig
from .models import CampusOnlineConnection

__all__ = (
    "CampusOnlineAPI",
    "CampusOnlineConnection",
    "CampusOnlineRESTConfig",
)
