#!/bin/bash

echo "Resum de logins:"
for user_name in $(cat /etc/passwd | cut -d : -f1);do
  #user_name=`cat /etc/passwd | grep "$user" | cut -d: -f1`
  numlogs=0
  days=0
  hours=0
  minutes=0

  #echo $user_name
  for login in $(last -F $user_name | grep - | cut -d '(' -f2 | cut -d ')' -f1);do
    numlogs=$(($numlogs + 1)) # contador de logins
    # Sumatorio de dias, son el numero de dias que ha estado logeado el usuario
    day=$(echo $login | grep + | cut -d + -f1)
    numDay=${#day}
    if [ $numDay -ne 0 ]; then
      days=$(expr $days + $day)
    fi

    #Sumantorio de horas, son el numero de horas que ha estado logeado el usuario
    hour=$(echo $login | cut -d + -f2 | cut -d : -f1 )
    numHour=${#hour}
    if [ $hour -ne 0 ]; then
      hours=$(expr $hours + $hour)
    fi

    #Sumatorio de minutos, son el numero de minutos que ha estado logeado el usuario
    minute=$(echo $login | cut -d ':' -f2)
    numMinute=${#minute}
    if [ $numMinute -ne 0 ]; then
      minutes=$(expr $minutes + $minute)
    fi
  done

  # Pasamos las horas y los dias a minutos y se lo sumamos a los minutes que ya teniamos
  minutes=$(($minutes+($hours*60)+($days*24*60)))

  if [ $minutes -ne 0 ]; then
    echo "Usuari $user_name: temps total de login $minutes min, nombre total de logins: $numlogs"
  fi
done

echo -e ""
echo "Resum d'usuaris connectats"

for user_name in $(cat /etc/passwd | cut -d: -f1);do

  logged=`last -F "$user_name" | grep 'still logged in' | wc -l` #logged contiene

  if [ $logged -ne 0 ]; then
    numProcesos=`ps aux | grep $user_name | wc -l`
    #Con el comando awk lo que hacemos es coger la 3 columna y hacer un sumatorio de todas las filas de esta columna
    cpu=`ps aux | grep $user_name | awk 'NR>2{arr[1]+=$3}END{for(i in arr) print arr[1]}' `
    echo "Usuari $user_name: $numProcesos processos -> $cpu% CPU"
  fi
done