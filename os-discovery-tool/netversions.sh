#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
lspcicmd=`which lspci`
modinfocmd=`which modinfo`
for pciaddress in $(${lshwcmd} -C Network 2>/dev/null | grep "pci@" | awk -F":" '{print $3":"$4}');
do
    versionstring=`${lspcicmd} -v -s $pciaddress | grep "Kernel driver" | \
    awk -F":" '{print $2}' | xargs ${modinfocmd} 2>/dev/null | grep ^version: | head -n1 | awk '{print $2}' | xargs`
if [ -z "${versionstring}" ]
    then
        echo `${lspcicmd} -v -s $pciaddress | grep "Kernel driver" | awk -F":" '{print $2}' | \
    xargs ${modinfocmd} 2>/dev/null | grep ^vermagic: | awk '{print $2}'`
    else
        echo ${versionstring}
    fi
done
# support for Emulex HBA Adapter
${lspcicmd} -nn | grep -Ei 'hba|host bus adapter|fibre channel' | awk -F" " '{print $1}' | while read pciaddress;
do
    hbaversionstring=`${lspcicmd} -v -s ${pciaddress} | grep "Kernel driver" | awk -F":" '{print $2}' | xargs ${modinfocmd} 2>/dev/null | grep ^version: | awk '{print $2}'`
    if [ -z "${hbaversionstring}" ]
    then
        echo `${lspcicmd} -v -s ${pciaddress} | grep "Kernel driver" | awk -F":" '{print $2}'| \
    xargs ${modinfocmd} 2>/dev/null | grep ^vermagic: | awk '{print $2}'`
    else
        echo ${hbaversionstring}
    fi
done