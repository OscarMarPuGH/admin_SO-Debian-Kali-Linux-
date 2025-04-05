#!/bin/bash

# Comprova si s'ha proporcionat el nom de l'usuari
if [ -z "$1" ]; then
    echo "Ús: $0 <nom_usuari>"
    exit 1
fi

USER=$1

# Obtenir el directori Home de l'usuari
USER_HOME=$(getent passwd "$USER" | cut -d: -f6)

# Comprovar si l'usuari existeix
if [ -z "$USER_HOME" ]; then
    echo "L'usuari '$USER' no existeix."
    exit 1
fi

# Mida total del directori Home de l'usuari
HOME_SIZE=$(du -sh "$USER_HOME" 2>/dev/null | cut -f1)

# Buscar directoris fora del directori Home on l'usuari té fitxers
OTHER_DIRS=$(find / -path "$USER_HOME" -prune -o -user "$USER" -type d -exec dirname {} \; 2>/dev/null | sort -u)

# Nombre de processos actius de l'usuari
ACTIVE_PROCESSES=$(ps -u "$USER" | wc -l)

# Mostrar la informació
echo "Home: $USER_HOME"
echo "Home size: $HOME_SIZE"
echo "Other dirs: $OTHER_DIRS"
echo "Active processes: $((ACTIVE_PROCESSES - 1))"  # Resta un per no comptar el procés 'ps'

