# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services configs."""

from dataclasses import dataclass
from typing import ClassVar

from ..records import CampusOnlineAPI, CampusOnlineRESTConfig


@dataclass
class CampusOnlineRESTServiceConfig(CampusOnlineRESTConfig):
    """Campusonline REST service config."""

    api_cls: ClassVar = CampusOnlineAPI
