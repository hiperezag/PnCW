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
From the package root: python3 main.py --figure S03
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S03'

data = read_json(HERE.parent/'shared'/'central_spectrum.json')
rows = {(r['window'], r['statistic'], r['model']): r for r in data['rows']}
SECTORS = ['pps','ppa','pm','mp','mm']
L_VALUES = np.array([1.,2.,4.,8.])
COLORS = {'poisson':'#2878b5','goe':'#d1495b','observed':'#111111'}
references = None
def reference_band(reference, count, model, statistic):
    return np.asarray(data['reference_quantiles'][f'{count}_{model}_{statistic}'])
fig, axes = plt.subplots(
    2,
    5,
    figsize=(11.5, 5.8),
    sharex=True,
    sharey=True,
    constrained_layout=True,
)
decisions = {}
for column, sector in enumerate(SECTORS):
    window = f"{sector}_26_34"
    count = rows[(window, "mean", "goe")]["levels"]
    decisions[sector] = {"levels": count}
    for row_index, statistic in enumerate(("affine", "quadratic")):
        ax = axes[row_index, column]
        archived = rows[(window, statistic, "goe")]
        observed = np.asarray(archived["observed_variance"])
        for model in ("poisson", "goe"):
            low, median, high = reference_band(references, count, model, statistic)
            ax.fill_between(
                L_VALUES,
                low,
                high,
                color=COLORS[model],
                alpha=0.17,
                linewidth=0,
            )
            ax.plot(
                L_VALUES,
                median,
                color=COLORS[model],
                linewidth=1.05,
                linestyle="--" if model == "poisson" else "-",
            )
        ax.plot(
            L_VALUES,
            observed,
            "o-",
            color=COLORS["observed"],
            linewidth=1.35,
            markersize=3.6,
            zorder=5,
        )
        ax.set_yscale("log")
        ax.set_ylim(0.32, 14.0)
        ax.set_xticks(L_VALUES)
        ax.set_yticks([0.4, 1.0, 2.0, 4.0, 8.0, 12.0])
        ax.tick_params(labelsize=12.5)
        ax.get_yaxis().set_major_formatter(matplotlib.ticker.FormatStrFormatter("%g"))
        ax.grid(color="#d9dde2", linewidth=0.45, which="major")
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        if row_index == 0:
            ax.set_title(rf"{sector}, $N={count}$", fontsize=14)
        if column == 0:
            label = "affine" if statistic == "affine" else "quadratic"
            ax.set_ylabel(rf"{label} $\widehat{{\Sigma}}^2(L)$", fontsize=14)
        if row_index == 1:
            ax.set_xlabel(r"interval length $L$", fontsize=13)
        decisions[sector][statistic] = {
            model: rows[(window, statistic, model)]["conclusion"]
            for model in ("poisson", "goe")
        }

axes[0, 0].plot([], [], "o-", color=COLORS["observed"], label="aluminum cell")
axes[0, 0].fill_between([], [], [], color=COLORS["goe"], alpha=0.17, label="finite GOE 95%")
axes[0, 0].fill_between([], [], [], color=COLORS["poisson"], alpha=0.17, label="finite Poisson 95%")
fig.legend(
    loc="outside lower center",
    ncols=3,
    frameon=False,
    fontsize=14,
)
fig.suptitle(
    r"Scale-resolved number variance, aluminum $f=0.03$, $26<\Omega\leq34$",
    fontsize=15,
)
finish(fig, FIGURE)
