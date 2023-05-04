# Copyright 2023 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Basic lifecycle commands for a Craft Application."""

# Tell pyright to ignore unnecessary type:ignore comments.
# This is because _LifestyleCommand.run currently does things that mypy needs
# an ignore on but pyright does not.
# pyright: reportUnnecessaryTypeIgnoreComment=false

import abc
import textwrap
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    cast,
)

from craft_cli import CommandGroup, emit
from craft_parts.features import Features
from overrides import overrides

from craft_application.commands.base import AppCommand
from craft_application.commands.lifecycle import _LifecycleCommand, PullCommand, BuildCommand, StageCommand, PackCommand, PrimeCommand, CleanCommand


def get_lifecycle_command_group() -> CommandGroup:
    """Return the lifecycle related command group."""
    # Craft CLI mangles the order, but we keep it this way for when it won't
    # anymore.
    commands: List[Type[_LifecycleCommand]] = [
        CleanCommand,
        PullCommand,
    ]

    commands.extend(
        [
            BuildCommand,
            StageCommand,
            PrimeCommand,
            PackCommand,
        ]
    )

    return CommandGroup(
        "Lifecycle",
        commands,
    )


class CharmPackCommand(PackCommand):
    """Command to pack the final artifact."""

    def run(
        self, parsed_args: "argparse.Namespace", step_name: Optional[str] = None
    ) -> None:
        """Run the pack command."""
        if step_name not in ("pack", None):
            raise RuntimeError(f"Step name {step_name} passed to pack command.")
        super().run(parsed_args, step_name="prime")

        create_package = self._callbacks["create_package"]
        package_name = create_package()

        emit.message(f"Packed {str(package_name)!r}")
