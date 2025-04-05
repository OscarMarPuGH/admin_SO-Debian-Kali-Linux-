#!/bin/bash

usage() {
    echo "Uso: $0 [-g grupo] max"
    echo "max ha d'estar seguit de K, M o G "
    exit 1
}


if [ "$#" -lt 1 ]; then
    usage
fi


GROUP=""
while getopts 'g:' OPTION; do
    case "$OPTION" in
        g)
            GROUP="$OPTARG";;
        ?)
            usage;;
    esac
done


shift "$((OPTIND - 1))"


if [ "$#" -ne 1 ]; then
    usage
fi

MAX=$1


if [[ $MAX == *K ]]; then
    LIMIT_KB=${MAX%K}
elif [[ $MAX == *M ]]; then
    LIMIT_KB=$((${MAX%M} * 1024))
elif [[ $MAX == *G ]]; then
    LIMIT_KB=$((${MAX%G} * 1048576))
else
    echo "Error: max ha de terminar en K, M o G."
    exit 1
fi

mensaje="# Has sobrepasat l'espai de disc permes. Edita el teu arxiu .profile. per a esborrar o esitar el missatge"


comprobar() {
    local usuario=$1
    local directorio=$2
    local espacio_usado_kb=$3

    if [ "$espacio_usado_kb" -ge 1048576 ]; then
        local espacio_usado_gb=$(echo "scale=2; $espacio_usado_kb/1048576" | bc)
        echo "$usuario - Uso: $espacio_usado_gb GB"
    elif [ "$espacio_usado_kb" -ge 1024 ]; then
        local espacio_usado_mb=$(echo "scale=2; $espacio_usado_kb/1024" | bc)
        echo "$usuario - Uso: $espacio_usado_mb MB"
    else
        echo "$usuario - Uso: $espacio_usado_kb KB"
    fi

    if [ "$espacio_usado_kb" -gt "$LIMIT_KB" ]; then
        if ! grep -q "$mensaje" "$directorio/.profile"; then
            echo "$mensaje" >> "$directorio/.profile"
        fi
    fi
}

   espacio_grupo() {
    local grupo=$1
    local total_kb=0
    local miembros_grupo=$(getent group $grupo | cut -d: -f4)

    for usuario in ${miembros_grupo//,/ }; do
        local directorio_usuario=$(getent passwd $usuario | cut -d: -f6)
        if [ -d "$directorio_usuario" ]; then
            local espacio_usado_kb=$(du -s "$directorio_usuario" | cut -f1)
            total_kb=$((total_kb + espacio_usado_kb))
            comprobar "$usuario" "$directorio_usuario" "$espacio_usado_kb"
        fi
    done

    echo "Total grupo $grupo: $(echo "scale=2; $total_kb/1024" | bc) MB"
}


if [ -n "$GROUP" ]; then
    espacio_grupo "$GROUP"
else
   
    for directorio in /home/*; do
        if [ -d "$directorio" ]; then
           
            usuario=$(basename "$directorio")

           
            espacio_usado_kb=$(du -s "$directorio" | cut -f1)

           
            comprobar "$usuario" "$directorio" "$espacio_usado_kb"
        fi
    done
fi



