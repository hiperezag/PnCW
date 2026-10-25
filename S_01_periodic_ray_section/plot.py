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
From the package root: python3 main.py --figure S01
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S01'

plt.rcParams.update({'font.size':10,'axes.titlesize':10,'axes.labelsize':10,
                     'xtick.labelsize':9,'ytick.labelsize':9,'pdf.fonttype':42})

data=read_json(HERE/'data.json');selected=csv_rows(HERE/'collisions.csv',numeric=True)
COLORS=dict(gas='#0072b2',aluminum='#d55e00')
fig, (a, b) = plt.subplots(1, 2, figsize=(8, 4.4), gridspec_kw={'width_ratios': (1, 1.7)})
fig.subplots_adjust(left=.08, right=.98, bottom=.30, top=.83, wspace=.30)
for index, center in enumerate(np.array(data['centers'])):
    a.add_patch(Circle(center, data['radius'], facecolor='#d5e0e6', edgecolor='#526775'))
    a.text(*center, str(index), ha='center', va='center', weight='bold')
a.axhline(.5, color='#666666', ls='--', lw=1)
a.axvline(.5, color='#888888', ls=':', lw=1)
a.text(.04, .53, 'wall mirror', fontsize=8, color='#555555')
a.text(.52, .17, 'axial seam', rotation=90, fontsize=8, color='#666666')
points = np.array(data['points'])
for index, point in enumerate(points):
    nxt = points[(index + 1) % len(points)]
    a.plot(*np.vstack((point, nxt)).T, color='#005e83', lw=1.7)
    a.annotate('', xy=.57*nxt+.43*point, xytext=.44*nxt+.56*point,
               arrowprops={'arrowstyle': '-|>', 'color': '#005e83', 'lw': 1.3})
a.scatter(*points.T, color='#111111', s=23, zorder=5)
a.set(xlim=(-.15, 1.15), ylim=(-.15, 1.15), xlabel=r'$x/L$', ylabel=r'$y/L$')
a.set_xticks((0, .5, 1)); a.set_yticks((0, .5, 1)); a.set_aspect('equal')
a.set_title('(a) Same guide, unfolded\n' + r'$0\to1\to2\to0$, $f=0.03$', loc='left', pad=12)
thresholds = data['thresholds']
b.axhspan(-thresholds['gas'], thresholds['gas'], color='#eef2f4', zorder=0)
for system, style in (('gas', '--'), ('aluminum', ':')):
    for sign in (-1, 1):
        b.axhline(sign*thresholds[system], color=COLORS[system], ls=style, lw=1.2)
for sign in (-1, 1):
    b.axhline(sign*data['certified'], color='#555555', ls='-.', lw=1)
periods = (3, 4, 6, 7)
colors = {3: '#0072b2', 4: '#e69f00', 6: '#009e73', 7: '#cc79a7'}
shapes = {3: 'o', 4: 's', 6: 'D', 7: '.'}
for j in range(1, 4):
    b.axvline(j, color='#d5d9dc', lw=.7, zorder=0)
for period in reversed(periods):
    group = [r for r in selected if r['period'] == period]
    b.scatter([r['sigma'] for r in group], [r['eta'] for r in group],
              marker=shapes[period], color=colors[period], s=18 if period == 7 else 28,
              alpha=.7, linewidths=0, zorder=11-period)
b.set(xlim=(0, 4), ylim=(-.88, .88), xlabel=r'$\sigma=j+s/(2\pi R)$', ylabel=r'$\eta=\sin\chi$')
b.set_xticks(range(5)); b.set_yticks((-.8, -.4, 0, .4, .8))
b.set_title('(b) Certified periodic points\n58 itineraries; 336 collision records', loc='left', pad=12)
handles = [Line2D([], [], marker=shapes[n], color=colors[n], ls='none', label=rf'$n={n}$') for n in periods]
handles += [Line2D([], [], color=COLORS['gas'], ls='--', label=r'gas: $\pm\eta_c$'),
            Line2D([], [], color=COLORS['aluminum'], ls=':', label=r'Al: $\pm\eta_c$'),
            Line2D([], [], color='#555555', ls='-.', label=r'certified $\pm\eta_*$')]
fig.legend(handles=handles, loc='lower center', bbox_to_anchor=(.5, .03), ncol=4,
           fontsize=9, frameon=False, columnspacing=1.4)
finish(fig, FIGURE)
