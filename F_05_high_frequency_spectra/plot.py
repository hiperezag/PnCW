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
From the package root: python3 main.py --figure 05
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
HERE = Path(__file__).resolve().parent
FIGURE = '05'

plt.rcParams['pdf.fonttype']=42

data = csv_rows(HERE/'curves.csv')
meta = read_json(HERE/'data.json')
colors = {'gas':'#B55224','aluminum':'#176E9C','goe':'#20242B','poisson':'#699449'}
plt.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':10,'legend.fontsize':8,
                     'axes.spines.top':False,'axes.spines.right':False})
fig,axes=plt.subplots(2,2,figsize=(8.4,6.6))
def curve(material, observable, model, unfolding):
    group=[r for r in data if r['material']==material and r['observable']==observable
           and r['model']==model and r['unfolding']==unfolding]
    return np.array([[float(r['x']),float(r['y'])] for r in group]).T
for col,material in enumerate(('gas','aluminum')):
    title=material.capitalize(); top=axes[0,col]; bottom=axes[1,col]
    record=next(r for r in meta['summary'] if r['material']==material)
    for model in ('poisson','goe'):
        x,y=curve(material,'ratio_cdf',model,'not_applicable')
        top.plot(np.r_[0,x,1],np.r_[0,y,1],color=colors[model],lw=1.45,
                 ls='--' if model=='poisson' else '-',label='Matched '+('GOE' if model=='goe' else 'Poisson'))
    x,y=curve(material,'ratio_cdf_exact','physical','not_applicable')
    top.step(x,y,where='post',color=colors[material],lw=1.65,label=title)
    top.set(xlim=(0,1),ylim=(0,1),xlabel=r'Adjacent-gap ratio $r$',ylabel=r'Cumulative distribution $F(r)$',
            title=f"({'ab'[col]}) {title}: {record['levels']} levels")
    top.text(.04,.94,rf"$\overline{{r}}={record['mean_ratio']:.4f}$"+'\n'+
             rf"$p_{{\mathrm{{GOE,CDF}}}}^{{\mathrm{{Holm}}}}={record['GOE_CDF_Holm_p']:.3f}$",
             transform=top.transAxes,va='top',fontsize=9)
    top.legend(loc='lower right',frameon=False)
    for unfolding,style in (('affine','-'),('quadratic','--')):
        for model in ('poisson','goe','physical'):
            x,y=curve(material,'number_variance',model,unfolding)
            if model=='physical':
                bottom.plot(x,y,color=colors[material],lw=1.8,ls=style,marker='o' if unfolding=='affine' else 's',
                            ms=5,markerfacecolor=colors[material] if unfolding=='affine' else 'white',zorder=4)
            else:
                bottom.plot(x,y,color=colors[model],lw=1.4,ls=style,marker='' if unfolding=='affine' else 'x',ms=4)
    bottom.set(xscale='log',yscale='log',xlim=(.88,9),ylim=(.36,9),
               xlabel=r'Interval length $L$ (mean spacings)',ylabel=r'Number variance $\Sigma^2(L)$',
               title=f"({'cd'[col]}) {title}: longer-range correlations")
    bottom.set_xticks([1,2,4,8],['1','2','4','8']);bottom.set_yticks([.5,1,2,4,8],['0.5','1','2','4','8']);bottom.minorticks_off()
    bottom.text(.03,.96,'GOE and Poisson rejected\nfor both unfoldings',transform=bottom.transAxes,va='top',fontsize=8.6)
    for ax in (top,bottom): ax.grid(axis='y',color='#e4e6e8',linewidth=.6);ax.set_axisbelow(True)
fig.text(.5,.018,'Lower panels: colors as above; solid = affine unfolding; dashed = quadratic unfolding. Logarithmic axes.',
         ha='center',va='bottom',fontsize=8)
fig.subplots_adjust(left=.08,right=.975,top=.955,bottom=.105,hspace=.43,wspace=.30)
finish(fig, FIGURE)
