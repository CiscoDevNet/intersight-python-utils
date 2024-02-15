#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
hwinfocmd=`which hwinfo`
modinfocmd=`which modinfo`
drivers=`${hwinfocmd} --network | grep Driver: | awk '{gsub(/"/,"",$2); print $2}'`
for driver in $drivers; do
    versionstring=`$modinfocmd $driver | grep ^version:`
    if [ -z "$versionstring" ]
    then
        $modinfocmd $driver | grep ^vermagic: | awk '{print $2}'
    else
        $modinfocmd $driver | grep ^version: | awk -F":[[:space:]]+" '{print $2}'
    fi
done
