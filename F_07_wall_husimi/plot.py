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
From the package root: python3 main.py --figure 07
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '07'

data=read_json(HERE.parent/'shared'/'representative_modes.json'); archive=np.load(HERE/'data.npz')
plt.rcParams.update({'font.size':12,'axes.titlesize':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':10})
fig,axes=plt.subplots(4,3,figsize=(10.8,10.8),layout='constrained')
names={'analytic_square':'Analytic square','empty_IEM':'IEM empty cell','gas':'H₂','aluminum':'Al'}
for index,(ax,record) in enumerate(zip(axes.flat,data['panels'])):
    im=ax.imshow(4*np.pi*archive['H'][index],origin='lower',extent=(0,2*np.pi,-1,1),vmin=0,vmax=8,cmap='magma',aspect='auto')
    frequency=f"{record['omega']:.8f}" if record['material_circle'] else f"{record['target']} (exact)"
    ax.set(title=f"({record['panel']}) {names[record['system']]}  Ω={frequency}",xlabel='q = x mod 2π' if index//3==3 else '',ylabel='η = kₓ/Ω' if index%3==0 else '')
    ax.set_xticks([0,np.pi,2*np.pi],['0','π','2π']);ax.set_yticks([-1,0,1])
fig.colorbar(im,ax=axes,label='4πH',shrink=.72,pad=.02)
finish(fig, FIGURE)
