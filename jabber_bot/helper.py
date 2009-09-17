#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Helper:
    """Shows help"""

    def __init__(self, plugins):
        self.plugins = plugins

    def run(self, contact, message):
        msg = 'List of keywords: help '
        if message:
            try:
                msg = '%s - %s' % (message, self.plugins[message].__doc__)
            except KeyError:
                if message == 'help':
                    msg = 'help - Shows help'
                else:
                    msg = '%s is not a keyword' % message
        else:
            for (key, object) in self.plugins.iteritems():
                msg += key + ' '
        contact.send(msg) 

    def exit(self):
        pass

