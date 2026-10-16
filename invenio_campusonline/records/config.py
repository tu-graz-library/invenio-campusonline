# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""API."""

from dataclasses import dataclass

from ..types import URL, CampusOnlineToken


@dataclass
class CampusOnlineRESTConfig:
    """Campus online rest config."""

    endpoint: URL = ""
    token: CampusOnlineToken = ""
