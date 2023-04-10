#/bin/bash

validate-tools(){
	if ! $(command -v modinfo &> /dev/null) || ! $(command -v lspci &> /dev/null) || ! $(command -v lshw &> /dev/null) || ! $(command -v ipmitool &> /dev/null)
	then
		echo "Error - Tools validation failed!  Make sure host has ipmitool, lshw(RHEL/Ubuntu/Centos)/hwinfo(SLES), pci-utils(lspci) and modinfo installed and available"                  
	exit
	fi
	
}

cleanup_host-inv()
{
	#Remove old host-inv.yaml off local system
	[ -e $filename ] && rm $filename
}

write-osinfo()
{
	#Start creating host-inv.yaml on local system
	echo "annotations:" > $filename

	kernel_version=$(uname -r | awk '{print $1}')
	os_type=$(uname -s | awk '{print $1}')
	os_arch=$(uname -m | awk '{print $1}')
	os_vendor=$(./osvendor.sh)


	if [[ $os_vendor == 'Ubuntu' ]]
	then
	  os_name=$(./debian-os-name.sh)
	  os_flavor=$(./debian-os-version.sh)
	  os_vendor='Ubuntu'
	elif [[ $os_vendor == 'rhel' ]]
	then
	  os_name=$(./redhat-os-name.sh)
	  os_flavor=$(./redhat-os-name.sh)
	  os_vendor='Red Hat'
	else
	  echo "Currently Unsupported OS"
	fi

	updateTimestamp=$(date -Is)

	releaseVersionString=$kernel_version
	type=$os_type
	vendor=$os_vendor
	name=$os_name
	arch=$os_arch

	echo " -kv:" >> $filename
	echo "  key: os.updateTimestamp" >> $filename
	echo "  value:" $updateTimestamp >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.kernelVersionString" >> $filename
	echo "  value:" $os_flavor >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.releaseVersionString" >> $filename
	echo "  value:" $releaseVersionString >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.type" >> $filename
	echo "  value:" $os_type >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.vendor" >> $filename
	echo "  value:" $os_vendor >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.name" >> $filename
	echo "  value:" $os_name >> $filename

	echo " -kv:" >> $filename
	echo "  key: os.arch" >> $filename
	echo "  value:" $os_arch >> $filename
}

write-networkinfo()
{
	echo "Getting Network Driver Info"

	drivers=$(./netdriver.sh)
	versions=$(./netversions.sh)
	description=$(./netdev.sh)

	totaldrivercount=0

	counter=0
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.name" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
		((totaldrivercount++))
	done <<< "$drivers"

	counter=0
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.version" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$versions"

	counter=0
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.description" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$description"
}

write-fcinfo()
{
	echo "Getting vHBA Driver Info"

	fc_dev=$(./fcdev.sh)
	drivers=$(./fcdriver.sh)
	versions=$(./fcversions.sh)

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.name" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$drivers"

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.version" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$versions"

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.description" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
		((totaldrivercount++))
	done <<< "$fc_dev"
}

write-storageinfo()
{
	echo "Getting Storage Driver Info"

	drivers=$(./storagedriver.sh)
	versions=$(./storageversions.sh)
	description=$(./storagedev.sh)

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.name" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$drivers"

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.version" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
	done <<< "$versions"

	counter=$totaldrivercount
	while IFS= read -r line; do
		echo " -kv:" >> $filename
		echo "  key: os.driver.$counter.description" >> $filename
		echo "  value:" $line >> $filename
		((counter++))
		((totaldrivercount++))
	done <<< "$description"
}

filename="host-inv.yaml"

validate-tools
cleanup_host-inv
write-osinfo
write-networkinfo
write-fcinfo
write-storageinfo

#Send host-inv.yaml file to IMC
./send_inventory_to_imc.sh
