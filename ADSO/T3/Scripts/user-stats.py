import subprocess as sp
import sys

#Defimos una funcion encargada de enviar comandos para facilitar la programacion en Python.
def run_command(command):
    process = sp.Popen(command, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    retcode = process.wait()
    if retcode != 0:
        raise Exception("Problem running command: " + command)
    stdout, stderr = process.communicate()
    return stdout.decode('UTF-8').rstrip()


print("Resum de logins:")

#Splitlines divide el string en elemenos para facilitaros porder iterarla
users = run_command("cat /etc/passwd | cut -d: -f1").splitlines()

for user in users:
    numlogs=0
    days=0
    hours=0
    minutes=0

    logins = run_command("last -F "+user+" | grep - | cut -d '(' -f2 | cut -d ')' -f1").splitlines()

    for login in logins:
        numlogs = numlogs + 1
        day = run_command("echo "+login+" | grep + | cut -d + -f1")
        if( day != ""):
            days = days + int(day)

        hour = run_command("echo "+login+" | cut -d + -f2 | cut -d : -f1")
        if( hours != ""):
            hours = hours + int(hour)

        minute = run_command("echo "+login+" | cut -d ':' -f2")
        if( minute != ""):
            minutes = minutes + int(minute)
    #print(minutes, hours, days)
    minutes = minutes + ( (hours*60) + (days*24*60) )
    if(minutes > 0):
        print("Usuari "+user+": temps total de login ",minutes," min, nombre total de logins: ",numlogs)


print("\nResum d'usuaris connectats")
users = run_command("cat /etc/passwd | cut -d: -f1").splitlines()

for user in users:
    logged = run_command("last -F "+ user + " | grep 'still logged in' | wc -l")
    if( logged != "0" ):
        numProcesos = run_command("ps aux | grep "+user+" | wc -l")
        cpu=run_command("ps aux | grep "+user+"| awk 'NR>2{arr[1]+=$3}END{for(i in arr) print arr[1]}'")
        print("Usuari "+user+": "+numProcesos+" processos -> "+cpu+"% CPU")