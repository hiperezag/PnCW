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
From the package root: python3 main.py --figure 04
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '04'

data = read_json(HERE.parent/'shared'/'central_spectrum.json')
rows = {(r['window'], r['statistic'], r['model']): r for r in data['rows']}
SECTORS = ['pps','ppa','pm','mp','mm']
COLORS = {'poisson':'#2878b5', 'goe':'#d1495b'}
def interval(reference, count, model, statistic, component=0):
    q = np.asarray(data['reference_quantiles'][f'{count}_{model}_{statistic}'])
    return q[:,component] if q.ndim == 2 else q
def draw_interval(ax, x, q, color, offset):
    ax.vlines(x+offset, q[0], q[2], color=color, linewidth=4., alpha=.72)
    ax.plot(x+offset, q[1], '_', color=color, markersize=9, markeredgewidth=1.6)
reference = None
x = np.arange(len(SECTORS))
fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.25), constrained_layout=True)

for i, sector in enumerate(SECTORS):
    name = f"{sector}_26_34"
    mean_row = rows[(name, "mean", "goe")]
    count = mean_row["levels"]
    for model, offset in [("poisson", -0.11), ("goe", 0.11)]:
        draw_interval(axes[0], i, interval(reference, count, model, "mean"),
                      COLORS[model], offset)
    axes[0].plot(i, mean_row["mean_ratio"], "ko", markersize=4.2, zorder=4)

    affine = rows[(name, "affine", "goe")]
    for model, offset in [("poisson", -0.11), ("goe", 0.11)]:
        draw_interval(axes[1], i,
                      interval(reference, count, model, "affine", component=3),
                      COLORS[model], offset)
    axes[1].plot(i, affine["observed_variance"][3], "ko", markersize=4.2, zorder=4)

for ax in axes:
    ax.set_xticks(x, SECTORS)
    ax.grid(axis="y", color="#d9dde2", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
axes[0].set_ylim(0.31, 0.62)
axes[0].set_ylabel(r"mean adjacent-gap ratio $\langle r\rangle$")
axes[0].set_title("(a) Short range", loc="left", fontsize=10)
axes[1].set_ylim(0, 12.5)
axes[1].set_ylabel(r"affine number variance $\widehat\Sigma^2(8)$")
axes[1].set_title("(b) Longer range", loc="left", fontsize=10)

axes[0].plot([], [], "ko", markersize=4.2, label="aluminum cell")
axes[0].plot([], [], color=COLORS["poisson"], linewidth=4, alpha=.72,
             label="finite Poisson 95%")
axes[0].plot([], [], color=COLORS["goe"], linewidth=4, alpha=.72,
             label="finite GOE 95%")
fig.legend(*axes[0].get_legend_handles_labels(), frameon=False,
           fontsize=9.5, loc="outside lower center", ncol=3)
fig.suptitle(r"Aluminum, $f=0.03$, common window $26<\Omega\leq34$",
             fontsize=10.5)
finish(fig, FIGURE)
