#!/usr/bin/python
#-*- coding: utf-8 -*-create_device.py

### configuration ######################################
DEVICE_NAME_NABAZTAG = "test_nabaztag"
ADDRESS = "openjabanab.fr"
VIOLET_TOKEN = "eeeeeeeeeeeeeeeeeeeeeeeeee"
VOICE = "claire"
MAC = "FFFFFFFFF"
TO = 'nabaztag'


from domogik.tests.common.testdevice import TestDevice
from domogik.common.utils import get_sanitized_hostname

plugin = 'nabaztag'

def create_device():
    ### create the device, and if ok, get its id in device_id
    client_id  = "plugin-{0}.{1}".format(plugin, get_sanitized_hostname())
    print "Creating the Nabaztag  device..."
    td = TestDevice()
    params = td.get_params(client_id, "nabaztag")
        # fill in the params
    params["device_type"] = "nabaztag"
    params["name"] = DEVICE_NAME_NABAZTAG
    params["address"] = ADDRESS
    params["violet_token"] = VIOLET_TOKEN
    params["voice"] = VOICE
    params["mac"] = MAC
    for idx, val in enumerate(params['global']):
        if params['global'][idx]['key'] == 'name' :  params['global'][idx]['value'] = DEVICE_NAME_NABAZTAG
        if params['global'][idx]['key'] == 'address' :  params['global'][idx]['value'] = ADDRESS
        if params['global'][idx]['key'] == 'violet_token' :  params['global'][idx]['value'] = VIOLET_TOKEN
        if params['global'][idx]['key'] == 'voice' :  params['global'][idx]['value'] = VOICE
        if params['global'][idx]['key'] == 'mac' :  params['global'][idx]['value'] = MAC
    for idx, val in enumerate(params['xpl']):
        params['xpl'][idx]['value'] = TO

    # go and create
    td.create_device(params)
    print "Device Nabaztag {0} configured".format(DEVICE_NAME_NABAZTAG)
    
if __name__ == "__main__":
    create_device()



