#!/bin/bash

# Construir base name para os ficheiros log de backup:
export THEDAY="`date +"%F"`"
export THEDATE="`date +"%F_%H%M"`"
export FILE_BASEDIR="./repos_segura/GitBackups/BackupLogs/BackupLog-$THEDAY.dir/"
export FILE_BASEPATH="$FILE_BASEDIR/BackupLog-$THEDATE"


# Verificar se o estação de backups está montada:
if [ "`mount | grep repos_segura | wc -l`" == "0" ]
then
   echo "`date`: O armazenamento 'Segura' não está montado." >> ./ERROR_NOT_MOUNTED.txt
   echo "abortando..."
   exit 0
else
   echo "'Segura' está montada..."
   mkdir -p "$FILE_BASEDIR"
fi

# Não queremos que isto execute concorrentemente:
export PIDFILE=running/"$$.pid"
touch "$PIDFILE"
if [ "`ls running/ | wc -l`" != "1" ]
then
   echo "O backup foi cancelado por o anterior ainda se encontrar em execução." >> "$FILE_BASEPATH".txt
   echo "abortando..."
   rm "$PIDFILE"
   exit 0
else
   echo "continuando..."
fi

# Fazer novo backup:
date >> "$FILE_BASEPATH".txt
./backend_update_backups.bash >> "$FILE_BASEPATH".txt >> "$FILE_BASEPATH".errors.txt
./backend_sql_backups.bash >> "$FILE_BASEPATH".txt >> "$FILE_BASEPATH".errors.txt
date >> "$FILE_BASEPATH".txt

rm "$PIDFILE"
