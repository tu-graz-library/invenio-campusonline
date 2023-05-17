# -*- coding: utf-8 -*-
#
# Copyright (C) 2021-2023 Graz University of Technology.
#
# invenio-campusonline is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Module tests."""

from flask import Flask

from invenio_campusonline import InvenioCampusonline, __version__


def test_version() -> None:
    """Test version import."""
    assert __version__


def test_init() -> None:
    """Test extension initialization."""
    app = Flask("testapp")
    ext = InvenioCampusonline(app)
    assert "invenio-campusonline" in app.extensions

    app = Flask("testapp")
    ext = InvenioCampusonline()
    assert "invenio-campusonline" not in app.extensions
    ext.init_app(app)
    assert "invenio-campusonline" in app.extensions
