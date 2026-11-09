#!/usr/bin/env python3
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
R=Path(__file__).resolve().parents[1]
files=sorted(p for p in R.rglob('*') if p.is_file() and not any(x in {'build','__pycache__','.git','.venv'} for x in p.relative_to(R).parts) and p.suffix not in {'.pyc','.tmp'})
(R/'dados/SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files if p.name!='SHA256SUMS.txt'))
files=sorted(set(files+[R/'dados/SHA256SUMS.txt']))
archive=R.parent/'projeto.zip'
with ZipFile(archive,'w',ZIP_DEFLATED) as z:
    for p in files:z.write(p,Path('projeto')/p.relative_to(R))
with ZipFile(archive) as z:assert z.testzip() is None
print(f'ZIP verificado: {archive} ({archive.stat().st_size} bytes, {len(files)} arquivos).')
