# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see LICENSE
# file for more details.


"""Types."""

from dataclasses import astuple, dataclass
from enum import Enum
from xml.etree.ElementTree import Element

URL = str
CampusOnlineToken = str
CampusOnlineID = str
FilePath = str
EmailAddress = str


class ThesesState(Enum):
    """Theses State class."""

    LOCKED = 1
    OPEN = 2


@dataclass
class ThesesFilter:
    """Filter dataclass."""

    filter_: list[Element]
    state: ThesesState

    def __iter__(self):
        return iter(astuple(self))


@dataclass
class CampusOnlineConfigs:
    """Configs for campus online."""

    endpoint: URL
    token: CampusOnlineToken
    user_email: EmailAddress
    theses_filters: ThesesFilter
    recipients: list[EmailAddress]
    sender: EmailAddress
