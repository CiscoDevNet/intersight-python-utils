#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
lspcicmd=`which lspci`
for pciaddress in $(${lshwcmd} -C Network 2>/dev/null | grep "pci@" | awk -F":" '{print $3":"$4}');
do
    ${lspcicmd} -v -s ${pciaddress} | grep "Kernel driver" | awk -F":" '{print $2}' | xargs;
done
# support for QLogic and Emulex HBA Adapter
${lspcicmd} -nn | grep -Ei 'hba|host bus adapter|fibre channel|Fibre Channel' | awk -F" " '{print $1}' | while read pciaddress;
do
    ${lspcicmd} -v -s ${pciaddress} | grep "Kernel driver" | awk -F":" '{print $2}'| xargs;
done
