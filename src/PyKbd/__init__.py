# This file is part of PyKbd
#
# Copyright (C) 2019  Nulano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

_version = "0.1.0-dev0"
_version_num = (0, 1, 0)

try:
    import subprocess as _subprocess

    _s = _subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True)
    _commit = _s.stdout.decode("ascii").strip()
    __version__ = f"{_version} ({_commit})"
except Exception:
    __version__ = _version

print(f"Importing PyKbd version {__version__}")
