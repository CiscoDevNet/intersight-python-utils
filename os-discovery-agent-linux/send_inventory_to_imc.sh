#!/bin/bash

inventoryfilename="host-inv.yaml"

echo "[localhost]: Removing existing host-inv.yaml inventory file from IMC"
cmd="ipmitool raw 0x36 0x77 0x03 0x68 0x6f 0x73 0x74 0x2d 0x69 0x6e 0x76 0x2e 0x79 0x61 0x6d 0x6c"
$cmd

echo "[localhost]: Getting File Descriptor For host-inv.yaml inventory file from IMC"
filedescriptor=$(ipmitool raw 0x36 0x77 0x00 0x68 0x6f 0x73 0x74 0x2d 0x69 0x6e 0x76 0x2e 0x79 0x61 0x6d 0x6c)
filedescriptor="0x${filedescriptor:1}"

filebytearray=($(od -An -vtx1 $inventoryfilename | tr -d '\n'))

payload=""
counter=0
payloadlength="0x28"
filelocationpointer=0

echo "[localhost]: Writing inventory to IMC"

for (( i=0; i<${#filebytearray[@]}; i++ )); do
    b=${filebytearray[$i]}
    ((counter++))
    if [ $counter -le 39 ]; then
        payload+=$(printf '0x%s ' "$b")
    else
        payload+=$(printf '0x%s ' "$b")
        filepointer=$(printf "0x%04X" $filelocationpointer)
        filepointer=$(echo $filepointer | sed -E 's/0x(..)(..)/0x\2 0x\1/')
        cmd="ipmitool raw 0x36 0x77 0x02 "$filedescriptor" "$payloadlength" "$filepointer" 0x00 0x00 "$payload
        filelocationpointer=$((filelocationpointer+40))
        $cmd
        counter=0
        payload=""
    fi
done

filepointer=$(printf "0x%04X" $filelocationpointer)
filepointer=$(echo $filepointer | sed -E 's/0x(..)(..)/0x\2 0x\1/')
cmd="ipmitool raw 0x36 0x77 0x02 "$filedescriptor" "$(printf '0x%x\n' $counter)" "$filepointer" 0x00 0x00 "$payload
$cmd

echo "[localhost]: Closing IMC file handle"
cmd="ipmitool raw 0x36 0x77 0x01 "$filedescriptor
$cmd
