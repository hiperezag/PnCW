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
From the package root: python3 main.py --figure 08
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '08'

plt.rcParams.update({'font.family':'DejaVu Serif','font.size':10,
                     'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})

modes=csv_rows(HERE/'modes.csv',numeric=True)
summary=csv_rows(HERE/'summary.csv',numeric=True)
SECTORS=['pps','ppa','pm','mp','mm']
METRICS=('pressure_joint_direction_random_wave_rms','connected_intensity_joint_direction_random_wave_rms')
COUNTS={'aluminum':(188,184,369,366,362),'integrable_square':(195,189,378,376,370)}
assert len(modes)==2977
fig,axes=plt.subplots(1,2,figsize=(11.2,4.6),sharey=True)
rng=np.random.default_rng(20261002)
verified=[]
for ax,metric,label,title in zip(axes,METRICS,('$D_p$','$D_I$'),
                               ('(a) Pressure','(b) Connected squared pressure')):
    for system,color,marker,offset,display in [
            ('aluminum','#2464a3','o',-.18,'Aluminum'),
            ('integrable_square','#b85c13','s',.18,'Integrable square')]:
        for sidx,sector in enumerate(SECTORS):
            values=np.array([float(r[metric]) for r in modes
                             if r['system']==system and r['sector']==sector])
            record=next(r for r in summary if r['system']==system
                        and r['sector']==sector and r['metric']==metric)
            mean,lo,hi=[float(record[key]) for key in
                        ('mean','bootstrap_mean_ci95_low','bootstrap_mean_ci95_high')]
            assert len(values)==int(record['modes'])==COUNTS[system][sidx]
            assert abs(values.mean()-mean) < 2e-15 and lo<mean<hi
            xpos=sidx+offset
            ax.scatter(xpos+rng.uniform(-.12,.12,len(values)),values,s=7,
                       alpha=.14,color=color,linewidths=0,zorder=1)
            ax.plot(xpos,mean,marker=marker,color=color,ms=4.5,zorder=6,
                    label=display if sidx==0 else None)
            ax.errorbar(xpos,mean,yerr=np.array([[mean-lo],[hi-mean]]),fmt='none',
                        ecolor='black',elinewidth=1.35,capsize=4,capthick=1.25,zorder=9)
            verified.append(dict(system=system,sector=sector,metric=metric,
                                 modes=len(values),mean=mean,ci95=[lo,hi]))
    ax.set_title(title,loc='left',fontsize=11)
    ax.set_xticks(range(5),SECTORS); ax.set_xlabel('Symmetry sector')
    ax.set_ylabel(label); ax.set_ylim(bottom=0)
    ax.grid(axis='y',alpha=.18); ax.legend(frameon=False,fontsize=9)
fig.tight_layout()
finish(fig, FIGURE)
