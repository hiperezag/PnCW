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
From the package root: python3 main.py --figure S06
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S06'

rows=csv_rows(HERE/'modes.csv',numeric=True);summaries=csv_rows(HERE/'summary.csv',numeric=True)
SYSTEMS=['gas','aluminum','integrable_square'];sectors=['pps','ppa','pm','mp','mm']
groups={(system,sector):(np.array([i for i,r in enumerate(rows) if r['system']==system and r['sector']==sector]),)
        for system in SYSTEMS for sector in sectors}
colors={'gas':'#0072B2','aluminum':'#D55E00','integrable_square':'#009E73'}
markers={'gas':'o','aluminum':'s','integrable_square':'^'}
labels={'gas':'Fast gas','aluminum':'Aluminum','integrable_square':'Integrable square'}
plt.rcParams.update({'font.size':17,'axes.labelsize':17,'axes.titlesize':17,'xtick.labelsize':16,'ytick.labelsize':16,'legend.fontsize':16})
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6), layout="constrained")
rng = np.random.default_rng(14723)
for panel, metric in enumerate(("pressure_joint_direction_random_wave_rms", "connected_intensity_joint_direction_random_wave_rms")):
    ax = axes[panel]
    for system_index, system in enumerate(SYSTEMS):
        for sector_index, sector in enumerate(sectors):
            if (system, sector) not in groups:
                continue
            ids = groups[system, sector][0]
            values = np.array([rows[i][metric] for i in ids])
            center = sector_index + (system_index - 1) * 0.24
            ax.scatter(center + rng.uniform(-0.055, 0.055, len(values)), values,
                       s=9, marker=markers[system], alpha=0.14, c=colors[system], linewidths=0, rasterized=True)
            summary = next(row for row in summaries if row["system"] == system and row["sector"] == sector and row["metric"] == metric)
            m = summary["mean"]
            ax.errorbar(center, m, yerr=[[m-summary["bootstrap_mean_ci95_low"]],
                                        [summary["bootstrap_mean_ci95_high"]-m]],
                        fmt=markers[system], color=colors[system], capsize=3, ms=6,
                        label=labels[system] if sector_index == 0 else None)
    ax.set_xticks(range(len(sectors)), sectors)
    ax.set_ylabel("Joint-direction RMS distance")
    ax.set_title("(a) Pressure versus $J_0$" if panel == 0 else "(b) Connected intensity versus $J_0^2$")
    ax.grid(axis="y", color="#dddddd", lw=0.6)
fig.legend(*axes[0].get_legend_handles_labels(), loc="outside lower center", ncol=3, frameon=False)
fig.suptitle(r"Joint distances on $0\leq r/\lambda\leq2$; mode-bootstrap 95% intervals", fontsize=16)
finish(fig, FIGURE)
