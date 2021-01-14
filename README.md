# intersight-python-utils

Cisco Intersight Python SDK examples.  Examples use the SDK available at https://intersight.com/apidocs/downloads/

## Python SDK Install
- Download the Python SDK from https://intersight.com/apidocs/downloads/ (be sure to dowload the OpenAPI schema version 3 SDK).  A web browser can be used to download, or you can download with wget or similar command line utilities (update the URL as needed based on the current SDK from https://intersight.com/apidocs/downloads/ :
```
wget https://cdn.intersight.com/components/an-apidocs/1.0.9-2908/model/intersight_python_sdk_v3_1.0.9.2908.tar.gz
```

- Install the SDK:
```
sudo pip install intersight_python_sdk_v3_1.0.9.2908.tar.gz
```

- Ensure that you only have one Intersight SDK active (older Intersight SDKs may conflict):
```
$ pip list
Package            Version   
------------------ ----------
<snip>
Intersight-OpenAPI 1.0.9.2908
```
(pip uninstall any intersight SDKs that may have been previously installed)

## Usage
If you're using playbooks in this repo, you will need to provide your own inventory file and cusomtize any variables used in playbooks with settings for your environment.
Here's an example inventory for the k8s-cluster playbooks (based on the examples at https://www.learnitguide.net/2019/01/install-kubernetes-cluster-using-ansible.html ):
```
[kube_main]
172.22.248.19

[kube_nodes]
172.22.248.[22:23]

[kube:children]
kube_main
kube_nodes

[kube:vars]
ansible_ssh_user=root
```
For demo purposes, you can copy the example above to a new file named inventory.  Then, edit the inventory file to provide your own hostnames (IPs).

Once you've inventory is setup, you'll also need to make sure you have ssh key based access to each host in the inventory.  
To do this place your ssh public key in ~/.ssh/authorized_keys on the host and verify you can login without a password:
```
ssh root@172.22.248.19
```

Here are example command lines for creating a k8s cluster (run from in the k8s-cluster subdirectory):
```
ansible-playbook -i inventory prereqs.yml --vault-id tme@vault_password_file
```
The --vault-id is only needed for RedHat distributions and subscription manager.  You can omit that argument for CentOS based config.

You can also specify your own host group if you have a different setup in your inventory file:
```
ansible-playbook -i inventory prereqs.yml -e group=demo
```
