#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xmpp

class Contact:

    def __init__(self, conn, jid):
        self.conn = conn
        self.jid = jid

    def get_jid(self):
        return self.jid

    def send(self, msg):
        self.conn.send(xmpp.Message(self.jid, msg, 'chat'))

