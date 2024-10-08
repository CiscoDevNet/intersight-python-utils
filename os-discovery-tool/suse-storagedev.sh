#!/bin/bash
export PATH=$PATH:/sbin:/usr/sbin
hwinfocmd=`which hwinfo`
modinfocmd=`which modinfo`
${hwinfocmd} --storage | grep Driver: | awk '{print $2}' | xargs ${modinfocmd} | grep -E '(^description:|^name:)'  | awk -F":[[:space:]]+" '{print $2}'
