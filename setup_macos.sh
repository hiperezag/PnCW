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

is_python_312() {
  "$1" -c 'import sys; raise SystemExit(sys.version_info[:2] != (3, 12))' >/dev/null 2>&1
}

python_executable=''
if [ -n "${PNCW_PYTHON:-}" ]; then
  if ! is_python_312 "$PNCW_PYTHON"; then
    printf 'PNCW_PYTHON must point to a working Python 3.12 interpreter.\n' >&2
    exit 1
  fi
  python_executable=$PNCW_PYTHON
else
  for candidate in python3.12 python3; do
    if command -v "$candidate" >/dev/null 2>&1 && is_python_312 "$candidate"; then
      python_executable=$(command -v "$candidate")
      break
    fi
  done
  if [ -z "$python_executable" ]; then
    for brew_candidate in brew /opt/homebrew/bin/brew /usr/local/bin/brew; do
      if command -v "$brew_candidate" >/dev/null 2>&1; then
        brew_prefix=$("$brew_candidate" --prefix python@3.12 2>/dev/null || true)
        if [ -n "$brew_prefix" ] && is_python_312 "$brew_prefix/bin/python3.12"; then
          python_executable=$brew_prefix/bin/python3.12
          break
        fi
      fi
    done
  fi
fi

if [ -z "$python_executable" ]; then
  printf 'Python 3.12 was not found. Install it, then rerun this script.\n' >&2
  printf 'With Homebrew: brew install python@3.12\n' >&2
  printf 'Without Homebrew: https://www.python.org/downloads/\n' >&2
  exit 1
fi

printf 'Using %s\n' "$python_executable"
if [ "${1:-}" = '--check' ]; then
  exit 0
fi

if [ -L .venv ]; then
  printf '.venv is a symbolic link; replace it with a local directory before setup.\n' >&2
  exit 1
fi

"$python_executable" -m venv --clear .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -c 'import numpy, matplotlib; print("Ready: NumPy", numpy.__version__, "Matplotlib", matplotlib.__version__)'
