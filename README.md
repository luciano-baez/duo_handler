DUO Handler  (Ver 0.8 ) (cmd script and Ansible module)
===========================================================
* This is a python script to be called from your shell script and a python module to be added in your playbooks or Roles in Ansible Tower*


## Requirements
------------
- For scripting python3
- For use in your playbooks in ansile, just usual Ansible requirements.

duo_handler module
===================
* This is a python module to handle duo configuration files and its includes
To implement this in a playbook you need to place the file duo_handler.py in the "library" directory and the duo_handler_lib.py on "module_utils" directory.


Module Functions
----------------
*Current programmed functions.*

Example get report
 
```yaml
  - name: Duo get report
    duo_handler:
      state: report
```




----------------------------------------------------------------------------------------------------------------------------

duo_handler_cmd command
=========================
* This is a python program to handle duo configuration files
In order to run it i recommned to follow this steps
    1 - Copy the duo_handler_cmd.py and the duo_hndlers_lib.py to a defined dir. Example /opt/scripts
    2 - create a script called duo_handler_cmd in the same directory with this content
```bash
if [ -f /usr/bin/python3 ]; then 
        python3  /opt/scripts/duo_handler_cmd.py $@
    else
        echo "ERR: You need python3"
    fi
```
    3 - Create a symbolic link in /usr/bin/, in order to have the script in the path
```bash
ln -s /opt/scripts/duo_handler_cmd /usr/bin/duo_handler_cmd
``` 

Then you will be able to run as this
    duo_handler_cmd -h
to see how to use ir.

Author Information
------------------
Role and modules developed by Luciano Baez (lucianobaez@kyndryl.com or lucianobaez1@ibm.com), working for the GI-SVC-GBSE team.
https://github.kyndryl.net/lucianobaez
https://github.ibm.com/lucianobaez1


Personal contact on lucianobaez@outlook.com ( https://github.com/luciano-baez )


