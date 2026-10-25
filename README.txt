PnCW - NUMERICAL FIGURE REPRODUCTION
===================================

This self-contained folder renders sixteen numerical-result figures:
Figures 03-10 and S01-S08. Every F_* or S_* directory contains one plot.py
and any figure-specific data. Metadata used by more than one figure are
stored once in shared/. There is one main runner and one shared plotting
helper. No physical solvers are included. 

INSTALLATION (macOS: Intel or Apple Silicon)
From a terminal inside this folder:

sh setup_macos.sh

The script finds Python 3.12, recreates .venv for this Mac and installs
the pinned NumPy and Matplotlib versions. Do not copy .venv between Macs.
If Python 3.12 is missing, install it once with Homebrew and rerun:

brew install python@3.12
sh setup_macos.sh

Without Homebrew, install Python 3.12 from https://www.python.org/downloads/
and rerun the script. For an interpreter outside PATH, use:

PNCW_PYTHON=/absolute/path/to/python3.12 sh setup_macos.sh

Dependency installation requires Internet once; rendering is offline.
The plotting package does not require LaTeX or another project.
On Windows, install Python 3.12 and use:

py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt

RENDER ALL SIXTEEN PDFS
.venv/bin/python main.py

Outputs are written to generated/. The data files are not modified.
Existing output files with the same names are regenerated. PLOT_RUN.json
records the selected figures and output filenames. Rendering is sequential
and numerical-library thread counts are limited to one.

OPTIONS
.venv/bin/python main.py --list
.venv/bin/python main.py --output my_figures
.venv/bin/python main.py --figure 06 --figure 07 --output my_atlas
.venv/bin/python F_06_pressure_modes/plot.py --output my_single_figure

Individual plot.py scripts also run from their own directories. They
use only files inside this package. The PDF settings retain each figure's own export requirements.

CONTENTS AND DATA
CSV files contain numerical tables. NPZ files contain losslessly
compressed numerical arrays, loaded without executable objects.
JSON files supply panel identities, parameters and numerical summaries.
All three formats are required when referenced by a plotting script.
FIGURE_INDEX.json maps the sixteen figure IDs to directory names and
their plotted content; main.py --list displays the same mapping.
main.py reads the figure index and the selected plotting inputs only.
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
- Original Python scripts (main.py, plot_support.py and the sixteen
  F_*/plot.py and S_*/plot.py scripts), and setup_macos.sh: Apache-2.0.
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
