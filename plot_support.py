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

"""Shared plotting utilities. No physical solver, inference, or external project access."""
from pathlib import Path
import argparse
import csv
import json
import os

# Sequential plotting, including on an 8-GB iMac. No multiprocessing/MPI.
for _name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[_name]='1'
os.environ.setdefault('MPLCONFIGDIR', str(Path(__file__).resolve().parent/'generated/.matplotlib'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
import numpy as np

# Each figure starts from explicit Matplotlib defaults, independent of user
# configuration. Individual plots retain their publication-specific styles.
plt.rcdefaults()
plt.rcParams.update({'font.family':'DejaVu Sans','mathtext.fontset':'dejavusans'})


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def csv_rows(path,numeric=False):
    with Path(path).open(newline='',encoding='utf-8') as stream:
        rows=list(csv.DictReader(stream))
    if numeric:
        for row in rows:
            for key,value in row.items():
                try:row[key]=float(value)
                except (TypeError,ValueError):pass
    return rows


def require(condition,reason):
    if not condition:raise ValueError(reason)


def finish(fig,number):
    parser=argparse.ArgumentParser(description='Plot saved numerical data only: Figure '+number)
    parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parent/'generated')
    parser.add_argument('--png',action='store_true',help='Also write a 240-dpi preview')
    args=parser.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    target=args.output/('Figure_'+number+'.pdf')
    options={}
    if number in ('03','08','S03'):options['bbox_inches']='tight'
    options['dpi']={'06':240,'07':240,'S06':220,'S07':300}.get(number,100)
    fig.savefig(target,facecolor='white',metadata={'CreationDate':None,'ModDate':None,'Author':''},**options)
    if args.png:
        fig.savefig(target.with_suffix('.png'),dpi=240,facecolor='white',
                    bbox_inches=options.get('bbox_inches'))
    plt.close(fig)
    print(target.resolve(),flush=True)
