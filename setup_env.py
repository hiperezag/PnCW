#!/usr/bin/env python3
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

"""Install PnCW using the Python interpreter that runs this script.

macOS/Linux: python3 setup_env.py
Windows:    py setup_env.py
Use --check to inspect the interpreter without creating an environment.
Use --check-env to check this interpreter and its plotting dependencies.
"""
import argparse
from importlib.metadata import PackageNotFoundError, version
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent
MIN_PYTHON = (3, 9)
MAX_PYTHON = (3, 14)


def check_python():
    if not MIN_PYTHON <= sys.version_info[:2] <= MAX_PYTHON:
        raise RuntimeError(
            'PnCW supports Python 3.9-3.14; this interpreter is Python '
            + platform.python_version() + '. Use a supported installed interpreter.')


def check_environment():
    """Validate the active requirements, including Python-version markers."""
    check_python()
    try:
        from packaging.requirements import Requirement
        requirements = (ROOT / 'requirements.txt').read_text(encoding='utf-8')
        versions = {}
        for line in requirements.splitlines():
            line = line.split('#', 1)[0].strip()
            if not line:
                continue
            requirement = Requirement(line)
            if requirement.marker and not requirement.marker.evaluate():
                continue
            installed = version(requirement.name)
            if not requirement.specifier.contains(installed, prereleases=False):
                raise RuntimeError(
                    requirement.name + ' ' + installed + ' is outside '
                    + str(requirement.specifier) + '.')
            versions[requirement.name] = installed
        # Check binary imports as well as package metadata (e.g. NumPy ABI).
        import numpy
        os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'generated' / '.matplotlib'))
        import matplotlib
        return dict(python=platform.python_version(),
                    implementation=platform.python_implementation(),
                    platform=platform.platform(), executable=sys.executable,
                    dependencies=versions)
    except (ImportError, PackageNotFoundError, RuntimeError) as error:
        raise RuntimeError(
            str(error) + ' Run setup_env.py with a supported interpreter, '
            'then use the resulting virtual-environment Python.') from error


def run(command, env):
    print('Running: ' + subprocess.list2cmdline([str(item) for item in command]), flush=True)
    subprocess.run([str(item) for item in command], check=True, env=env)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    checks = parser.add_mutually_exclusive_group()
    checks.add_argument('--check', action='store_true', help='Check Python only; no installation')
    checks.add_argument('--check-env', action='store_true', help='Check installed plotting dependencies')
    parser.add_argument('--venv', type=Path, default=ROOT / '.venv',
                        help='Virtual-environment directory (default: .venv in this package)')
    args = parser.parse_args()
    check_python()
    print('Using Python ' + platform.python_version() + ': ' + sys.executable, flush=True)
    if args.check:
        return
    if args.check_env:
        print(json.dumps(check_environment(), indent=2))
        return

    environment = args.venv.absolute()
    if environment.is_symlink() or environment.resolve() == ROOT:
        raise RuntimeError('Choose a dedicated local virtual-environment directory, not a symlink or the package root.')
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if environment.exists():
        if not (environment / 'pyvenv.cfg').is_file() or not python.is_file():
            raise RuntimeError('The environment directory is not a working venv. Choose another --venv directory.')
        existing = subprocess.check_output(
            [str(python), '-c', 'import sys; print("%s.%s" % sys.version_info[:2])'],
            text=True).strip()
        if existing != '%s.%s' % sys.version_info[:2]:
            raise RuntimeError('The existing venv uses Python ' + existing
                               + '. Use its original interpreter or choose another --venv directory.')
    else:
        try:
            venv.EnvBuilder(with_pip=True).create(environment)
        except (OSError, subprocess.SubprocessError) as error:
            raise RuntimeError('Could not create a venv. On Linux, install the venv/ensurepip '
                               'component for your Python using the system package manager. '
                               + str(error)) from error

    env = os.environ.copy()
    env['PIP_CACHE_DIR'] = str(ROOT / '.cache' / 'pip')
    env['PIP_DISABLE_PIP_VERSION_CHECK'] = '1'
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    env['MPLCONFIGDIR'] = str(environment / '.matplotlib')
    run([python, '-m', 'pip', 'install', '--upgrade', 'pip'], env)
    run([python, '-m', 'pip', 'install', '--only-binary=:all:',
         '-r', ROOT / 'requirements.txt'], env)
    run([python, '-m', 'pip', 'check'], env)
    run([python, ROOT / 'setup_env.py', '--check-env'], env)
    print('\nReady. Render the sixteen PDFs with:', flush=True)
    print(subprocess.list2cmdline([str(python), str(ROOT / 'main.py'), '--output', 'generated']))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, subprocess.SubprocessError) as error:
        print('Setup failed: ' + str(error), file=sys.stderr)
        sys.exit(1)
