#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
lspcicmd=`which lspci`
modinfocmd=`which modinfo`
enicdrivername="enic"
for pciaddress in $(${lshwcmd} -C Network 2>/dev/null | grep "pci@" | awk -F":" '{print $3":"$4}');
    do
        drivername=`${lspcicmd} -v -s $pciaddress | grep "Kernel driver" | awk -F":" '{print $2}'`
        if [[ $drivername == *"$enicdrivername"* ]]
        then
            kernalversion=`uname -r`
            echo ${kernalversion%.*}
        else
            versionstring=`${lspcicmd} -v -s $pciaddress | grep "Kernel driver" | \
            awk -F":" '{print $2}' | xargs ${modinfocmd} 2>/dev/null | grep ^version: | head -n1 | awk '{print $2}' | xargs`
            if [ -z "${versionstring}" ]
            then
                echo `${lspcicmd} -v -s $pciaddress | grep "Kernel driver" | awk -F":" '{print $2}' | \
                xargs ${modinfocmd} 2>/dev/null | grep ^vermagic: | awk '{print $2}'`
            else
                echo ${versionstring}
            fi
        fi
    done