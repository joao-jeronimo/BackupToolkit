#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, io, re

LOGS_PATH = "/var/gitbackups/repos_segura/GitBackups/BackupLogs/"

class FIND_LEADIN: pass
class FILELIST: pass


def sum_log(filename, outfileh):
    # Mecanismo auxiliar para não depejar tudo imediatamente - precisamos disto
    # para contar o número de ficheiros salvos para cada unidade de backup:
    thisheader = []
    def flushlist():
        nonlocal thisheader
        for ln in thisheader:
            outfileh.write(ln)
        thisheader = []
    # Processar o log se o existir:
    with open(filename, "r") as infileh:
        maq_state = FIND_LEADIN
        while True:
            thisline = infileh.readline()
            if len(thisline)==0: break
            
            if maq_state == FIND_LEADIN:
                if thisline[0:2]=="==":
                    maq_state = FILELIST
                    thisheader.append(thisline.strip())
                    line_count = 0
                    # A linha seguinte deverá ser:
                    nextline1 = infileh.readline().strip()
                    if nextline1 != "receiving incremental file list":
                        print("##### ERRO: falta a frase 'receiving incremental file list'....")
                        exit(-1)
            elif maq_state == FILELIST:
                if thisline=='\n':
                    maq_state = FIND_LEADIN
                    thisheader[0] += " %d ficheiros atualizados\n"%line_count
                    flushlist()
                else:
                    thisheader.append(thisline)
                    line_count +=1
            else:
                print("##### ERRO: Estado inválido......: " + str(maq_state))
                exit(-1)

def proccess_file(day, hour, outfileh):
    # Construir filename e verificar se aquele log existe - nem todos existem:
    in_dirname = "BackupLog-%(day)s.dir" % { 'day': day, }
    in_filename = "BackupLog-%(day)s_%(hour)s" % { 'day': day, 'hour': hour, }
    in_filepath = LOGS_PATH+"/"+in_dirname+"/"+in_filename+".errors.txt"
    if not os.path.isfile(in_filepath):
        return
    # Se tudo bem, avançar:
    outfileh.write(
           ("#################################\n"+
            "### BackupLog-%(day)s_%(hour)s ###\n"+
            "#################################\n") % { 'day':      day, 'hour': hour,  }
            )
    sum_log(in_filepath, outfileh)

def remove_zeros(infileh, outfileh):
    while True:
        thisline = infileh.readline()
        if len(thisline)==0: break
        ###
        if not re.search("0 ficheiros atualizados", thisline, flags=0):
            outfileh.write(thisline)

# Streams argumentos de linha de comandos:
global_output = io.StringIO()
alldays = sys.argv[1:]
# Construir a lista de todos os logs que há num dia:
allmoments = []
for hournr in range(24):
    for minutenr in range(0, 60, 20):
        allmoments.append( ("%02d%02d"%( hournr, minutenr, )) )
# Lista de todos os logs a processar:
alllogs = []
for day in alldays:
    if not re.search("^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]$", day, flags=0):
        print("##### ERRO: Formato errado para o dia: "+day)
        exit(-1)
    for moment in allmoments:
        alllogs.append( (day, moment) )
# GC:
del alldays
del allmoments
print("A resumir logs: "+", ".join(map(lambda t: "%s_%s"%(t[0],t[1]), alllogs)))

# Processar realmente o pessoal:
for thislog in alllogs:
    # processar este ficheiro:
    pass1 = io.StringIO()
    proccess_file(thislog[0], thislog[1], pass1)
    pass2 = io.StringIO()
    remove_zeros(io.StringIO(pass1.getvalue()), pass2)
    # Verificar se, nesta data, algum ficheiro foi salvo:
    if not re.search("ficheiros atualizados", pass2.getvalue(), flags=0):
        # Ignorar ficheiro caso nada tenha sido atualizado:
        continue
    # Adicionar ao output global:
    global_output.write(pass2.getvalue())
    

print(global_output.getvalue())
