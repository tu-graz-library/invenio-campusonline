# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Helper proxy to the state object."""

from typing import cast

from flask import current_app
from werkzeug.local import LocalProxy

from .ext import InvenioCampusonline

current_campusonline: InvenioCampusonline = cast(
    InvenioCampusonline,
    LocalProxy(lambda: current_app.extensions["invenio-campusonline"]),
)
"""Helper proxy to get teh current campusonline extension."""
