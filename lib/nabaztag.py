# !/usr/bin/python
# -*- coding: utf-8 -*-

# import PyNUT
import time
from domogik_packages.plugin_nabaztag.lib.nabaztag_client import NabaztagClient, getClientId
from domogik_packages.plugin_nabaztag.lib.client_devices import GetDeviceParams, OPERATORS_SERVICE


class NabaztagClientsManagerException(Exception):
    """
    Nabaztag Manager exception
    """

    def __init__(self, value):
        Exception.__init__(self)
        self.value = "NabaztagClientsManager exception" + value

    def __str__(self):
        return repr(self.value)


class NabaztagClientsManager:
    """
    Manager Nabaztag Web Clients.
    """

    def __init__(self, xplPlugin, cb_send_xPL):
        """Init manager Nabaztag Clients"""
        self._xplPlugin = xplPlugin
        self._cb_send_xPL = cb_send_xPL
        self.clients = {}  # list of all Nabaztag Clients
        self._xplPlugin.log.info(u"Manager Nabaztag Clients is ready.")

    def _del__(self):
        """Delete all Nabaztag CLients"""
        print "try __del__ NabaztagClients"
        for id in self.clients: self.clients[id] = None

    def stop(self):
        """Close all Nabaztag CLients"""
        self._xplPlugin.log.info(u"Closing NabaztagManager.")
        for id in self.clients: self.clients[id].close()

    def addClient(self, instance):
        """Add a Nabaztag from domogik instance"""
        name = getClientId(instance)
        if self.clients.has_key(name):
            self._xplPlugin.log.debug(u"Manager Client : Nabaztag Client {0} already exist, not added.".format(name))
            return False
        else:
            params = GetDeviceParams(self._xplPlugin, instance)
            if params:
                if params['operator'] in OPERATORS_SERVICE:
                    self.clients[name] = NabaztagClient(self, params, self._xplPlugin.log)
                else:
                    self._xplPlugin.log.error(
                        u"Manager Client : Nabaztag Client type {0} not exist, not added.".format(name))
                    return False
                self._xplPlugin.log.info(u"Manager Client : created new client {0}.".format(name))
            else:
                self._xplPlugin.log.info(
                    u"Manager Client : instance not configured can't add new client {0}.".format(name))
                return False
            return True

    def removeClient(self, name):
        """Remove a Nabaztag client and close it"""
        client = self.getClient(name)
        if client:
            client.close()
            self.clients.pop(name)

    def getClient(self, id):
        """Get Nabaztag client object by id."""
        if self.clients.has_key(id):
            return self.clients[id]
        else:
            return None

    def getIdsClient(self, idToCheck):
        """Get Nabaztag client key ids."""
        retval = []
        findId = ""
        self._xplPlugin.log.debug(u"getIdsClient check for device : {0}".format(idToCheck))
        if isinstance(idToCheck, NabaztagClient):
            for id in self.clients.keys():
                if self.clients[id] == idToCheck:
                    retval = [id]
                    break
        else:
            self._xplPlugin.log.debug(u"getIdsClient, no NabaztagClient instance...")
            if isinstance(idToCheck, str):
                findId = idToCheck
                self._xplPlugin.log.debug(u"str instance...")
            else:
                if isinstance(idToCheck, dict):
                    if idToCheck.has_key('to'):
                        findId = idToCheck['to']
                    else:
                        if idToCheck.has_key('name') and idToCheck.has_key('id'):
                            findId = getClientId(idToCheck)
            if self.clients.has_key(findId):
                retval = [findId]
                self._xplPlugin.log.debug(u"key id type find")
            else:
                self._xplPlugin.log.debug(
                    u"No key id type, search {0} in devices {1}".format(findId, self.clients.keys()))
                for id in self.clients.keys():
                    self._xplPlugin.log.debug(
                        u"Search in list by device key : {0}".format(self.clients[id].domogikDevice))
                    if self.clients[id].domogikDevice == findId:
                        self._xplPlugin.log.debug('find Nabaztag Client :)')
                        retval.append(id)
        self._xplPlugin.log.debug(u"getIdsClient result : {0}".format(retval))
        return retval

    def refreshClientDevice(self, client):
        """Request a refresh domogik device data for a Nabaztag Client."""
        cli = MQSyncReq(zmq.Context())
        msg = MQMessage()
        msg.set_action('device.get')
        msg.add_data('type', 'plugin')
        msg.add_data('name', self._xplPlugin.get_plugin_name())
        msg.add_data('host', get_sanitized_hostname())
        devices = cli.request('dbmgr', msg.get(), timeout=10).get()
        for a_device in devices:
            if a_device['device_type_id'] == client._device['device_type_id'] and a_device['id'] == client._device[
                'id']:
                if a_device['name'] != client.device['name']:  # rename and change key client id
                    old_id = getClientId(client._device)
                    self.clients[getClientId(a_device)] = self.clients.pop(old_id)
                    self._xplPlugin.log.info(u"Nabaztag Client {0} is rename {1}".format(old_id, getClientId(a_device)))
                client.updateDevice(a_device)
                break

    def sendXplAck(self, data):
        """Send an ack xpl message"""
        self._cb_send_xPL("sendmsg.confirm", data)

    def sendXplTrig(self, schema, data):
        """Send an xpl message"""
        self._cb_send_xPL(schema, data)
