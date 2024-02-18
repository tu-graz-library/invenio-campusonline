# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Services configs."""

from dataclasses import dataclass

from ..types import URL, CampusOnlineToken


@dataclass
class CampusOnlineRESTServiceConfig:
    """Campusonline REST service config."""

    endpoint: URL = ""
    token: CampusOnlineToken = ""
