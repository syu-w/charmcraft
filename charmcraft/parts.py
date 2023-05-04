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
"""PartsLifecycle for sourcecraft."""

from typing import Any, Dict, List, Optional, cast
from craft_cli import emit
from craft_application import PartsLifecycle
from craft_application.errors import PartsLifecycleError
from craft_parts import LifecycleManager, Step, plugins, callbacks


class CharmPartsLifecycle(PartsLifecycle):
    """Parts lifecycle for sourcecraft.


    Contains any sourcecraft specific parts lifecycle handling..
    """

    def run(self, step_name: str, part_names: Optional[List[str]]) -> None:
        """Run the lifecycle manager for the parts."""
        try:
            target_step = self._lifecycle_steps[step_name]
        except KeyError as key_error:
            raise RuntimeError(f"Invalid target step {step_name!r}") from key_error

        try:
            if step_name:
                actions = self._lcm.plan(target_step, part_names=part_names)
            else:
                actions = []

            with self._lcm.action_executor() as aex:
                for action in actions:
                    message = _action_message(action)
                    emit.progress(f"Executing parts lifecycle: {message}")
                    with emit.open_stream("Executing action") as stream:
                        aex.execute(action, stdout=stream, stderr=stream)
                    emit.progress(f"Executed: {message}", permanent=True)

                emit.progress("Executed parts lifecycle", permanent=True)
        except RuntimeError as err:
            raise RuntimeError(f"Parts processing internal error: {err}") from err
        except OSError as err:
            msg = err.strerror
            if err.filename:
                msg = f"{err.filename}: {msg}"
            raise errors.PartsLifecycleError(msg) from err
        except Exception as err:  # noqa BLE001: Converting general error.
            raise errors.PartsLifecycleError(str(err)) from err

