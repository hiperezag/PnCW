PnCW - NUMERICAL FIGURE REPRODUCTION
===================================

This self-contained folder renders sixteen numerical-result figures:
Figures 03-10 and S01-S08. Every F_* or S_* directory contains one plot.py
and any figure-specific data. Metadata used by more than one figure are
stored once in shared/. There is one main runner and one shared plotting
helper. No physical solvers are included. 

PYTHON COMPATIBILITY AND DEPENDENCIES
The installation accepts an existing Python 3.9-3.14 interpreter. It does
not install Python or require the version used to prepare the figures.
These are the supported interpreter targets; older releases, later
releases and all possible platform/architecture combinations are not
implicitly certified. Prefer a Python release still maintained upstream.

requirements.txt selects bounded dependencies for the interpreter:
- Python 3.9-3.12: NumPy >=1.26.4,<2.0 and Matplotlib >=3.8.4,<=3.10.7.
- Python 3.13-3.14: NumPy >=2.3.4,<2.4 and Matplotlib >=3.10.7,<3.11.
pip also enforces each library's Python and operating-system requirements.
The NumPy 1.x branch avoids incompatible earlier Matplotlib binary builds;
the newer branch provides wheels for the newer interpreters. Installation
uses binary wheels, so no Fortran/C compiler is required for plotting.
Wheel availability still depends on the operating system and architecture.
Dependency compatibility references:
https://numpy.org/devdocs/release/1.26.4-notes.html
https://numpy.org/doc/stable/release/2.3.4-notes.html
https://matplotlib.org/3.10.7/install/dependencies.html

INSTALLATION AND EXECUTION
Extract or clone the complete package and open a terminal in its root.
Use your installed interpreter to run setup_env.py. The script creates
a local .venv and installs the active requirements there. It reuses a
working environment with the same Python minor version, without clearing
it. A different interpreter requires a different environment directory
(--venv) or a freshly extracted package. Do not copy .venv across machines.

macOS (Intel or Apple Silicon), Terminal:
python3 --version
python3 setup_env.py
.venv/bin/python main.py --output generated

Linux, terminal:
python3 --version
python3 setup_env.py
.venv/bin/python main.py --output generated

Windows, PowerShell or Command Prompt:
py --version
py setup_env.py
.venv\Scripts\python.exe main.py --output generated

In PowerShell the explicit relative path .\.venv\Scripts\python.exe also
works. If the Python launcher is unavailable but python is in PATH, use
python setup_env.py. There is no need to activate the environment or change
PowerShell execution policy. Replace python3/py with the full path to an
installed compatible interpreter when necessary; quote paths with spaces.
In PowerShell prefix a quoted executable path with the call operator &.

The previous macOS entry point remains available as a wrapper:
sh setup_macos.sh
It selects a compatible installed interpreter from PATH, or the executable
specified in PNCW_PYTHON, and calls the same setup_env.py installer.
For example: PNCW_PYTHON=/absolute/path/to/python sh setup_macos.sh

If Python is absent or outside the supported range, install a compatible
release from https://www.python.org/downloads/ or your system's package
manager. Some Linux distributions package venv/ensurepip separately; install
the venv component matching your interpreter (for example python3-venv on
Debian/Ubuntu). Installation errors about missing binary wheels indicate
an unsupported OS/architecture or interpreter combination, rather than a
need to compile the acoustic solvers.

Dependency installation requires Internet; subsequent rendering is offline.
The plotting package does not require LaTeX or another project.

To use an already prepared environment instead of the installer:
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: -r requirements.txt
.venv/bin/python setup_env.py --check-env
On Windows use py for the first command and .venv\Scripts\python.exe for
the remaining commands. The same requirements apply to conda environments.

RENDER ALL SIXTEEN PDFS (AFTER INSTALLATION)
macOS/Linux: .venv/bin/python main.py --output generated
Windows:    .venv\Scripts\python.exe main.py --output generated

Outputs are written to generated/. The data files are not modified.
Existing output files with the same names are regenerated. PLOT_RUN.json
records the selected figures, output filenames, interpreter, library
versions and platform. Rendering is sequential
and numerical-library thread counts are limited to one.

OPTIONS
.venv/bin/python main.py --list
.venv/bin/python main.py --output my_figures
.venv/bin/python main.py --figure 06 --figure 07 --output my_atlas
.venv/bin/python F_06_pressure_modes/plot.py --output my_single_figure

