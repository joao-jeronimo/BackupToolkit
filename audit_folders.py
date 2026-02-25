#!/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
from pathlib import Path

def scanfolders(folder):
    gen = Path(folder).rglob("*")
    for fol in gen:
        # Skip directories:
        if fol.is_dir():
            continue
        # Yield this path:
        if not fol.is_absolute():
            fol = os.path.join(os.path.curdir, fol)
        yield fol

for folpath in scanfolders(folder = sys.argv[1]):
    print(folpath)
