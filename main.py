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

"""PnCW: render the sixteen numerical-result figures from supplied data.

Terminal setup (macOS, Python 3.12):
  sh setup_macos.sh

Render all sixteen PDFs, sequentially:
  .venv/bin/python main.py
  .venv/bin/python main.py --output generated

Select figures or add PNG previews:
  .venv/bin/python main.py --list
  .venv/bin/python main.py --figure 06 --figure 07 --output selected
  .venv/bin/python main.py --png

Only Figures 03-10 and S01-S08 are included. The program reads local
CSV/NPZ/JSON files. It does not solve eigenproblems, recompute statistical
inference, compile documents, access another project, or use the network.
Existing output PDFs with the same names are regenerated; input data
are never overwritten. Documentation and model PDFs are not plot inputs
and are never opened by this runner.
"""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--list',action='store_true',help='List the sixteen figures')
    parser.add_argument('--figure',action='append',help='03-10 or S01-S08; repeat to select multiple figures')
    parser.add_argument('--output',type=Path,default=ROOT/'generated',help='Output directory (default: generated/)')
    parser.add_argument('--png',action='store_true',help='Also export 240-dpi PNG previews')
    args=parser.parse_args()
    index=json.loads((ROOT/'FIGURE_INDEX.json').read_text())
    if args.list:
        for key,value in index.items():print(key+'  '+value['directory']+'  '+value['title'])
        return
    selected=[]
    for key in args.figure or list(index):
        key=key.upper().replace('FIGURE_','')
        key=('S'+key[1:].zfill(2)) if key.startswith('S') else key.zfill(2)
        if key not in index:parser.error('Figure not included: '+key)
        if key not in selected:selected.append(key)
    output=args.output.resolve()
    protected=[ROOT/value['directory'] for value in index.values()]+[ROOT/'shared',ROOT/'documentation']
    if output==ROOT or any(output.is_relative_to(path) for path in protected):
        parser.error('Output must not overwrite distributed data or code directories.')
    output.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy()
    for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
        env[key]='1'
    env['PYTHONDONTWRITEBYTECODE']='1'
    env['MPLCONFIGDIR']=str(output/'.matplotlib')
    env['XDG_CACHE_HOME']=str(output/'.cache')
    records=[]
    for key in selected:
        print('Rendering Figure_'+key,flush=True)
        command=[sys.executable,str(ROOT/index[key]['directory']/'plot.py'),'--output',str(output)]
        if args.png:command.append('--png')
        subprocess.run(command,check=True,env=env)
        pdf=output/('Figure_'+key+'.pdf')
        if not pdf.is_file() or pdf.stat().st_size<500:raise RuntimeError('PDF not generated: '+str(pdf))
        records.append(dict(figure=key,pdf=pdf.name))
    record=dict(scope='Rendering supplied numerical data only; no physical solves or new inference.',
                count=len(records),python=sys.version.split()[0],figures=records)
    (output/'PLOT_RUN.json').write_text(json.dumps(record,indent=2)+'\n')
    print(f'Completed: {len(records)} figures in {output}',flush=True)


if __name__=='__main__':main()
