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
From the package root: python3 main.py --figure 06
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from plot_support import *
from io import BytesIO
from matplotlib.backends.backend_pdf import RendererPdf
HERE = Path(__file__).resolve().parent
FIGURE = '06'

data=read_json(HERE.parent/'shared'/'representative_modes.json'); archive=np.load(HERE/'data.npz')
plt.rcParams.update({'font.size':12,'axes.titlesize':11,'axes.labelsize':11,'xtick.labelsize':10,'ytick.labelsize':10})
names={'analytic_square':'Analytic square','empty_IEM':'IEM empty cell','gas':'H₂','aluminum':'Al'}
def full(quarter):
    upper=np.concatenate((quarter[:,::-1],quarter),axis=1)
    return np.concatenate((upper[::-1],upper),axis=0)

def pressure_rasters():
    """Sample the supplied fields at the declared PDF resolution.

    A material-first calibration layout fixes the nearest-neighbor pixel
    phase before the final panel permutation. Layout passes are in memory;
    they neither calculate fields nor create additional output figures.
    Capturing the PDF renderer's RGBA samples avoids a second resampling.
    """
    order=(6,7,8,9,10,11,0,1,2,3,4,5)
    frame,axes=plt.subplots(4,3,figsize=(10.8,11.8),layout='constrained')
    region=np.hypot(*np.meshgrid((np.arange(512)+.5)*np.pi/512,
                                (np.arange(512)+.5)*np.pi/512))>data['radius']
    empty=[]
    for slot,(axis,index) in enumerate(zip(axes.flat,order)):
        record=data['panels'][index]
        values=archive['normalized_squared_pressure_quarter'][index]
        image=axis.imshow(full(np.where(region,values,np.nan)),origin='lower',
            extent=(-np.pi,np.pi,-np.pi,np.pi),vmin=0,vmax=6,cmap='magma',interpolation='nearest')
        circle=Circle((0,0),data['radius'],facecolor='white',edgecolor='gray',lw=.8,
                      ls='-' if record['material_circle'] else '--')
        axis.add_patch(circle)
        frequency=f"{record['omega']:.8f}" if record['material_circle'] else f"{record['target']} (exact)"
        axis.set(title=f"({chr(97+slot)}) {names[record['system']]}  Ω={frequency}",
                 xlabel='x/ℓ₀' if slot//3==3 else '',ylabel='y/ℓ₀' if slot%3==0 else '')
        axis.set_xticks([-np.pi,0,np.pi],['−π','0','π'])
        axis.set_yticks([-np.pi,0,np.pi],['−π','0','π'])
        if not record['material_circle']:empty.append((image,circle,full(values)))
    frame.colorbar(image,ax=axes,label='|p|² / exterior mean(|p|²)',shrink=.72,pad=.02)
    frame.savefig(BytesIO(),format='png',dpi=240)
    frame.savefig(BytesIO(),format='pdf',dpi=240)
    frame.set_layout_engine(None)
    for image,circle,values in empty:image.set_data(values);circle.remove()
    captured=[]
    draw_image=RendererPdf.draw_image
    def capture(renderer,gc,x,y,image,transform=None):
        captured.append(image.copy())
        return draw_image(renderer,gc,x,y,image,transform)
    try:
        RendererPdf.draw_image=capture
        frame.savefig(BytesIO(),format='pdf',dpi=240)
    finally:
        RendererPdf.draw_image=draw_image
        plt.close(frame)
    if len(captured)!=13:raise RuntimeError('Unexpected pressure raster count')
    result=[None]*12
    for slot,index in enumerate(order):result[index]=captured[slot]
    return result


rasters=pressure_rasters()
fig,axes=plt.subplots(4,3,figsize=(10.8,11.8),layout='constrained')
for index,(ax,record) in enumerate(zip(axes.flat,data['panels'])):
    ax.imshow(rasters[index],origin='lower',extent=(-np.pi,np.pi,-np.pi,np.pi),interpolation='none')
    if record['material_circle']:ax.add_patch(Circle((0,0),data['radius'],facecolor='white',edgecolor='gray',lw=.8))
    frequency=f"{record['omega']:.8f}" if record['material_circle'] else f"{record['target']} (exact)"
    ax.set(title=f"({record['panel']}) {names[record['system']]}  Ω={frequency}",xlabel='x/ℓ₀' if index//3==3 else '',ylabel='y/ℓ₀' if index%3==0 else '')
    ax.set_xticks([-np.pi,0,np.pi],['−π','0','π']);ax.set_yticks([-np.pi,0,np.pi],['−π','0','π'])
fig.colorbar(matplotlib.cm.ScalarMappable(norm=matplotlib.colors.Normalize(0,6),cmap='magma'),
             ax=axes,label='|p|² / exterior mean(|p|²)',shrink=.72,pad=.02)
finish(fig, FIGURE)
