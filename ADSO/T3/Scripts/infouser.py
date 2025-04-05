import os
import pwd
import subprocess
import sys

def get_home_directory(user):
    try:
        return pwd.getpwnam(user).pw_dir
    except KeyError:
        print(f"L'usuari '{user}' no existeix.")
        sys.exit(1)

def get_home_size(home_dir):
    try:
        result = subprocess.run(['du', '-sh', home_dir], stdout=subprocess.PIPE, text=True, check=True)
        return result.stdout.split()[0]
    except subprocess.CalledProcessError:
        return "Error obtenint la mida del directori Home."

def get_other_dirs(user, home_dir):
    try:
        result = subprocess.run(['find', '/', '-path', home_dir, '-prune', '-o', '-user', user, '-type', 'd', '-print'],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, check=True)
        dirs = result.stdout.strip().split('\n')
        # Obtener solo los directorios principales (equivalente a `dirname` en Bash)
        parent_dirs = {os.path.dirname(d) for d in dirs if d}
        return sorted(parent_dirs)  # Ordena y elimina duplicados
    except subprocess.CalledProcessError:
        return []

def get_active_processes(user):
    try:
        result = subprocess.run(['ps', '-u', user, '--no-headers'], stdout=subprocess.PIPE, text=True, check=True)
        processes = result.stdout.strip().split('\n')
        return len(processes) if processes[0] else 0
    except subprocess.CalledProcessError:
        return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ús: infouser.py <nom_usuari>")
        sys.exit(1)

    user = sys.argv[1]
    home_dir = get_home_directory(user)
    home_size = get_home_size(home_dir)
    other_dirs = get_other_dirs(user, home_dir)
    active_processes = get_active_processes(user)

    print(f"Home: {home_dir}")
    print(f"Home size: {home_size}")
    print("Other dirs:", " ".join(other_dirs) if other_dirs else "None")
    print(f"Active processes: {active_processes}")
