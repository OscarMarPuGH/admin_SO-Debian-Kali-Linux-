import os
import sys
import subprocess

p = 0
usage = "Usage: BadUser.py [-p]"

if len(sys.argv) > 1:
    if len(sys.argv) == 2:
        if sys.argv[1] == "-p":
            p = 1
        else:
            print(usage)
            sys.exit(1)
    else:
        print(usage)
        sys.exit(1)

# llegir el fitxer de password i només agafar el camp de nom de l'usuari
with open("/etc/passwd") as f:
    for line in f:
        user = line.split(":")[0]
        home = line.split(":")[5]

        if os.path.isdir(home):
            num_fich = int(subprocess.getoutput(f'find {home} -type f -user {user} 2>/dev/null | wc -l'))
        else:
            num_fich = 0

        if num_fich == 0:
            if p == 1:
                # detectar si l'usuari té processos en execució
                user_proc = int(subprocess.getoutput(f'pgrep -u {user} | wc -l'))
                if user_proc == 0:
                    print(user)
            else:
                print(user)