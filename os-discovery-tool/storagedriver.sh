#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
lspcicmd=`which lspci`
for pciaddress in $(${lshwcmd} -C Storage 2>/dev/null | grep "pci@" | awk -F":" '{print $3":"$4}');
do
    pcioutput=$("$lspcicmd" -v -s "$pciaddress")
    kernel_driver=$(echo "$pcioutput" | grep "Kernel driver" | awk '{print $NF}')
    kernel_modules=$(echo "$pcioutput" | grep "Kernel modules" | awk '{print $NF}')
    if [ -n "$kernel_driver" ]; then
	    echo $kernel_driver
    else
	    echo $kernel_modules
    fi
done
