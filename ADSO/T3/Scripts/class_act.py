import os
import sys
import subprocess

usage = "Usage: python3 class_act.py [n] [\"name surname\"]"

if len(sys.argv) == 3:
    if sys.argv[1].isdigit():
        if not sys.argv[2]:
            print(usage)
            sys.exit(1)
    else:
        print(usage)
        sys.exit(1)
else:
    print(usage)
    sys.exit(1)

numF = sys.argv[1]
nomU = sys.argv[2]

if int(subprocess.getoutput(f"grep -c '\\b{nomU}\\b' /etc/passwd")) != 1:
    print(usage)
    sys.exit(1)

with open("/etc/passwd", "r") as f:
    passwd = f.read()
if nomU not in passwd:
    print(f"No existeix l'usuari ({nomU}) en el sistema")
    sys.exit(1)

usuariHome = ""
usuariNom = ""

for line in passwd.splitlines():
    if nomU in line:
        parts = line.split(":")
        usuariHome = parts[5]
        usuariNom = parts[0]
        break
    
cFitxers = subprocess.getoutput(f'find "{usuariHome}" -type f -mtime -{numF} 2>/dev/null')

nFitxers = len(cFitxers.splitlines())

if nFitxers == 0:
    nFitxers = nFitxers + 1

eFitxers = subprocess.getoutput(f'echo "{cFitxers}" | xargs du -b 2>/dev/null | awk \'{{s+=$1}} END {{print s}}\' | numfmt --to=iec')

if nFitxers == 0:
    print(f"{nomU} ({usuariNom}) no modifica cap fitxer")
elif nFitxers != 1:
    print(f"{nomU} ({usuariNom}) {nFitxers} fitxers modificats que ocupen {eFitxers}")
else:
    print(f"{nomU} ({usuariNom}) {nFitxers} fitxer modificat que ocupa {eFitxers}")

