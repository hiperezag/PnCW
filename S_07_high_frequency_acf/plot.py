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
From the package root: python3 main.py --figure S07
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S07'

archive=np.load(HERE/'data.npz');s=archive['s']
rows=csv_rows(HERE/'modes.csv',numeric=True);summary=csv_rows(HERE/'summary.csv',numeric=True)
SYSTEMS=['gas','aluminum','integrable_square']
COLORS={'gas':'#0072B2','aluminum':'#D55E00','integrable_square':'#009E73'}
LABELS={'gas':'Fast gas','aluminum':'Elastic aluminum','integrable_square':'Integrable square'}
LINE_STYLES={'gas':'-','aluminum':'--','integrable_square':'-.'}
MARKERS={'gas':'o','aluminum':'s','integrable_square':'^'}
plt.rcParams.update({'font.size':14,'axes.titlesize':13,'axes.labelsize':14,'xtick.labelsize':12,'ytick.labelsize':12})
bands={system:{key:archive[system+'_ppa_'+key] for key in ('mean','low','high')} for system in SYSTEMS}
fig, axes = plt.subplots(2, 2, figsize=(9.1, 7.0), layout='constrained')
for col, (observable, metric, power) in enumerate([
        ('pressure', 'pressure_joint_direction_random_wave_rms', 1),
        ('connected_intensity', 'connected_intensity_joint_direction_random_wave_rms', 2)]):
    ax = axes[0,col]
    for system in SYSTEMS:
        part = bands[system]
        ax.plot(s, part['mean'][col], color=COLORS[system], ls=LINE_STYLES[system], lw=1.8,
                label=LABELS[system])
        ax.fill_between(s, part['low'][col], part['high'][col], color=COLORS[system], alpha=.17)
    ax.plot(s,archive['pressure_reference' if col==0 else 'intensity_reference'],'k:',lw=1.3,label='Random-wave reference')
    ax.set_xlabel(r'$r/\lambda_{\rm air}$')
    ax.set_ylabel(r'$\overline{C}_p$' if col==0 else r'$\overline{C}_I$')
    ax.set_title('(a) Pressure correlation' if col==0 else '(b) Connected squared pressure')
    ax.grid(alpha=.2)
    ax=axes[1,col]
    rng=np.random.default_rng(605032)
    for i,system in enumerate(SYSTEMS):
        values=np.array([float(r[metric]) for r in rows if r['system']==system and r['sector']=='ppa'])
        records=[r for r in summary if r['system']==system and r['sector']=='ppa' and r['metric']==metric]
        if len(records) != 1 or int(records[0]['modes']) != len(values):
            raise RuntimeError('Joint-distance summary does not match the mode ensemble')
        rec=records[0]
        mean=float(rec['mean'])
        if not np.isclose(mean, np.mean(values), rtol=0, atol=1e-12):
            raise RuntimeError('Joint-distance CSV mean is inconsistent')
        ax.scatter(i+rng.uniform(-.12,.12,len(values)),values,s=15,marker=MARKERS[system],alpha=.35,color=COLORS[system])
        ax.errorbar(i,mean,yerr=[[mean-float(rec['bootstrap_mean_ci95_low'])],
                               [float(rec['bootstrap_mean_ci95_high'])-mean]],fmt=MARKERS[system],ms=6,color='black',capsize=4)
    ax.set_xticks(range(3),['Gas','Aluminum','Square'])
    ax.set_ylabel(r'$D_p$' if col==0 else r'$D_I$')
    ax.set_title('(c) Per-mode pressure distance' if col==0 else '(d) Squared-pressure distance')
    ax.grid(axis='y',alpha=.2)
fig.legend(*axes[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=2,frameon=False,fontsize=13)
finish(fig, FIGURE)
