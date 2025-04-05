#!/usr/bin/env python3
import os
import sys
import grp
import pwd
import subprocess

def usage():
    print("Ús: ocupacio.py [-g grup] max")
    print("max ha d'estar seguit de K, M o G")
    sys.exit(1)

def convert_size(size):
    units = {"K": 1, "M": 1024, "G": 1024**2}
    number, unit = size[:-1], size[-1]
    if unit.upper() in units:
        return int(number) * units[unit.upper()]
    else:
        print("Error: max ha de terminar en K, M o G.")
        sys.exit(1)

def format_size(size_kb):
    if size_kb >= 1048576:
        return f"{size_kb / 1048576:.2f} GB"
    elif size_kb >= 1024:
        return f"{size_kb / 1024:.2f} MB"
    else:
        return f"{size_kb} KB"

def get_disk_usage(directory):
    try:
        result = subprocess.run(['du', '-sk', directory], stdout=subprocess.PIPE, text=True)
        usage_kb = int(result.stdout.split()[0])
        return usage_kb
    except (IndexError, ValueError, subprocess.CalledProcessError):
        print(f"Error al obtenir l'espai per a {directory}")
        return 0

def check_usage(home_dir, max_permitted_kb):
    usage_kb = get_disk_usage(home_dir)
    formatted_usage = format_size(usage_kb)
    user = os.path.basename(home_dir)
    print(f"{user}\t\t{formatted_usage}")
    
    if usage_kb > max_permitted_kb:
        mensaje = "# Has sobrepassat l'espai de disc permès. Edita el teu arxiu .profile per a esborrar o editar el missatge."
        profile_path = os.path.join(home_dir, '.profile')
        with open(profile_path, 'a') as profile:
            profile.write(f"\n{mensaje}\n")

def get_group_members(group_name):
    try:
        gid = grp.getgrnam(group_name).gr_gid
        members = [pwd.getpwuid(u.pw_uid).pw_name for u in pwd.getpwall() if u.pw_gid == gid]
        return members
    except KeyError:
        print(f"El grup '{group_name}' no existeix.")
        sys.exit(2)

def check_group_usage(group_name, max_permitted_kb):
    members = get_group_members(group_name)
    total_kb = 0
    for user in members:
        home_dir = os.path.join('/home', user)
        if os.path.isdir(home_dir):
            usage_kb = get_disk_usage(home_dir)
            total_kb += usage_kb
            check_usage(home_dir, max_permitted_kb)
    print(f"Total grup {group_name}: {format_size(total_kb)}")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        usage()

    group_name = ""
    if "-g" in sys.argv:
        g_index = sys.argv.index("-g")
        group_name = sys.argv[g_index + 1]
        max_permitted = sys.argv[g_index + 2]
    else:
        max_permitted = sys.argv[1]

    max_permitted_kb = convert_size(max_permitted)

    if group_name:
        check_group_usage(group_name, max_permitted_kb)
    else:
        for home_dir in os.listdir('/home'):
            full_path = os.path.join('/home', home_dir)
            if os.path.isdir(full_path):
                check_usage(full_path, max_permitted_kb)

if __name__ == "__main__":
    main()



