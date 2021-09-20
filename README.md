# pyitop
Small iTop REST API Python library. It can be used to interact with iTop REST API in case of get or update CIs.

## Features
- Get iTop CIs
- Update iTop CIs

## Usage example
```code Python
from pyitop import iTopAPI

iapi = iTopAPI(url='http://itop.domail.local/webservices/rest.php?version=1.3', user='itop-user', password='P@ssw0rd', ssl_verify=False)
iapi.get('VirtualMachine') # get all CIs of VirtualMachine class
iapi.get('Server', key=2) # get Server CI with key = 2
iapi.get('Server', key={'name': 'server-01'}) # get Server CI with name equals to 'server-01'
iapu.get('VirtualMachine', key=42, output_fileds=['name', 'osfamily_name']) # get Virtual machine with key = 42, but retrieve only 'name' and 'osfamily_name' attributes
```
