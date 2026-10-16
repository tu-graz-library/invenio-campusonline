# SPDX-FileCopyrightText: 2022-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

"""Command line interface to interact with the CampusOnline-Connector module."""

from datetime import datetime
from xml.etree.ElementTree import Element

from .types import Embargo


def extract_embargo_range(thesis: Element) -> Embargo:
    """Extract the embargo range."""
    ns = "http://www.campusonline.at/thesisservice/basetypes"
    xpath_start = f".//{{{ns}}}attr[@key='SPVON']"
    xpath_end = f".//{{{ns}}}attr[@key='SPBIS']"
    start = thesis.find(xpath_start)
    end = thesis.find(xpath_end)

    if start is None or end is None:
        return Embargo()

    if start.text is None or end.text is None:
        return Embargo()

    in_format = "%Y-%m-%d %H:%M:%S"
    start_embargo = datetime.strptime(start.text, in_format)
    end_embargo = datetime.strptime(end.text, in_format)

    return Embargo(start_embargo, end_embargo)
