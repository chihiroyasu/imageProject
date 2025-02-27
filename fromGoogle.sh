#!/bin/bash
#REF: https://stackoverflow.com/questions/29010999/how-to-assign-echo-value-to-a-variable-in-shell
{
    ifs=$'\n' read -r -d '' stderr;
    ifs=$'\n' read -r -d '' stdout;
} < <((printf '\0%s\0' "$(/home/qqqlq/pypy/bin/python /home/qqqlq/yasu_device/imageProject/redundant.py)" 1>&2) 2>&1)

if [ -n "$stdout" ]
then
    echo -e "$stdout\n" >> /home/qqqlq/yasu_device/imageProject/log/fromGoogle.log
fi

if [ -n "$stderr" ]
then
    date +"[%y-%m-%d %H:%M:%S]" | awk -v var="$stderr" '{print $0,var}' >> /home/qqqlq/yasu_device/imageProject/fromGoogle-error.log 
fi
