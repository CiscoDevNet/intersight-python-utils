#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
lshwcmd=`which lshw`
lspcicmd=`which lspci`
gpuvendornvidia='nvidia'
gpuvendoramd='amd'
nvidiasmicmd=`which nvidia-smi 2>&1`
amdcmdpath="/opt/rocm/.info/version"
invalid=" |'"

for pciaddress in $(${lshwcmd} -C Display 2>/dev/null | grep "pci@" | awk -F":" '{print $3":"$4}');
do
    displaydevice=$(${lspcicmd} -v -s ${pciaddress} | grep "Subsystem" | awk -F":" '{print $2}'| xargs);
    # NVIDIA Vendor GPU
    if [[ ${displaydevice,,} =~ ${gpuvendornvidia} ]]; then
        if ! ([[ $nvidiasmicmd =~ $invalid || -z "$nvidiasmicmd" ]]); then
            echo $displaydevice
        fi
    # AMD Vendor GPU
    elif [[ ${displaydevice,,} =~ ${gpuvendoramd} ]]; then
        if [ -e $amdcmdpath ]; then
            echo $displaydevice
        fi
    fi
done
