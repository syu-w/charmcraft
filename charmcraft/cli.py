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
"""Command-line interface entrypoint."""

import charmcraft
from . import CharmCraft
from .models import CharmProject
from .provider import CharmProviderManager

APP_NAME = "charmcraft"


def main() -> int:
    """Start up and run charmcraft."""
    provider_manager = CharmProviderManager(APP_NAME)

    app = CharmCraft(
        name=APP_NAME,
        version=charmcraft.__version__,
        summary="Verify your sources",
        manager=provider_manager,
        project_class=CharmProject,
    )

    return app.run()
