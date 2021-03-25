#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## Nota: para isto funcionar, instalar o gitpython:
# pip3 install gitpython

import os
from git import Repo

def main():
    repo = Repo.init(os.path.join('.', 'xptotry'))
    with open(os.path.join('.', 'xptotry', 'triedfile'), 'w') as nfl:
        nfl.write("ehehehehehehe\n\n\neheh!\n")
        nfl.close()
    repo.index.add(['triedfile'])
    repo.index.commit("Experiencia!")
    


if __name__ == "__main__": main()
