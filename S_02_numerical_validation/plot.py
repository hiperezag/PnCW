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

"""Render supplied numerical data only. No solver or statistical calibration.

From this directory: python3 plot.py --output ../generated
From the package root: python3 main.py --figure S02
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S02'

plt.rcParams.update({'font.size':10,'axes.titlesize':10,'axes.labelsize':10,
                     'xtick.labelsize':9,'ytick.labelsize':9,'pdf.fonttype':42})

order=csv_rows(HERE/'order.csv'); mps=csv_rows(HERE/'mps.csv'); acf=csv_rows(HERE/'acf.csv')
SYSTEMS=('gas','aluminum','integrable_square')
COLORS=dict(gas='#0072b2',aluminum='#d55e00',integrable_square='#007b5b')
MARKERS=dict(gas='o',aluminum='s',integrable_square='D')
LABELS=dict(gas='Gas',aluminum='Aluminum',integrable_square='Integrable square')
fig, axes = plt.subplots(2, 2, figsize=(8, 7.2))
fig.subplots_adjust(left=.12, right=.98, bottom=.14, top=.94, hspace=.43, wspace=.32)
a, b, c, d = axes.flat
for system in SYSTEMS[:2]:
    rows = [row for row in order if row['system'] == system]
    a.semilogy([int(r['order']) for r in rows], [float(r['maximum_drift_to_local_gap']) for r in rows],
               color=COLORS[system], marker=MARKERS[system], markersize=6, lw=1.6)
    rows = [row for row in mps if row['system'] == system]
    b.semilogy([float(r['sem_omega']) for r in rows], [float(r['frequency_error_to_local_gap']) for r in rows],
               ls='none', marker=MARKERS[system], color=COLORS[system], markersize=6)
for ax in (a, b):
    ax.axhline(1e-3, ls='--', color='#a33d3d', lw=1.2)
    ax.grid(axis='y', alpha=.18)
a.set(title='(a) Order refinement', xlabel=r'Polynomial order $n_p$',
      ylabel=r'Maximum $|\Delta\Omega|/\delta_\Omega$', xlim=(19.7, 24.3), ylim=(1e-5, .4))
a.set_xticks((20, 22, 24))
a.text(.05, .95, 'Counts: 48 gas / 47 Al', transform=a.transAxes, va='top', fontsize=9)
a.text(.97, .06, r'$n_p=24$ accepted', transform=a.transAxes, ha='right', fontsize=9)
b.set(title='(b) Independent MPS', xlabel=r'SEM frequency $\Omega$',
      ylabel=r'$|\Omega_{\rm MPS}-\Omega_{\rm SEM}|/\delta_\Omega$', xlim=(59.97, 61.03), ylim=(5e-9, 3e-3))
b.text(.05, .62, '5 fixed modes / material', transform=b.transAxes, fontsize=9)
for ax, observable, letter, label in ((c, 'pressure', 'c', 'Pressure ACF'),
                                       (d, 'connected_intensity', 'd', 'Connected-intensity ACF')):
    point_count = 0
    for system in reversed(SYSTEMS):
        rows = [r for r in acf if r['system'] == system]
        x = [float(r[observable + '_rms_fraction_of_gate']) for r in rows]
        y = [float(r[observable + '_pointwise_fraction_of_gate']) for r in rows]
        require(all(0 < v < 1 for v in x+y), 'ACF point outside the gates')
        collection = ax.scatter(x, y, marker=MARKERS[system], s=34,
                                facecolors='none' if ax is c else COLORS[system],
                                edgecolors=COLORS[system] if ax is c else '#202020',
                                linewidths=1.1 if ax is c else .45, alpha=1)
        point_count += len(collection.get_offsets())
    require(point_count == 144, 'A plotted mode is missing')
    # Set display limits without moving any validation coordinate.
    # Keep every coordinate unchanged and adapt only the displayed extent.
    xx=[float(r[observable+'_rms_fraction_of_gate']) for r in acf]
    yy=[float(r[observable+'_pointwise_fraction_of_gate']) for r in acf]
    ax.set(xscale='log', yscale='log', xlim=(min(.04,min(xx)/1.15),max(.23,max(xx)*1.15)),
           ylim=(min(.035,min(yy)/1.15),max(.20,max(yy)*1.15)),
           title=f'({letter}) {label}', xlabel='RMS change / 0.01', ylabel='Maximum change / 0.03')
    ax.text(.04, .92, '144 modes; grid 2048 / 1024', transform=ax.transAxes, fontsize=8.7)
    ax.text(.97, .04, 'Acceptance: both axes < 1', transform=ax.transAxes,
            fontsize=8.2, ha='right', color='#853535')
    ax.grid(alpha=.18)
fig.legend(handles=[Line2D([], [], ls='none', marker=MARKERS[s], color=COLORS[s],
                           markeredgecolor='#202020', markersize=7, label=LABELS[s]) for s in SYSTEMS],
           loc='lower center', bbox_to_anchor=(.54, .035), ncol=3, frameon=False, fontsize=10)
finish(fig, FIGURE)
