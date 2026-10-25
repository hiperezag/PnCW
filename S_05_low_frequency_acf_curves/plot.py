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
From the package root: python3 main.py --figure S05
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = 'S05'

data=read_json(HERE/'data.json');archive=np.load(HERE/'data.npz');s=archive['s']
plt.rcParams.update({'font.size':17,'axes.labelsize':17,'axes.titlesize':17,'xtick.labelsize':16,'ytick.labelsize':16,'legend.fontsize':16})
colors={'gas':'#0072B2','aluminum':'#D55E00','integrable_square':'#009E73'}
styles={'gas':'-','aluminum':'--','integrable_square':'-.'}
labels={'gas':'Fast gas','aluminum':'Aluminum','integrable_square':'Integrable square'}
fig,axes=plt.subplots(2,5,figsize=(13.3,6),sharex=True,sharey='row',layout='constrained',squeeze=False)
for col,sector in enumerate(data['sectors']):
    for obs in range(2):
        ax=axes[obs,col]
        reference=archive['pressure_reference' if obs==0 else 'intensity_reference']
        ax.plot(s,reference,color='black',ls=':',lw=1.8,label='Gaussian random wave' if col==0 and obs==0 else None)
        for system in data['systems']:
            prefix=system+'_'+sector
            ax.plot(s,archive[prefix+'_mean'][obs],color=colors[system],ls=styles[system],lw=2,
                    label=labels[system] if col==0 and obs==0 else None)
            ax.fill_between(s,archive[prefix+'_low'][obs],archive[prefix+'_high'][obs],color=colors[system],alpha=.16,lw=0)
        ax.axhline(0,color='#cccccc',lw=.7);ax.grid(color='#e8e8e8',lw=.5);ax.set_xlim(s[0],s[-1])
        if obs==0:ax.set_title(sector)
        else:ax.set_xlabel(r'$r/\lambda_{\rm air}$')
axes[0,0].set_ylabel(r'Pressure $\overline{C}_p$');axes[1,0].set_ylabel(r'Connected intensity $\overline{C}_I$')
axes[0,0].set_ylim(-.45,1.04);axes[1,0].set_ylim(-.3,1.04)
fig.legend(*axes[0,0].get_legend_handles_labels(),loc='outside upper center',ncol=4,frameon=False)
finish(fig, FIGURE)
