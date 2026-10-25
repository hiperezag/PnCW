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
From the package root: python3 main.py --figure S08
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S08'

rows=csv_rows(HERE/'modes.csv');summary=read_json(HERE/'data.json')
SECTORS=('pps','ppa','pm','mp','mm');COLORS=('#1f526f','#ac5628','#337b62','#714c88','#425c97')
plt.rcParams.update({"font.family":"DejaVu Sans", "font.size":9,
    "axes.labelsize":9, "axes.titlesize":9, "xtick.labelsize":8,
    "ytick.labelsize":8, "legend.fontsize":7.5, "axes.linewidth":.65,
    "pdf.fonttype":42, "ps.fonttype":42, "mathtext.fontset":"dejavusans"})
fig, axes = plt.subplots(2, 3, figsize=(8.8, 5.15), sharey=True,
                         gridspec_kw={"hspace":.4, "wspace":.21})
records = []
for index, (sector, color, ax) in enumerate(zip(SECTORS, COLORS, axes.flat)):
    selected = [row for row in rows if row["sector"] == sector]
    omega = np.array([float(row["omega"]) for row in selected])
    fraction = np.array([float(row["solid_energy_fraction"]) for row in selected])
    expected = next(r for r in summary["sectors"] if r["sector"] == sector)
    if len(selected) != expected["count"] or not np.all((omega>26)&(omega<=34)):
        raise RuntimeError("Frequency/count mismatch")
    ax.scatter(omega, fraction, s=7, color=color, alpha=.72, edgecolors="none")
    ax.axhline(fraction.mean(), color="#303030", lw=.8, ls="--", zorder=0)
    ax.set_title(f"({chr(97+index)}) {sector}, N = {len(selected)}", loc="left")
    ax.set_xlim(25.9,34.1)
    ax.set_xticks([26,28,30,32,34])
    ax.set_xlabel(r"Reduced frequency $\Omega$")
    records.append(dict(sector=sector, count=len(selected),
                        fraction_mean=float(fraction.mean()),
                        fraction_quantiles=np.quantile(fraction,[.05,.5,.95]).tolist()))
ax = axes.flat[-1]
for i, (record, color) in enumerate(zip(records, COLORS)):
    q5, median, q95 = record["fraction_quantiles"]
    ax.plot([i,i],[q5,q95],color=color,lw=2)
    ax.plot([i-.10,i+.10],[q5,q5],color=color,lw=1)
    ax.plot([i-.10,i+.10],[q95,q95],color=color,lw=1)
    ax.plot(i,median,"o",ms=4.2,color=color)
    ax.plot(i,record["fraction_mean"],"D",ms=3.7,color="#202020",zorder=5)
ax.set_title("(f) Complete-ensemble summaries",loc="left")
ax.set_xticks(range(5),SECTORS)
ax.set_xlim(-.5,4.5)
ax.set_xlabel("Symmetry sector")
ax.legend(handles=[Line2D([0],[0],marker="D",color="none",markerfacecolor="#202020",
                           markeredgecolor="#202020",markersize=3.8,label="Mean"),
                   Line2D([0],[0],marker="o",color="#666666",markersize=4,
                           label="Median, 5-95% quantiles")],
          loc="lower center",bbox_to_anchor=(.46,.015),frameon=False,
          handlelength=1.6,handletextpad=.45,labelspacing=.35)
for ax in axes.flat:
    ax.set_yscale("log")
    ax.set_ylim(5e-10,2e-5)
    ax.grid(axis="y",which="major",color="#dddddd",lw=.55,zorder=-1)
    ax.spines[["right","top"]].set_visible(False)
for ax in axes[:,0]:
    ax.set_ylabel(r"Solid energy fraction $E_s/(E_a+E_s)$")
fig.subplots_adjust(left=.09,right=.99,bottom=.10,top=.95)
finish(fig, FIGURE)
