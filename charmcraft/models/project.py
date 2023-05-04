#  This file is part of sourcecraft.
#
#  Copyright 2023 Canonical Ltd.
#
#  This program is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License version 3, as
#  published by the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
#  SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.
"""sourcecraft project definition.

This module defines a sourcecraft.yaml file, exportable to a JSON schema.
"""
from typing import Dict, List, Optional

from craft_application import Project
from craft_application.types import PlatformDict


class CharmProject(Project):
    """CharmCraft project definition."""

    # Base is mandatory for source projects.
    # base: str  # type: ignore[assignment]
    # platforms: Dict[str, Optional[PlatformDict]]
    type: str
    bases: Optional[List[Dict[str, List[Dict[str, str]]]]]
    charmhub: Optional[Dict[str, str]]
