#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmpp, pluginLoader, contact

class JabberBotException(Exception):
    pass

class JabberBot:
    
    def __init__(self, jid, password, plugin_path):
        self.__establish_connection(jid, password)
        
        self.client.RegisterHandler('message', self.__message_handler)
        self.client.RegisterHandler('presence', self.__presence_handler)
        self.client.RegisterHandler('iq', self.__iq_handler)

        self.plugins = pluginLoader.PluginLoader(plugin_path)
        self.client.sendInitPresence()

    def __establish_connection(self, jid, password):
        sp = jid.split('@')
        if len(sp) != 2:
            raise JabberBotException('JID should be in format name@server.')
        
        self.client = xmpp.Client(sp[1], debug=[])
        conn = self.client.connect()
        if not conn:
            raise JabberBotException("Can't connect.")

        auth = self.client.auth(sp[0],password,'jabber_bot')
        if not auth:
            raise JabberBotException("Can't authenticate.")


    def __message_handler(self, conn, msg):
        txt = msg.getBody()
        if txt:
            split_txt = txt.strip().split(' ',1)
            try:
                plugin = self.plugins.get_plugin(split_txt[0])
                plugin.run(contact.Contact(conn, msg.getFrom()), split_txt[1])
            except KeyError:
                plugin = self.plugins.get_plugin('help')
                plugin.run(contact.Contact(conn, msg.getFrom()), '')
            except IndexError:
                plugin.run(contact.Contact(conn, msg.getFrom()), '')

    def __presence_handler(self, conn, node):
        if node.getType() == 'subscribe':
            self.client.getRoster().Authorize(node.getFrom())

    def __iq_handler(self, conn, node):
        pass

    def loop(self,timeout=1):
        try:
            while True:
                self.client.Process(timeout)
        except KeyboardInterrupt:
            self.plugins.exit()

if __name__ == '__main__':
    a = JabberBot('pokusny_kralicek@jabbim.cz', 'heslo', 'plugins')
    a.loop()

