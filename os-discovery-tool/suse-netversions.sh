#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
hwinfocmd=`which hwinfo`
modinfocmd=`which modinfo`
versionstring=`${hwinfocmd} --network | grep Driver: | awk '{print $2}' | xargs ${modinfocmd} | grep ^version:`
if [ -z "$versionstring" ]
then
    ${hwinfocmd} --network | grep Driver: | awk '{print $2}' | xargs ${modinfocmd} | grep ^vermagic: | awk '{print $2}'
else
    ${versionstring} | awk -F":[[:space:]]+" '{print $2}'
fi
