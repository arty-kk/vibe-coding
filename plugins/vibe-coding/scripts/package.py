#!/usr/bin/env python3
"""Validate and create a reproducible ZIP. Does not install or publish."""

import argparse
import os
import zipfile
from pathlib import Path
from validate import ROOT, validate


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',required=True,type=Path);p.add_argument('--force',action='store_true');args=p.parse_args()
    output=args.output.expanduser().resolve()
    if output.is_relative_to(ROOT):p.error('Output must be outside the plugin directory.')
    if output.exists() and not args.force:p.error('Output already exists; use --force to replace it.')
    errors=validate()
    if errors:p.error('Validation failed:\n'+'\n'.join(errors))
    output.parent.mkdir(parents=True,exist_ok=True);temp=output.with_suffix(output.suffix+'.tmp')
    try:
        with zipfile.ZipFile(temp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for file in sorted(ROOT.rglob('*')):
                if not file.is_file() or any(s in {'.git','__pycache__','.DS_Store'} for s in file.relative_to(ROOT).parts):continue
                info=zipfile.ZipInfo('vibe-coding/'+file.relative_to(ROOT).as_posix(),date_time=(2020,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
                z.writestr(info,file.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
        os.replace(temp,output)
    finally:
        if temp.exists():temp.unlink()
    print(output)


if __name__=='__main__':main()
