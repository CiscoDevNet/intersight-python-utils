#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
modinfocmd=`which modinfo`
driver_name=`sudo ${lshwcmd} -C bus | awk '$1=="configuration:"{$1=""; print}' | grep fnic | awk '{print $1}' | awk -F"=" '{print $2}'| head -n 1`
driver_name_modinfo=`sudo ${modinfocmd} fnic | awk '$2 == "fnic"{print $2}'`
if [ -z ${driver_name} ]
then
        echo ${driver_name_modinfo}
else
        echo ${driver_name}
fi