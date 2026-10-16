# SPDX-FileCopyrightText: 2024-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Services decorators."""


from collections.abc import Callable
from functools import wraps
from typing import Any

from .config import CampusOnlineRESTServiceConfig
from .services import CampusOnlineRESTService


def build_services(f: Callable) -> Callable:
    """Decorate to build the services."""

    @wraps(f)
    def build(*_: dict, **kwargs: dict) -> Any:  # noqa: ANN401
        endpoint = kwargs.pop("endpoint")
        token = kwargs.pop("token")

        config = CampusOnlineRESTServiceConfig(endpoint, token)
        kwargs["cms_service"] = CampusOnlineRESTService(config)

        return f(**kwargs)

    return build
