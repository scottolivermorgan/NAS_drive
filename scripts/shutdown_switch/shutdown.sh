#!/bin/bash

match='fields'
insert='/home/scott/NAS_drive/functions/shutdown.py'
file='/etc/rc.local'

sed -i "19 i $insert" $file