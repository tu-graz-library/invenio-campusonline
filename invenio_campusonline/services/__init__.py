# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services."""

from .config import CampusOnlineRESTServiceConfig
from .services import CampusOnlineRESTService

__all__ = (
    "CampusOnlineRESTService",
    "CampusOnlineRESTServiceConfig",
)
