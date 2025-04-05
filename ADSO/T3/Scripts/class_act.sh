#!/bin/bash
usage="Usage: ./class_act.sh [n] [\"name surname\"]"

if [ $# -eq 2 ]; then
    # comprobem que és un nombre enter natural
    if [[ $1 =~ ^[0-9]+$ ]]; then
        # comprobem que no està buit
        if [[ -z "$2" ]]; then
        	echo $usage; exit 1
        fi
    else
        echo $usage; exit 1
    fi
else
    echo $usage; exit 1
fi

numF=$1
nomU="$2"

if [ $(grep -c "\b$nomU\b" /etc/passwd) -ne 1 ]; then
	echo $usage; exit 1
fi

usuari="$(grep "$nomU\>" /etc/passwd)"

usuariHome=""
usuariNom=""

if [ -z "$usuari" ]; then
    echo "No existeix l'usuari ("$nomU") en el sistema"
    exit 1
else
    usuariHome="$(echo "$usuari" | cut -d: -f6)"
    usuariNom="$(echo "$usuari" | cut -d: -f1)"
fi

nFitxers=0
cFitxers=$(find "$usuariHome" -type f -mtime -"$numF" 2>/dev/null)
nFitxers=$(echo "$cFitxers" | wc -l)
eFitxers=$(echo "$cFitxers" | xargs du -b 2>/dev/null | awk '{s+=$1} END {print s}' | numfmt --to=iec)

if [ $nFitxers -eq 0 ]; then
    echo "$nomU ($usuariNom) no modifica cap fitxer"
elif [ $nFitxers -ne 1 ]; then
    echo "$nomU ($usuariNom) $nFitxers fitxers modificats que ocupen $eFitxers"
else
    echo "$nomU ($usuariNom) $nFitxers fitxer modificat que ocupa $eFitxers"
fi
