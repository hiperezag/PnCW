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
From the package root: python3 main.py --figure 09
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '09'

rows=csv_rows(HERE/'modes.csv',numeric=True)
SECTORS=['pps','ppa','pm','mp','mm']
plt.rcParams.update({'font.size':10,'axes.labelsize':11,'pdf.fonttype':42})
colors={'aluminum':'#176b8d','square_control':'#bd7035'}
fig,axes=plt.subplots(1,2,figsize=(10.4,4.1),layout='constrained')
for si,sector in enumerate(SECTORS):
    for system,offset in [('aluminum',-.16),('square_control',.16)]:
        group=[r for r in rows if r['sector']==sector and r['system']==system]
        for ax,key in zip(axes,('participation','channel_participation')):
            values=np.asarray([r[key] for r in group])
            percent=np.quantile(values,[.1,.25,.5,.75,.9]); x=si+offset
            ax.plot([x,x],percent[[0,4]],color=colors[system],lw=1)
            ax.plot([x,x],percent[[1,3]],color=colors[system],lw=5,alpha=.5)
            ax.scatter([x],[percent[2]],color=colors[system],s=25,zorder=3,
                       marker='o' if system=='aluminum' else 's',
                       label=('Aluminum' if system=='aluminum' else 'Integrable control') if si==0 else None)
for ax in axes:
    ax.set_xticks(range(5),SECTORS); ax.set_xlabel('Resolved symmetry sector')
    ax.grid(axis='y',alpha=.18)
axes[0].set_ylabel(r'Wall-trace participation $P_H$')
axes[1].set_ylabel(r'Effective tangential channels $N_{\mathrm{ch}}$')
axes[0].set_title('(a) Coherent phase-space spread')
axes[1].set_title('(b) Fourier channel mixing')
axes[0].legend(frameon=False,loc='best',fontsize=9)
fig.suptitle(r'Complete $(26,34]$ ensembles; median, quartiles and 10--90% ranges',fontsize=12)
finish(fig, FIGURE)
