#!/bin/bash

insert='python /home/'$UN'/NAS_drive/functions/shutdown.py &'
file='/etc/rc.local'

sed -i "19 i $insert" $file