Use .venv\Scripts\python.exe instead of .venv/bin/python on Windows.
python3 setup_env.py --check checks the selected interpreter without
installing anything. .venv/bin/python setup_env.py --check-env checks the
installed dependency versions and binary imports, without rendering.

Individual plot.py scripts also run from their own directories. They
use only files inside this package. The PDF settings retain each figure's
own export requirements.

COMPATIBILITY VERIFICATION
The interpreter/dependency range above is a compatibility target, not a
claim that every version combination has been executed on every platform.
The local verification record is in COMPATIBILITY.txt. Rendering with
different library versions may change font metrics, layout, PDF encoding
or raster sampling slightly. Input arrays, frequencies, normalization and
statistical decisions remain those distributed with this package.
PLOT_RUN.json identifies the environment of each successful rendering run.
Upload the distributed source/data/documentation files to the repository;
keep .venv/, .validation/, .cache/, generated/ and __pycache__/ local.
.gitignore excludes these directories when using git; when uploading in
the browser, omit them manually. User-selected output directories should
also be omitted unless deliberately publishing generated figures.

CONTENTS AND DATA
CSV files contain numerical tables. NPZ files contain losslessly
compressed numerical arrays, loaded without executable objects.
JSON files supply panel identities, parameters and numerical summaries.
All three formats are required when referenced by a plotting script.
FIGURE_INDEX.json maps the sixteen figure IDs to directory names and
their plotted content; main.py --list displays the same mapping.
main.py checks the dependency requirements and reads the figure index
and selected plotting inputs.
Editing or rebuilding the model cannot block the sixteen figures.

The plots retain the supplied eigenfrequencies, pressure arrays, wall-map
densities, correlation curves, uncertainty intervals, per-mode observables
and calibrated spectral summaries. Rendering may evaluate means or
quantiles of those saved values, but does not solve IEM/SEM/MPS problems,
compute new modal ensembles, resample bootstrap intervals or simulate
GOE/Poisson reference ensembles.

The pressure and wall-map atlases have the same row order: analytic
square, empty-cell IEM, gas IEM and elastic-aluminum IEM. Empty pressure
panels display the complete square without a circular mask. A shared
exterior observation region fixes their normalization, not an obstacle.
The pressure scale saturates at 6; the wall-map scale is 4*pi*H with
saturation at 8. Physical roots are rounded only in displayed labels.

NUMERICAL SCOPE
These scripts reproduce figures from the included numerical results.
Rendering the saved data is not a new physical convergence test or
recalibration of the statistical decisions. main.py generates
only the sixteen result figures, not geometry figures, model diagrams,
manuscripts or supplementary documents.

LICENSING
The article authors have authorized the following licenses:

- Original numerical data and metadata (.csv, .npz and .json), original
  distributed figure images, and standalone package documentation:
  Creative Commons Attribution 4.0 International (CC-BY-4.0).
- The original standalone "Numerical model and data companion for acoustic
  wave chaos in a periodic phononic-crystal waveguide", including its text,
  original diagrams, and PDF, whether distributed within or
  alongside this package: CC-BY-4.0.
- Original Python scripts (main.py, setup_env.py, plot_support.py and the
  sixteen F_*/plot.py and S_*/plot.py scripts), and setup_macos.sh: Apache-2.0.
  Embedded software documentation follows Apache-2.0; standalone documents
  follow CC-BY-4.0. Script headers identify the software license.

LICENSE contains the component-specific grants and the complete legal
texts of both licenses. These licenses apply to different components;
they are not a choice of either license for every file.

CC BY 4.0 permits sharing and adaptation, including commercial reuse,
with appropriate attribution, a license link, and identification of changes.
Apache 2.0 permits software use, modification and redistribution under its
notice and redistribution conditions. Retain applicable copyright and
license notices and mark modified files as required by the license.

Author names, author order and affiliations are provided in the associated
article identified in LICENSE and are not repeated here. For attribution,
credit "PnCW project authors and contributors" and identify the package or
model companion and the specific version used. Citation of the associated
article, when available, is requested for scholarly credit and is not an
additional license restriction.

The repository licenses do not license the PRE article or its scientific
supplement. Third-party libraries, fonts, reference publications and any
other third-party material retain their own licenses and notices.
Only original material for which the licensors hold the necessary rights
is covered. No GitHub repository or DOI is assigned by these notices.
