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
"""Main application class for sourcecraft."""
import functools
import tarfile
from pathlib import Path
from typing import cast, List, Type

from craft_application import Application
from craft_cli import emit, GlobalArgument
from overrides import override  # pyright: ignore[reportUnknownVariableType]

from .commands import build
from .commands import CharmPackCommand
from .models import CharmMetadataModel, CharmProject
from .parts import CharmPartsLifecycle
from .provider import CharmProviderManager


class CharmCraft(Application):
    """SourceCraft application definition."""

    def __init__(  # noqa PLR0913 - Can't determine how to reduce arguments.
        self,
        name: str,
        version: str,
        summary: str,
        manager: CharmProviderManager,
        project_class: Type[CharmProject] = CharmProject,
    ) -> None:
        super().__init__(name, version, summary, manager, project_class)
        destructive_mode_arg = GlobalArgument(
    "destructive", "flag", None, "--destructive-mode", "Show the application version and exit"
)


    def create_package(self) -> Path:
        """Create the final package from the prime directory.

        :returns: Path to created package.
        """

        print(self.project)
        return self._pack_charm()

    @override
    def generate_metadata(self) -> None:
        """Generate the metadata in the prime directory for the Application."""
        metadata = CharmMetadataModel(
            name=self.project.name, version=self.project.version, bases=self.project.bases
        )

        metadata_file = self.parts_lifecycle.prime_dir / "source.yaml"
        metadata_file.write_text(
            metadata.yaml()  # pyright: ignore[reportUnknownMemberType]
        )

    # @override TODO: Enable this once overrides supports cached_properties.
    @functools.cached_property
    def parts_lifecycle(
        self,
    ) -> CharmPartsLifecycle:  # pyright: ignore[reportIncompatibleVariableOverride]
        """Get a parts lifecycle specifically for sourcecraft."""
        return CharmPartsLifecycle(
            self.name,
            self.project.parts,
            cache_dir=self.cache_dir,
            work_dir=Path.cwd(),
            base=self.project.effective_base,
        )

    # @override TODO: Enable this once overrides supports cached_properties.
    @functools.cached_property  # pyright: ignore[reportIncompatibleVariableOverride]
    def project(self) -> CharmProject:
        """Get the sourcecraft project metadata.

        This method exists primarily for type checking reasons.
        """
        return cast(CharmProject, super().project)


    def _pack_charm(self) -> List[Path]:
        """Pack a charm."""
        print(self.config)

        # build
        emit.progress("Packing the charm.")
        builder = build.Builder(
            config=self.config,
            debug=parsed_args.debug,
            shell=parsed_args.shell,
            shell_after=parsed_args.shell_after,
            measure=parsed_args.measure,
        )
        charms = builder.run(
            parsed_args.bases_index,
            destructive_mode=parsed_args.destructive_mode,
        )

        # avoid showing results when run inside a container (the outer charmcraft
        # is responsible of the final message to the user)

        if parsed_args.format:
            info = {"charms": charms}
            emit.message(self.format_content(parsed_args.format, info))
        else:
            emit.message("Charms packed:")
            for charm in charms:
                emit.message(f"    {charm}")
