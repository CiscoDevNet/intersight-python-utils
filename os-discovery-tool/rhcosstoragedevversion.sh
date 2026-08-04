#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
modinfocmd=`which modinfo`
for var in "$@"
do
    ${modinfocmd} ${var} 2>/dev/null| grep -i "version" | head -n1 | awk '{print $2}'
done