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
From the package root: python3 main.py --figure 10
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '10'

data=np.load(HERE/'data.npz')
omega=data['omega']
shift_percent=data['shift_percent']
envelope_percent=data['envelope_percent']
channel_al=data['channel_al']
channel_rigid=data['channel_rigid']
theta=data['theta']
gas_phase=data['gas_phase']
al_phase=data['al_phase']
theta_min=19.29859
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9.5,
    'axes.labelsize':9.5,'axes.titlesize':10,'xtick.labelsize':8.5,
    'ytick.labelsize':8.5,'legend.fontsize':8.2,'axes.linewidth':.65,
    'pdf.fonttype':42,'ps.fonttype':42,'mathtext.fontset':'dejavusans'})
fig,axes=plt.subplots(1,3,figsize=(10.9,4.05),gridspec_kw={'width_ratios':[1.04,1,1.04]})
fig.subplots_adjust(left=.07,right=.985,bottom=.19,top=.76,wspace=.43)
blue='#235f85';orange='#bc612e';gray='#a2a8ad'
a,b,c=axes
a.vlines(omega,shift_percent-envelope_percent,shift_percent+envelope_percent,color=gray,lw=.65,alpha=.8,zorder=1)
a.scatter(omega,shift_percent,color=blue,s=9,edgecolor='none',zorder=3)
a.axhline(0,color='#666666',lw=.65,zorder=0)
a.set(xlim=(25.9,34.1),ylim=(-.085,.41),xticks=[26,28,30,32,34],yticks=[0,.1,.2,.3],
      xlabel=r'Reduced frequency $\Omega$',ylabel=r'$(\Omega_{\rm rigid}-\Omega_{\rm Al})/g_i$ (%)')
a.set_title('(a) Small spectral perturbation',loc='left',pad=10)
a.legend(handles=[Line2D([],[],linestyle='none',marker='o',ms=3.6,color=blue,label='All 184 modes'),
                  Line2D([],[],color=gray,lw=1,label='Observed p-refinement envelope')],
         loc='upper left',frameon=False,handlelength=1.4,borderpad=0,labelspacing=.5)
a.text(.02,.76,'Maximum with envelope: 0.2574%',transform=a.transAxes,fontsize=8)
b.plot([0,16],[0,16],color='#8f969c',lw=1.0,zorder=1,label='Identity')
b.scatter(channel_al,channel_rigid,s=14,facecolors='white',edgecolors=blue,linewidths=.6,alpha=.88,zorder=3,label='All 184 pairs')
b.set(xlim=(0,16),ylim=(0,16),xticks=[0,4,8,12,16],yticks=[0,4,8,12,16],
      xlabel=r'$N_{\rm ch}$, elastic aluminum',ylabel=r'$N_{\rm ch}$, rigid inclusion')
b.set_aspect('equal',adjustable='box')
b.set_title('(b) Directional mixing retained',loc='left',pad=10)
b.text(.04,.92,'Means: 5.98815 / 5.98833',transform=b.transAxes,va='top',fontsize=8.2)
b.legend(loc='lower right',frameon=False,handlelength=1.5,borderpad=.1)
c.plot(theta,gas_phase,color=orange,lw=1.8,label='Gas inclusion')
c.plot(theta,al_phase,color=blue,lw=1.8,label='Elastic aluminum')
c.axvline(theta_min,color='#707070',lw=.75,ls=':')
c.set(xlim=(theta_min,80),ylim=(-190,14),xticks=[20,40,60,80],yticks=[-180,-120,-60,0],
      xlabel=r'Incidence from normal $\theta$ (deg)',ylabel=r'Pressure reflection phase $\arg r$ (deg)')
c.set_title('(c) Distinct boundary phases',loc='left',pad=10)
c.legend(loc='center',bbox_to_anchor=(.53,.62),frameon=False)
c.text(.51,.31,r'$|r|^2=1$ for both materials',transform=c.transAxes,ha='center',fontsize=8.6)
for ax in axes:
    ax.spines[['top','right']].set_visible(False)
    ax.grid(color='#e7e7e7',lw=.5,zorder=-1)
# Explicit separation of a global modal intervention from a local model.
fig.text(.353,.955,r'SAME PhCW: central ppa modes, $26<\Omega\leq34$',ha='center',weight='bold',fontsize=10)
fig.text(.353,.891,'Elastic inclusion replaced by a rigid boundary on the same circle',ha='center',fontsize=8.8,color='#444444')
fig.text(.848,.955,'LOCAL PLANAR INTERFACE',ha='center',weight='bold',fontsize=10)
fig.text(.848,.891,'Lossless half-spaces; not a new guide',ha='center',fontsize=8.8,color='#444444')
fig.add_artist(Line2D([.663,.663],[.12,.982],transform=fig.transFigure,color='#b0b4b8',lw=.75))
fig.text(.353,.032,'Field conservation under a controlled intervention; not a per-mode chaos test.',ha='center',fontsize=8.5,color='#444444')
fig.text(.848,.032,r'Common phase axis; $\theta\geq19.29859^\circ$.',ha='center',fontsize=8.5,color='#444444')
finish(fig, FIGURE)
