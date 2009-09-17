#!/usr/bin/env python
# -*- coding: utf-8 -*-

class EchoPlugin:
    """Echoes message"""

    def __init__(self):
        print "echo init"

    def run(self, contact, msg):
        contact.send(msg)

    def exit(self):
        print "echo exit"

provides = {'echo': EchoPlugin}

