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
From the package root: python3 main.py --figure 03
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '03'

data = read_json(HERE/'data.json')
FILLS = data['fills']
by_key = {(r['material'], r['fill']): r for r in data['certificates']}
incidence = np.array(data['incidence'])
instability = np.array(data['instability'])
COLORS = {'observed':'#111111', 'gas':'#0072b2', 'aluminum':'#d55e00', 'instability':'#009e73'}
fig = plt.figure(figsize=(7.15, 4.95), constrained_layout=True)
grid = fig.add_gridspec(2, 2, height_ratios=[1.05, 0.82])
ax_angle = fig.add_subplot(grid[0, 0])
ax_instability = fig.add_subplot(grid[0, 1])
ax_graph = fig.add_subplot(grid[1, :])

fill_percent = 100 * np.asarray(FILLS)
ax_angle.plot(
    fill_percent,
    incidence,
    "o-",
    color=COLORS["observed"],
    linewidth=1.5,
    markersize=4.5,
    label=r"certified $\theta_{\mathrm{inc,min}}$",
)
critical = {}
for material, label in (("gas", "gas inclusion"), ("aluminum", "elastic Al")):
    theta = by_key[(material, FILLS[0])]["critical_angle_deg"]
    critical[material] = theta
    ax_angle.axhline(
        theta,
        color=COLORS[material],
        linestyle="--",
        linewidth=1.4,
        label=rf"$\theta_c$, {label}",
    )
    ax_angle.fill_between(
        fill_percent,
        theta,
        incidence,
        where=incidence >= theta,
        color=COLORS[material],
        alpha=0.08,
    )
ax_angle.set_xticks(fill_percent)
ax_angle.set_xlabel("filling fraction (%)")
ax_angle.set_ylabel("angle (deg)")
ax_angle.set_ylim(4.0, 23.0)
ax_angle.set_title("(a) Total-reflection certificate", loc="left", fontsize=10)
ax_angle.legend(frameon=True, facecolor="white", framealpha=0.95,
                edgecolor="#dddddd", fontsize=8.5, loc="lower left")

ax_instability.errorbar(
    fill_percent,
    instability[:, 1],
    yerr=np.asarray([instability[:, 1] - instability[:, 0], instability[:, 2] - instability[:, 1]]),
    fmt="o-",
    color=COLORS["instability"],
    linewidth=1.5,
    markersize=4.5,
    capsize=4,
    label="median; bars show min-max",
)
ax_instability.set_xticks(fill_percent)
ax_instability.set_xlabel("filling fraction (%)")
ax_instability.set_ylabel(r"$\log|\mu_u|/n$ per collision")
ax_instability.set_ylim(2.35, 4.08)
ax_instability.set_title("(b) Sampled periodic-ray instability", loc="left", fontsize=10)
ax_instability.legend(frameon=False, fontsize=8.5, loc="upper right")
ax_instability.text(
    0.03, 0.06, "58 itineraries/f; periods 3-7\nfinite sample, not a uniform bound",
    transform=ax_instability.transAxes, ha="left", va="bottom", fontsize=8.5,
    color="#4b5563",
)

states = [(i, j) for i in range(4) for j in range(4) if i != j]
adjacency = np.array(data['adjacency'])
ax_graph.imshow(
    adjacency,
    cmap=ListedColormap(["#f2f4f7", "#5b5f97"]),
    vmin=0,
    vmax=1,
    interpolation="nearest",
    aspect="auto",
)
labels = [rf"${i}{j}$" for i, j in states]
ticks = np.arange(len(states))
ax_graph.set_xticks(ticks, labels, fontsize=8.5)
ax_graph.set_yticks(ticks, labels, fontsize=8.5)
ax_graph.set_xlabel("next ordered disk pair")
ax_graph.set_ylabel("current ordered disk pair")
ax_graph.set_title(
    r"(c) Symbolic transition matrix: 12 states, 2 successors/state, "
    r"$\rho(A)=2$, $h_{\mathrm{top}}=\ln 2$ per collision",
    loc="left",
    fontsize=10,
)

for ax in (ax_angle, ax_instability):
    ax.grid(axis="y", color="#d9dde2", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
finish(fig, FIGURE)
