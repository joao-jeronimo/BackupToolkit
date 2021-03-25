#!/bin/bash

init_git () {
    export thepath=$1
    mkdir "$thepath"
    pushd "$thepath"
    git init 
    git config --global user.email "user@example.com"
    git config --global user.name "John Smith"
    popd
}

#init_git repos_segura/GitBackups/f_drive/
#init_git repos_segura/GitBackups/g_drive/
#init_git repos_segura/GitBackups/h_drive/
#init_git repos_segura/GitBackups/i_drive/
#init_git repos_segura/GitBackups/p_drive/


#######################################
do_rsync () {
    export orig_ip="$1"
    export orig_port="$2"
    export orig_username="$3"
    export orig_path="$4"
    export dest_path="$5"
    
    # Nota: --archive é equivalente a -rlptgoD. Mas aqui usamos apenas os seguintes:
    #    r - Recursivo.
    #    l - Listar detalhes dos ficheiros.
    #    t - Preservar timestamps (sem isto o rsync não é capaz de "saltar" os ficheiros que não foram anterados.
    #    v - Listar os ficheiros ao copiar.
    #   (Nota: as opções -ogp não foram usadas pk podiam impedir a VM de backups de manipular os ficheiros e de os adicionar ao git.)
    rsync -rlt --delete --exclude=".recycle" --exclude=".git" -v --port="$orig_port" "$orig_username"@"$orig_ip":"$orig_path" "$dest_path"
}

do_commit_git() {
    export repo_path=$1
    
    pushd "$repo_path"
    
    git add .
    git commit -m "Backup de dia: `date`"
    
    popd
}


#######################################
update_backup () {
    export backupname="$1"
    export orig_ip="$2"
    export orig_port="$3"
    export orig_username="$4"
    export orig_path="$5"
    export dest_path="$6"

    printf "== Iniciado backup %s\n" "$backupname"
    do_rsync "$orig_ip" "$orig_port" "$orig_username" "$orig_path" "$dest_path"
    do_commit_git "$dest_path"
    printf "\n\n"
}

#######################################

# Unidades F: e G::
update_backup "Unidade F:" IP.IP.IP.IP 22 remotebackups /remote/path/ local/path/
update_backup "Unidade G:" IP.IP.IP.IP 22 remotebackups /remote/path/ local/path/

###################################################
### Melhoramentos a fazer:
# Os acentos aparecem mal em ambos os sítios: origem e destino.
# O rsync deverá guardar logs de cada vez que faz a sincrinização.
# Não só os logs do rsync em si, mas também os git-status entre commits.
# Escrever tão-bem o tempo total de sincronização das drives todas.
# De vez em quando tem que se fazer "git-prune" (mas não git-gc, que vai querer comprimir coisas).
# (etc)
