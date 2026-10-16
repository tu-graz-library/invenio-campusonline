#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2021-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

ruff check .

python -m pytest
