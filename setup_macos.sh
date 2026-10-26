#!/bin/sh
# SPDX-FileCopyrightText: 2026 PnCW project authors and contributors
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -eu

cd "$(dirname "$0")"

case "${1:-}" in
  ''|--check) ;;
  *) printf 'Usage: sh setup_macos.sh [--check]\n' >&2; exit 2 ;;
esac

is_supported_python() {
  "$1" -c 'import sys; raise SystemExit(not (3, 9) <= sys.version_info[:2] <= (3, 14))' >/dev/null 2>&1
}

python_executable=''
if [ -n "${PNCW_PYTHON:-}" ]; then
  if ! is_supported_python "$PNCW_PYTHON"; then
    printf 'PNCW_PYTHON must point to a working Python 3.9-3.14 interpreter.\n' >&2
    exit 1
  fi
  python_executable=$PNCW_PYTHON
else
  for candidate in python3 python python3.14 python3.13 python3.12 python3.11 python3.10 python3.9; do
    if command -v "$candidate" >/dev/null 2>&1 && is_supported_python "$candidate"; then
      python_executable=$(command -v "$candidate")
      break
    fi
  done
fi

if [ -z "$python_executable" ]; then
  printf 'No supported Python interpreter was found in PATH (Python 3.9-3.14).\n' >&2
  printf 'Use PNCW_PYTHON=/absolute/path/to/python or see README.txt.\n' >&2
  exit 1
fi

# Compatibility entry point; installation logic is shared with Windows/Linux.
exec "$python_executable" setup_env.py "$@"
