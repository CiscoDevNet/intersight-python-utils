# intersight-python-utils/config_targets

Automated Cisco Intersight Target (Device) Claim with the Python SDK.

## Python SDK Install and Setup
- Follow the instructions at https://github.com/CiscoDevNet/intersight-python-utils/blob/master/README.md for installing the Intersight Python SDK and settting up Intersight API credentials.

## Usage
The claim_target.py script can be run directly to claim systems or used with Ansible.  Below is an example using Ansible to allow for target claim run in parallel.

- Copy and edit the example_inventory for your target systems.  Target local management IPs are used as the inventory_hostname in example_inventory and local management credentials also must be provided.
- Run the example_claim.yml playbook to claim targets in Intersight.  Note that the playbook should be run from the config_targets subdirectory since the script will use the credentials module in the parent (../) directory.
```
$ pwd
/Users/dsoper/Documents/intersight-python-utils/config_targets

$ ansible-playbook -i tme_inventory example_claim.yml 

PLAY [all] ******************************************************************************************************************************************************************************

TASK [Define JSON string passed to claim script] ****************************************************************************************************************************************
ok: [172.28.225.122]
ok: [172.28.225.20]

TASK [Claim targets] ********************************************************************************************************************************************************************
ok: [172.28.225.20]
...
```

## Additional Information
See https://community.cisco.com/t5/data-center-and-cloud-documents/automated-intersight-target-claim/ta-p/3652214 for a detailed overview of Automated Target Claim in Intersight using the Python SDK.
